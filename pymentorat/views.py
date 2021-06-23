from datetime import date

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.utils.timezone import now
from django.utils.text import slugify

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from io import BytesIO

from .models import Discipline, Student, Teacher, EDA, Mentor, Contract, Convocation
from .forms import MentorForm, EDAForm, StudentForm, TeacherForm, ContractForm, ParagraphErrorList, ContractFormWithEDA
from .forms import MentorFormWithStudent, EDAFormWithStudent, ConvocationFormWithContract, ContractFormDuplicate
from .apps import CURRENT_YEAR
from .filter import MentorFilter, EDAFilter, StudentFilter, TeacherFilter, ContractFilter

@login_required
def index(request):
    """ Function based view to render the home page """
    disciplines = Discipline.objects.order_by('name')
    mentors = Mentor.objects.filter(year=CURRENT_YEAR, is_active=True)
    edas = EDA.objects.filter(year=CURRENT_YEAR, is_active=True)
    contracts = Contract.objects.filter(year=CURRENT_YEAR, end_date=None).order_by('discipline')
    convocations = Convocation.objects.filter(date__gt = now()).order_by('date', 'time')
    context = {
        'disciplines': disciplines,
        'mentors': mentors,
        'nb_mentors': mentors.count(),
        'edas': edas,
        'nb_edas': edas.count(),
        'contracts': contracts,
        'nb_contracts': contracts.count(),
        'convocations': convocations,
        'nbconvocations': convocations.count(),
    }
    return render(request, 'pymentorat/index.html', context)


# Views for students
@login_required
def student_filter_list(request):
    """ Function based view to render the list of all the students, with a filter. """
    student_list = Student.objects.order_by('name')
    student_filter = StudentFilter(request.GET, queryset=student_list)
    return render(request, 'pymentorat/student_list.html', {'filter': student_filter})

@login_required
def student_details(request, id_student):
    """ Function based view to edit an EDA. """
    student = get_object_or_404(Student, pk=id_student)
    contract_list = Contract.objects.filter(Q(mentor__student=student) | Q(eda__student=student), year=CURRENT_YEAR)
    mentor_list = Mentor.objects.filter(student=student, year=CURRENT_YEAR)
    eda_list = EDA.objects.filter(student=student, year=CURRENT_YEAR)
    context = {
        'student_pk' : student.pk,
        'student_name': student.name,
        'student_vorname': student.vorname,
        'student_portable' : student.portable,
        'student_email': student.email,
        'classe': student.classe,
        'contracts': contract_list,
        'nb_contracts': contract_list.count(),
        'mentors' : mentor_list,
        'nb_mentors': mentor_list.count(),
        'edas' : eda_list,
        'nb_edas': eda_list.count(),
    }

    return render(request,'pymentorat/student_details.html', context)

@login_required
def student_update(request, id_student):
    """ Function based view to edit a students. """
    student = get_object_or_404(Student, pk=id_student)
    form = StudentForm(request.POST or None, instance=student)
    context = {
        'student_name': student.name,
        'student_vorname' : student.vorname,
        'student_id' : student.id_OD,
        'student_classe' : student.classe
    }
    if form.is_valid():
        form.save()
        return redirect(student.get_absolute_url())
    context['form'] = form
    return render(request,'pymentorat/student_form.html', context)


# Views for teachers
@login_required
def teacher_filter_list(request):
    """ Function based view to render the list of all the teachers, with a filter. """
    teacher_list = Teacher.objects.order_by('name')
    teacher_filter = TeacherFilter(request.GET, queryset=teacher_list)
    return render(request, 'pymentorat/teacher_list.html', {'filter': teacher_filter})


@login_required
def teacher_update(request, id_teacher):
    """ Function based view to edit a teacher. """
    teacher = get_object_or_404(Teacher, pk=id_teacher)
    form = TeacherForm(request.POST or None, instance=teacher)
    if form.is_valid():
        form.save()
        return redirect('pymentorat:teacher_list')
    return render(request,'pymentorat/teacher_form.html',{'form':form})


# Views for mentors
@login_required
def mentor_filter_list(request):
    """ Function based view to render the list of current year mentors, with a filter. """
    mentor_list = Mentor.objects.filter(year=CURRENT_YEAR, is_active=True).order_by('student__name')
    mentor_filter = MentorFilter(request.GET, queryset=mentor_list)
    return render(request, 'pymentorat/mentor_list.html', {'filter': mentor_filter})

