from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Discipline, Student, Teacher, EDA, Mentor
from .forms import MentorForm, EDAForm, StudentForm, TeacherForm
from .apps import CURRENT_YEAR
from .filter import MentorFilter, EDAFilter, StudentFilter, TeacherFilter



@login_required
def index(request):
    disciplines = Discipline.objects.order_by('name')
    mentors = Mentor.objects.filter(year=CURRENT_YEAR)
    edas = EDA.objects.filter(year=CURRENT_YEAR)
    context = {
        'disciplines': disciplines,
        'mentors': mentors,
        'edas': edas
    }
    return render(request, 'pymentorat/index.html', context)

@login_required
def mentor_filter_list(request):
    mentor_list = Mentor.objects.order_by('student__nom')
    mentor_filter = MentorFilter(request.GET, queryset=mentor_list)
    return render(request, 'pymentorat/mentor_list.html', {'filter': mentor_filter})

@login_required
def mentor_create(request):
    if request.POST:
        form = MentorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pymentorat:mentor_list')
    else:
        form = MentorForm()
    return render(request,'pymentorat/mentor_form.html',{'form':form})

@login_required
def mentor_update(request, id_mentor):
    mentor = get_object_or_404(Mentor, pk=id_mentor)
    form = MentorForm(request.POST or None, instance=mentor)
    if form.is_valid():
        form.save()
        return redirect('pymentorat:mentor_list')
    return render(request,'pymentorat/mentor_form.html',{'form':form})

@login_required
def eda_filter_list(request):
    eda_list = EDA.objects.order_by('student__nom')
    eda_filter = EDAFilter(request.GET, queryset=eda_list)
    return render(request, 'pymentorat/eda_list.html', {'filter': eda_filter})

@login_required
def eda_create(request):
    if request.POST:
        form = EDAForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pymentorat:eda_list')
    else:
        form = MentorForm()
    return render(request,'pymentorat/eda_form.html',{'form':form})

@login_required
def eda_update(request, id_eda):
    eda = get_object_or_404(EDA, pk=id_eda)
    form = EDAForm(request.POST or None, instance=eda)
    if form.is_valid():
        form.save()
        return redirect('pymentorat:eda_list')
    return render(request,'pymentorat/eda_form.html',{'form':form})

@login_required
def student_filter_list(request):
    student_list = Student.objects.order_by('nom')
    student_filter = StudentFilter(request.GET, queryset=student_list)
    return render(request, 'pymentorat/student_list.html', {'filter': student_filter})

@login_required
def student_update(request, id_student):
    student = get_object_or_404(Student, pk=id_student)
    form = StudentForm(request.POST or None, instance=student)
    context = {
        'student_nom': student.nom,
        'student_prenom' : student.prenom,
        'student_id' : student.id_OD,
    }
    if form.is_valid():
        form.save()
        return redirect('pymentorat:student_list')
    context['form'] = form
    return render(request,'pymentorat/student_form.html',context)

@login_required
def teacher_filter_list(request):
    teacher_list = Teacher.objects.order_by('nom')
    teacher_filter = TeacherFilter(request.GET, queryset=teacher_list)
    return render(request, 'pymentorat/teacher_list.html', {'filter': teacher_filter})

@login_required
def teacher_update(request, id_teacher):
    teacher = get_object_or_404(Teacher, pk=id_teacher)
    form = TeacherForm(request.POST or None, instance=teacher)
    if form.is_valid():
        form.save()
        return redirect('pymentorat:teacher_list')
    return render(request,'pymentorat/teacher_form.html',{'form':form})


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MentorListView(LoginRequiredMixin, ListView):
    model = Mentor
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discipline'] = "Allemand"
        return context


class MentorUpdate(LoginRequiredMixin, UpdateView):
    model = Mentor
    fields = [
        'student',
        'teacher',
        'discipline',
        'year',
        'remark'
    ]
