from django import forms

from .models import Mentor, EDA, Student, Teacher

class MentorForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = '__all__'


class EDAForm(forms.ModelForm):
    class Meta:
        model = EDA
        fields = '__all__'


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['email', 'tel', 'portable']
        readonly_fields = ['nom', 'prenom', 'id_OD']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