@login_required
def mentor_details(request, id_mentor):
    """ Function based view to edit an EDA. """
    mentor = get_object_or_404(Mentor, pk=id_mentor)
    contract_list = Contract.objects.filter(mentor=mentor, year=CURRENT_YEAR)
    context = {
        'mentor_pk' : mentor.pk,
        'mentor_name': mentor.student.name,
        'mentor_vorname': mentor.student.vorname,
        'mentor_portable' : mentor.student.portable,
        'mentor_classe': mentor.student.classe,
        'mentor_discipline' : mentor.discipline,
        'student_pk' : mentor.student.pk,
        'teacher_name': mentor.teacher.name,
        'teacher_vorname': mentor.teacher.vorname,
        'contracts': contract_list,
        'nb_contracts': contract_list.count()
    }

    return render(request,'pymentorat/mentor_details.html', context)

@login_required
def mentor_create(request):
    """ Function based view to create a mentor. """
    if request.POST:
        form = MentorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pymentorat:mentor_list')
    else:
        form = MentorForm()
    return render(request, 'pymentorat/mentor_form.html', {'form':form})


@login_required
def mentor_create_from_student(request, id_student):
    """ Function based view to create a mentor from a selected student. """
    student = get_object_or_404(Student, pk=id_student)

    form = MentorFormWithStudent(request.POST or None, error_class=ParagraphErrorList,
                                 initial={'student': student})
    context = {
        'student_name': student.name,
        'student_vorname': student.vorname,
        'student_classe': student.classe,
        'status': 'new',
    }
    if form.is_valid():
        form.save()
        return redirect('pymentorat:mentor_list')
    context['form'] = form
    return render(request,'pymentorat/mentor_form.html', context=context)


@login_required
def mentor_update(request, id_mentor):
    """ Function based view to edit a mentor. """
    mentor = get_object_or_404(Mentor, pk=id_mentor)
    form = MentorFormWithStudent(request.POST or None, instance=mentor)
    context = {
        'student_name': mentor.student.name,
        'student_vorname': mentor.student.vorname,
        'student_classe' : mentor.student.classe,
        'status': 'update',
    }
    if form.is_valid():
        form.save()
        return redirect('pymentorat:mentor_list')
    context['form'] = form
    return render(request,'pymentorat/mentor_form.html', context=context)


# Views for EDAs
@login_required
def eda_filter_list(request):
    """ Function based view to render the list of current year EDAs, with a filter. """
    eda_list = EDA.objects.filter(year=CURRENT_YEAR, is_active=True).order_by('inscription_date')
    eda_filter = EDAFilter(request.GET, queryset=eda_list)
    context = {
        'filter': eda_filter,
        'title': "Liste des élèves demandeurs d'aide"
    }
    return render(request, 'pymentorat/eda_list.html', context)


@login_required
def eda_filter_nomentor_list(request):
    """ Function based view to render the list of current year EDAs waiting for a mentor, with a filter. """
    eda_list = EDA.objects.filter(contract__end_date=None, year=CURRENT_YEAR, is_active=True).order_by('inscription_date')
    eda_filter = EDAFilter(request.GET, queryset=eda_list)
    context = {
        'filter': eda_filter,
        'title': "EDA sans mentor"
    }
    return render(request, 'pymentorat/eda_list.html', context)

@login_required
def eda_details(request, id_eda):
    """ Function based view to edit an EDA. """
    eda = get_object_or_404(EDA, pk=id_eda)
    contract_list = Contract.objects.filter(eda=eda, year=CURRENT_YEAR)
    context = {
        'eda_pk' : eda.pk,
        'eda_name': eda.student.name,
        'eda_vorname': eda.student.vorname,
        'eda_portable' : eda.student.portable,
        'eda_classe': eda.student.classe,
        'eda_discipline' : eda.discipline,
        'student_pk': eda.student.pk,
        'teacher_name': eda.teacher.name,
        'teacher_vorname': eda.teacher.vorname,
        'contracts': contract_list,
        'nb_contracts': contract_list.count()
    }

    return render(request,'pymentorat/eda_details.html', context)

@login_required
def eda_create(request):
    """ Function based view to create an EDA. """
    if request.POST:
        form = EDAForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pymentorat:eda_list')
    else:
        form = MentorForm()
    return render(request,'pymentorat/eda_form.html',{'form':form})


