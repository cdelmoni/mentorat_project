from django import forms
from django.forms.utils import ErrorList

#import floppyforms.__future__ as forms

from .models import Mentor, EDA, Student, Teacher, Contract, Convocation, Discipline

from .apps import CURRENT_YEAR


class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small_error">%s</p>' % e for e in self])


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['classe', 'email', 'portable', 'tel']
        readonly_fields = ['name', 'vorname', 'id_OD']


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'


class MentorForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = '__all__'


class MentorFormWithStudent(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MentorFormWithStudent, self).__init__(*args, **kwargs)

        self.fields['teacher'].queryset = Teacher.objects.order_by('name')
        self.fields['discipline'].queryset = Discipline.objects.order_by('name')

    class Meta:
        model = Mentor

        fields = [
            'student',
            'discipline',
            'teacher',
            'inscription_date',
            'remark',
            'is_active'
        ]

        widgets = {
            'student': forms.HiddenInput,
        }

        labels = {
            'teacher': "Maître de branche",
            'discipline': "Branche",
        }

        readonly_fields = [
            'student',
        ]



class EDAForm(forms.ModelForm):

    class Meta:
        model = EDA
        fields = '__all__'


class EDAFormWithStudent(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EDAFormWithStudent, self).__init__(*args, **kwargs)

        self.fields['teacher'].queryset = Teacher.objects.order_by('name')
        self.fields['discipline'].queryset = Discipline.objects.order_by('name')


    class Meta:
        model = EDA

        fields = [
            'student',
            'discipline',
            'teacher',
            'inscription_date',
            'remark',
            'is_active'
        ]

        widgets = {
            'student': forms.HiddenInput,
        }

        labels = {
            'teacher': "Maître de branche",
            'discipline': "Branche",
        }

        readonly_fields = [
            'student',
            'year'
        ]


# Forms for contracts
class ContractForm(forms.ModelForm):
    """ Form to create a contract """
    class Meta:
        model = Contract

        fields = [
            'eda',
            'mentor',
            'end_date',
            'remark',
            'contract_parent'
        ]

        widgets = {
            'eda': forms.HiddenInput,
            'mentor': forms.HiddenInput
        }

        labels = {
            'remark': "Remarque"
        }

        readonly_fields = [
            'discipline',
            'eda',
            'year'
        ]


class ContractFormWithEDA(forms.ModelForm):
    """ Form to create a contract with data of an EDA """

    def __init__(self, *args, **kwargs):
        discipline_id = kwargs.pop('discipline_id', None)
        super(ContractFormWithEDA, self).__init__(*args, **kwargs)

        if discipline_id:
            self.fields['mentor'].queryset = Mentor.objects.filter(discipline_id=discipline_id, year=CURRENT_YEAR)

    class Meta:
        model = Contract

        fields = [
            'discipline',
            'eda',
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


class ContractFormDuplicate(forms.ModelForm):
    """ Form to create a contract from a parent one """

    class Meta:
        model = Contract

        fields = [
            'discipline',
            'eda',
            'mentor',
            'remark',
            'contract_parent'
        ]

        widgets = {
            'eda': forms.HiddenInput,
            'mentor': forms.HiddenInput,
            'discipline': forms.HiddenInput,
            'year': forms.HiddenInput,
        }

        labels = {
            'eda': "Demandeur d'aide",
            'remark': "Remarque"
        }


# Forms for convocations
class ConvocationFormWithContract(forms.ModelForm):
    """ Form to create a convocation from a contract """
    contract = forms.HiddenInput()

    class Meta:
        model = Convocation

        fields = [
            'contract',
            'date',
            'time',
            'place',
            'message'
        ]

        widgets = {
            'contract': forms.HiddenInput,
            'date': forms.SelectDateWidget,
            'time': forms.DateTimeInput,
            'place': forms.TextInput(attrs={'maxlength': 64}),
            'message': forms.TextInput(attrs={'maxlength': 64}),
        }

        readonly_fields = [
            'contract'
        ]
