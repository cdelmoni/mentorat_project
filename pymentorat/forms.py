from django import forms
from django.forms.utils import ErrorList
from django.db.models import F

from .models import Mentor, EDA, Student, Teacher, Contract, Discipline

from .apps import CURRENT_YEAR

class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small_error">%s</p>' % e for e in self])


class MentorForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = '__all__'


class MentorFormWithStudent(forms.ModelForm):

   # student = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Mentor

        fields = [
            'student',
            'discipline',
            'teacher',
            'year',
            'classe',
            'remark',
            'is_active'
        ]

        widgets = {
            'student': forms.HiddenInput
        }

        labels = {
            'discipline': 'Branche',
            'teacher': "Maître de branche",
        }

        readonly_fields = [
            'student',
            'year'
        ]


class EDAForm(forms.ModelForm):
    class Meta:
        model = EDA
        fields = '__all__'


class EDAFormWithStudent(forms.ModelForm):

    class Meta:
        model = EDA

        fields = [
            'student',
            'discipline',
            'teacher',
            'year',
            'classe',
            'remark',
            'is_active'
        ]

        widgets = {
            'student': forms.HiddenInput
        }

        labels = {
            'discipline': 'Branche',
            'teacher': "Maître de branche",
        }

        readonly_fields = [
            'student',
            'year'
        ]


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['email', 'tel', 'portable']
        readonly_fields = ['name', 'vorname', 'id_OD']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'


class ContractForm(forms.ModelForm):

    #discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), disabled=True)

    class Meta:
        model = Contract

        fields = [
            'eda',
            'year',
            'mentor',
            'end_date',
            'remark',
            'contract_parent'
        ]

        labels = {
            'eda': "Demandeur d'aide",
            'mentor': "Mentor",
            'remark': "Remarque"
        }

        readonly_fields = [
            'discipline',
            'eda',
            'year'
        ]

class ContractFormWithEDA(forms.ModelForm):

    discipline = forms.HiddenInput()

    class Meta:
        model = Contract

        fields = [
            'discipline',
            'eda',
            'year',
            'mentor',
            'remark',
            'contract_parent'
        ]

        widgets = {
            'eda': forms.HiddenInput,
            'discipline': forms.HiddenInput,
            'year': forms.HiddenInput,
        }

        labels = {
            'eda': "Demandeur d'aide",
            'mentor': "Mentor",
            'remark': "Remarque"
        }

        readonly_fields = [
            'discipline',
            'eda',
            'year'
        ]