@login_required
def eda_create_from_student(request, id_student):
    """ Function based view to create a mentor from a selected student. """
    student = get_object_or_404(Student, pk=id_student)

    form = EDAFormWithStudent(request.POST or None, error_class=ParagraphErrorList,
                                 initial={'student': student})
    context = {
        'student_name': student.name,
        'student_vorname': student.vorname,
        'student_classe': student.classe,
        'status': 'new',
    }
    if form.is_valid():
       # print(form.cleaned_data['student'])
        form.save()
        return redirect('pymentorat:eda_list')
    context['form'] = form
    return render(request,'pymentorat/eda_form.html', context=context)


@login_required
def eda_update(request, id_eda):
    """ Function based view to edit an EDA. """
    eda = get_object_or_404(EDA, pk=id_eda)
    form = EDAFormWithStudent(request.POST or None, instance=eda)
    context = {
        'student_name': eda.student.name,
        'student_vorname': eda.student.vorname,
        'student_classe': eda.student.classe,
        'status': 'update',
    }
    if form.is_valid():
        form.save()
        return redirect('pymentorat:eda_list')
    context['form'] = form
    return render(request,'pymentorat/eda_form.html',context=context)


# Views for contracts
@login_required
def contract_filter_list(request):
    """ Function based view to render the list of current year contracts, with a filter. """
    contract_list = Contract.objects.filter(year=CURRENT_YEAR).order_by('begin_date')
    contract_filter = ContractFilter(request.GET, queryset=contract_list)
    context = {
        'filter': contract_filter,
        'current_year': 2018
    }
    return render(request, 'pymentorat/contract_list.html', context)

@login_required
def contract_create_from_eda(request, id_eda):
    """ Function based view to create a contract. """
    eda = get_object_or_404(EDA, pk=id_eda)
    form = ContractFormWithEDA(request.POST or None, error_class=ParagraphErrorList,
                               discipline_id=eda.discipline.pk,
                               initial={'eda': eda, 'discipline': eda.discipline})
    context = {
        'eda_name': eda.student.name,
        'eda_vorname': eda.student.vorname,
        'eda_classe': eda.student.classe,
        'year': eda.year,
        'discipline': eda.discipline.name,
        'status': 'new',
    }
    if form.is_valid():
        form.save()
        return redirect('pymentorat:contract_list')
    context['form'] = form
    return render(request,'pymentorat/contract_form.html',context=context)

@login_required
def contract_duplicate(request, id_contract):
    """ Function based view to create a contract. """
    contract_parent = get_object_or_404(Contract, pk=id_contract)
    eda = contract_parent.eda
    mentor = contract_parent.mentor
    form = ContractFormDuplicate(request.POST or None, error_class=ParagraphErrorList,
                               initial={'eda': eda, 'mentor':mentor, 'discipline': eda.discipline, 'contract_parent': contract_parent})
    context = {
        'eda_name': eda.student.name,
        'eda_vorname': eda.student.vorname,
        'eda_classe': eda.student.classe,
        'mentor_name': mentor.student.name,
        'mentor_vorname': mentor.student.vorname,
        'mentor_classe': mentor.student.classe,
        'year': eda.year,
        'discipline': eda.discipline.name,
        'status': 'new',
    }
    if form.is_valid():
        form.save()
        return redirect('pymentorat:contract_list')
    context['form'] = form
    return render(request,'pymentorat/contract_form.html',context=context)

@login_required
def contract_update(request, id_contract):
    """ Function based view to edit a contract. """
    contract = get_object_or_404(Contract, pk=id_contract)
    form = ContractForm(request.POST or None, instance=contract, error_class=ParagraphErrorList,
                       initial={'eda': contract.eda, 'mentor': contract.mentor, 'begin_date': contract.begin_date})
    context = {
        'eda_name': contract.eda.student.name,
        'eda_vorname': contract.eda.student.vorname,
        'eda_classe': contract.eda.student.classe,
        'mentor_name': contract.mentor.student.name,
        'mentor_vorname': contract.mentor.student.vorname,
        'mentor_classe': contract.mentor.student.classe,
        'year': contract.year,
        'discipline': contract.discipline.name,
        'begin_date': contract.begin_date,
        'status': 'update',
    }
    if form.is_valid():
        form.save()
        return redirect('pymentorat:contract_list')
    context['form'] = form
    return render(request,'pymentorat/contract_form.html',context=context)

# Views for convocations
@login_required
def convocation_create_from_contract(request, id_contract):
    """ Function based view to create a convocation. """
    contract = get_object_or_404(Contract, pk=id_contract)
    form = ConvocationFormWithContract(request.POST or None, error_class=ParagraphErrorList,
                              initial={'contract': contract, 'date': now()})
    context = {
        'eda_name': contract.eda.student.name,
        'eda_vorname': contract.eda.student.vorname,
        'eda_classe': contract.eda.student.classe,
        'mentor_name': contract.mentor.student.name,
        'mentor_vorname': contract.mentor.student.vorname,
        'mentor_classe': contract.mentor.student.classe,
        'discipline': contract.discipline.name,
        'status': 'new'
    }
    if form.is_valid():
        convocation=form.save()
        return redirect('pymentorat:convocation_pdf', id_convocation=convocation.pk)
    context['form'] = form
    return render(request,'pymentorat/convocation_form.html',context=context)



@login_required
def convocation_update(request, id_convocation):
    """ Function based view to update a convocation. """
    convocation = get_object_or_404(Convocation, pk=id_convocation)
    form = ConvocationFormWithContract(request.POST or None, error_class=ParagraphErrorList,
                              instance=convocation)
    context = {
        'eda_name': convocation.contract.eda.student.name,
        'eda_vorname': convocation.contract.eda.student.vorname,
        'eda_classe': convocation.contract.eda.student.classe,
        'mentor_name': convocation.contract.mentor.student.name,
        'mentor_vorname': convocation.contract.mentor.student.vorname,
        'mentor_classe': convocation.contract.mentor.student.classe,
        'discipline': convocation.contract.discipline.name,
        'status' : 'update'
    }
    if form.is_valid():
        convocation=form.save()
        return redirect('pymentorat:convocation_pdf', id_convocation=convocation.pk)
    context['form'] = form
    return render(request,'pymentorat/convocation_form.html',context=context)

@login_required
def convocation_delete(request, id_convocation):
    """ Function based view to delete a convocation. """
    convocation = get_object_or_404(Convocation, pk=id_convocation)

    if request.method == "POST":
        convocation.delete()
        #messages.success(request, "Post successfully deleted!")
        return redirect('pymentorat:index')

    return render(request, 'pymentorat/convocation_confirm_delete.html',  context={'object':convocation})




### Views for PDF rendering



@login_required
def contract_pdf(request, id_contract):
    contract = get_object_or_404(Contract, pk=id_contract)
    response = HttpResponse(content_type='application/pdf')
    filename = "contrat_mentorat_{0}_{1}.pdf".format(slugify(contract.eda.student.name), slugify(contract.mentor.student.name))
    response['Content-Disposition'] = "attachment;filename={0}".format(filename)

    buffer = BytesIO()

    registerFont(TTFont('Arial', 'pymentorat/static/fonts/Arial.ttf'))
    registerFont(TTFont('Arial-Bold', 'pymentorat/static/fonts/Arial Bold.ttf'))

    logo = ImageReader('pymentorat/static/img/logo_texte_adresse.png')
    logo_scale = 0.1
    logo_width = 1075*logo_scale
    logo_height = 544*logo_scale

    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    height, width  = A4
    head = 2.5*cm
    foot = 2*cm
    left=1*cm

    right=2*cm

    def xpos(x):
        return x*cm+left

    def ypos(y):
        return -y*cm-head

    # p = canvas.Canvas(response, pagesize=landscape(A4))
    p.translate(0,height)

    p.setFont("Arial-Bold", 18)

    p.drawImage(logo, xpos(0), ypos(0), logo_width, logo_height, anchor='sw', anchorAtXY=True, showBoundary=False)

    p.drawCentredString(width/4, ypos(1), "Contrat de Mentorat" )

    p.setFont("Arial", 9)
    p.drawCentredString(width / 4, ypos(1.5), "(A conserver en parfait état)")

    p.line(xpos(0), ypos(2), width / 2 - 1 * cm, ypos(2))

    p.setFont("Arial-Bold", 12)
    p.drawString(xpos(0), ypos(2.5), "Branche :")
    p.setFont("Arial", 11)
    p.drawString(xpos(4.5), ypos(2.5), "{branche}".format(branche=contract.discipline))

    p.line(xpos(0), ypos(3), width / 2 - 1 * cm, ypos(3))

    p.setFont("Arial-Bold", 12)
    p.drawString(xpos(0), ypos(3.5), "Mentor : ")

    p.setFont("Arial", 11)
    p.drawString(xpos(4.5), ypos(3.5), "{nom} {prenom} ({classe})".format(nom=contract.mentor.student.name,
                                                                          prenom=contract.mentor.student.vorname,
                                                                          classe=contract.mentor.student.classe
                                                                         ))

    p.setFont("Arial", 10)
    p.drawString(xpos(0.5), ypos(4.5), "Port. : {natel}".format(natel=contract.mentor.student.portable ))
    p.drawString(xpos(4.5), ypos(4.5),"Email : {email}".format(email=contract.mentor.student.email))

    p.line(xpos(0), ypos(5), width / 2 - 1 * cm, ypos(5))

    p.setFont("Arial-Bold", 12)
    p.drawString(xpos(0), ypos(5.5), "Demandeur d'aide :")
    p.setFont("Arial", 11)
    p.drawString(xpos(4.5), ypos(5.5), "{nom} {prenom} ({classe})".format(nom=contract.eda.student.name,
                                                                         prenom=contract.eda.student.vorname,
                                                                         classe=contract.eda.student.classe
                                                                         ))
    p.setFont("Arial", 10)
    p.drawString(xpos(0.5), ypos(6.5), "Port. : {natel}".format(natel=contract.eda.student.portable))
    p.drawString(xpos(4.5), ypos(6.5), "Email : {email}".format(email=contract.eda.student.email))



    p.line(xpos(0), ypos(7), width / 2 - 1 * cm, ypos(7))

    p.drawString(xpos(0), ypos(8), "Date et lieu : Cheseaux-Noréaz, le ")
    p.drawString(xpos(6), ypos(8), "...........................................")
    p.drawString(xpos(0), ypos(9), "Signature du mentor")
    p.drawString(xpos(6), ypos(9), "...........................................")

    p.drawString(xpos(0), ypos(10), "Signature du demandeur")
    p.drawString(xpos(6), ypos(10), "...........................................")

    p.line(xpos(0), ypos(10.5), width / 2 - 1 * cm, ypos(10.5))

    p.setFont("Arial-Bold", 12)
    p.drawString(xpos(0), ypos(11.5), "Signatures de la responsable du mentorat (S. Amy) :")

    p.setFont("Arial", 11)
    p.drawString(xpos(0), ypos(12.5), "Avant la première séance")
    p.drawString(xpos(6), ypos(12.5), "...........................................")

    p.drawString(xpos(0), ypos(13.5), "Après la dernière séance")
    p.drawString(xpos(6), ypos(13.5), "...........................................")



    p.line(xpos(0), ypos(14), width / 2 - 1 * cm, ypos(14))
    p.setFont("Arial-Bold", 11)
    p.drawString(xpos(0), ypos(15), "A remettre au secrétariat en fin de contrat, avec les deux signatures")
    p.drawString(xpos(0), ypos(15.5), "de la responsable, pour l'obtention de l'aide à la formation.")


    # sepéaration
    p.line(width / 2, -0.5*cm , width / 2, -height + 0.5*cm)

    # Page 2
    head = 2 * cm

    p.setFont("Arial-Bold", 18)

    p.drawCentredString(3*width / 4, ypos(0), "Fiche de suivi")

    p.setFont("Arial", 11)
    p.drawCentredString(3 * width / 4, ypos(1), "A remplir à l'issue de chaque séance.")

    p.line(width / 2 + 1 * cm, ypos(1.5), width - 1 * cm, ypos(1.5))

    p.line(width / 2 + 1 * cm, ypos(2.5), width - 1 * cm, ypos(2.5))
    p.line(width / 2 + 1 * cm, ypos(5), width - 1 * cm, ypos(5))
    p.line(width / 2 + 1 * cm, ypos(7.5), width - 1 * cm, ypos(7.5))
    p.line(width / 2 + 1 * cm, ypos(10), width - 1 * cm, ypos(10))
    p.line(width / 2 + 1 * cm, ypos(12.5), width - 1 * cm, ypos(12.5))
    p.line(width / 2 + 1 * cm, ypos(15), width - 1 * cm, ypos(15))
    p.line(width / 2 + 1 * cm, ypos(17.5), width - 1 * cm, ypos(17.5))

    p.line(width / 2 + 1 * cm, ypos(1.5), width / 2 + 1 * cm, ypos(17.5))
    p.line(width / 2 + 2.5 * cm, ypos(1.5), width / 2 + 2.5 * cm, ypos(17.5))
    p.line(width / 2 + 11 * cm, ypos(1.5), width / 2 + 11 * cm, ypos(17.5))
    p.line(width - 1 * cm, ypos(1.5), width - 1 * cm, ypos(17.5))

    p.setFont("Arial", 11)
    p.drawString(width / 2 + xpos(0.1), ypos(2), "Dates")
    p.drawString(width / 2 + xpos(1.6), ypos(2), "Sujets abordés")
    p.drawString(width / 2 + xpos(10.1), ypos(2), "Signatures")
    p.drawString(width / 2 + xpos(0.1), ypos(3), "1.")
    p.drawString(width / 2 + xpos(0.1), ypos(5.5), "2.")
    p.drawString(width / 2 + xpos(0.1), ypos(8), "3.")
    p.drawString(width / 2 + xpos(0.1), ypos(10.5), "4.")
    p.drawString(width / 2 + xpos(0.1), ypos(13), "5.")
    p.drawString(width / 2 + xpos(0.1), ypos(15.5), "6.")

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)

    return response

@login_required
def convocation_pdf(request, id_convocation):
    convocation = get_object_or_404(Convocation, pk=id_convocation)
    response = HttpResponse(content_type='application/pdf')
    filename = "convocation_mentorat_{0}_{1}.pdf".format(slugify(convocation.contract.eda.student.name),
                                                   slugify(convocation.contract.mentor.student.name))
    response['Content-Disposition'] = "attachment;filename={0}".format(filename)

    eda = convocation.contract.eda
    mentor = convocation.contract.mentor


    buffer = BytesIO()

    registerFont(TTFont('Arial', 'pymentorat/static/fonts/Arial.ttf'))
    registerFont(TTFont('Arial-Bold', 'pymentorat/static/fonts/Arial Bold.ttf'))

    logo = ImageReader('pymentorat/static/img/logo_texte_adresse.png')
    logo_scale = 0.1
    logo_width = 1075*logo_scale
    logo_height = 544*logo_scale

    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    height, width  = A4
    head = 2.5*cm
    foot = 2*cm
    left=1*cm

    right=2*cm



    p.translate(0,height)

    def page(dest, head, left):
        def xpos(x):
            return x * cm + left

        def ypos(y):
            return -y * cm - head

        p.setFont("Arial-Bold", 18)

        p.drawImage(logo, xpos(0), ypos(0), logo_width, logo_height, anchor='sw', anchorAtXY=True, showBoundary=False)

        p.setFont("Arial", 10)
        p.drawString(xpos(7), ypos(0), "Cheseaux-Noréaz, le {0}".format(date.today().strftime('%d.%m.%Y')))

        p.setFont("Arial-Bold", 18)
        p.drawCentredString(xpos(6.5), ypos(1.5), "Convocation" )

        p.setFont("Arial", 18)
        p.drawString(xpos(0), ypos(3), "{0} {1} ({2})".format(dest.student.vorname, dest.student.name, dest.student.classe))

        p.setFont("Arial", 14)
        p.drawString(xpos(0), ypos(5), "Concerne : Contrat de mentorat")

        p.setFont("Arial", 14)
        p.drawString(xpos(0), ypos(7), "Merci de vous présenter {0}".format(convocation.place.casefold()))
        p.drawString(xpos(5.45), ypos(8), "le {0} à {1}".format(convocation.date.strftime('%A %d.%m.%Y'),
                                                                convocation.time.strftime('%H:%M')))

        if (convocation.message != None):
            p.drawString(xpos(0), ypos(10),"{0}".format(convocation.message))

        p.drawCentredString(xpos(8), ypos(13), "Sandrine Amy")
        p.drawCentredString(xpos(8), ypos(14), "Responsable du mentorat")

    page(eda, head, left)

    # sepéaration
    p.line(width / 2, -0.5 * cm, width / 2, -height + 0.5 * cm)

    # Page 2

    page(mentor, head, width/2 + left)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)

    return response


@login_required
def statistiques(request):
    ByBranch = {}

    for disc in Discipline.objects.order_by('name'):
        studentDisc = EDA.objects.filter(discipline=disc.id);

        # TODO: A ameliorer, meme si pour la taille de la bd, pas necessaire...
        ByBranch[disc] = {
            'contracts': Contract.objects.filter(discipline=disc.id).count(),
            'mentors': Mentor.objects.filter(discipline=disc.id).count(),
            'eda': studentDisc.count(),
            'eda1': studentDisc.filter(student__classe__startswith="1").count(),
            'eda2': studentDisc.filter(student__classe__startswith="2").count(),
            'eda3': studentDisc.filter(student__classe__startswith="3").count(),
            'eda1c': studentDisc.filter(student__classe__startswith="1C").count(),
            'eda2c': studentDisc.filter(student__classe__startswith="2C").count(),
            'eda3c': studentDisc.filter(student__classe__startswith="3C").count(),
            'eda1m': studentDisc.filter(student__classe__startswith="1M").count(),
            'eda2m': studentDisc.filter(student__classe__startswith="2M").count(),
            'eda3m': studentDisc.filter(student__classe__startswith="3M").count(),
            'eda4': studentDisc.filter(student__classe__startswith="4").count(),
        }
    
    totaux = {}
    
    totaux['eda1c'] = EDA.objects.filter(student__classe__startswith="1C").count();
    totaux['eda2c'] = EDA.objects.filter(student__classe__startswith="2C").count();
    totaux['eda3c'] = EDA.objects.filter(student__classe__startswith="3C").count();
    totaux['eda1m'] = EDA.objects.filter(student__classe__startswith="1M").count();
    totaux['eda2m'] = EDA.objects.filter(student__classe__startswith="2M").count();
    totaux['eda3m'] = EDA.objects.filter(student__classe__startswith="3M").count();
    
    totaux['eda1'] = totaux['eda1c']+totaux['eda1m'];
    totaux['eda2'] = totaux['eda2c']+totaux['eda2m'];
    totaux['eda3'] = totaux['eda3c']+totaux['eda3m'];
    totaux['eda4'] = EDA.objects.filter(student__classe__startswith="4").count();

    return render(request, 'pymentorat/statistiques.html', {
        'numberof': {
            'byBranch': ByBranch,
            'totaux': totaux,
            'nbstudents': Student.objects.count(),
            'nbmentors': Mentor.objects.count(),
            'nbeda': EDA.objects.count(),
            'nbcontracts': Contract.objects.count()
        }
        })
# Several test to use Class Based Views (no success)

# class StudentListView(LoginRequiredMixin, ListView):
#     model = Student
#     paginate_by = 50
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
#
#
# class MentorListView(LoginRequiredMixin, ListView):
#     model = Mentor
#     paginate_by = 50
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['discipline'] = "Allemand"
#         return context
#
#
# class MentorUpdate(LoginRequiredMixin, UpdateView):
#     model = Mentor
#     fields = [
#         'student',
#         'teacher',
#         'discipline',
#         'year',
#         'remark'
#     ]
#
# class ContractCreateView(LoginRequiredMixin, CreateView):
#     model = Contract
#     fields = [
#         'eda',
#         'mentor',
#         'discipline',
#         'year',
#         'contractParent',
#         'begin_date',
#         'end_date',
#         'remark'
#     ]
#
#     success_url = "/contract/"
#
#
# class ContractCreateView(LoginRequiredMixin, UpdateView):
#     model = Contract
#     fields = [
#         'eda',
#         'mentor',
#         'discipline',
#         'year',
#         'contractParent',
#         'begin_date',
#         'end_date',
#         'remark'
#     ]

class SimpleContractListView(LoginRequiredMixin, ListView):
    model = Contract
    fields = [
        'eda',
        'mentor',
        'discipline',
        'year',
        'contractParent',
        'begin_date',
        'end_date',
        'remark'
    ]
    template_name = "pymentorat/contract_simple_list.html"



# class ContractListView(LoginRequiredMixin, ListView):
#     model = Contract
#     fields = [
#         'eda',
#         'mentor',
#         'discipline',
#         'year',
#         'contractParent',
#         'begin_date',
#         'end_date',
#         'remark'
#     ]

    # def get_queryset(self):
    #     qs = self.model.objects.all()
    #     contract_filtered_list = ContractFilter(self.request.GET, queryset=qs)
    #     return contract_filtered_list.qs

# class ContractDetailView(LoginRequiredMixin, DetailView):
#     model = Contract
