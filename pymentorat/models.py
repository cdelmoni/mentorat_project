from django.db import models
from django import forms
from django.urls import reverse

from .apps import CURRENT_YEAR

class Student(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    tel = models.CharField(max_length=13, null=True, blank=True)
    portable = models.CharField(max_length=13, null=True, blank=True)
    id_OD = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return "{0} {1}".format(self.nom,self.prenom)

    class Meta:
        verbose_name = "Elève"
        verbose_name_plural = "Elèves"


class Teacher(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    id_OD = models.CharField(max_length=12, unique=True, null=True)

    def __str__(self):
        return "{0} {1}".format(self.nom, self.prenom)

    class Meta:
        verbose_name = "Maître"
        verbose_name_plural = "Maîtres"


class Discipline(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Discipline"
        verbose_name_plural = "Disciplines"

class Mentor(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    year = models.IntegerField(default=CURRENT_YEAR)
    classe = models.CharField(max_length=12)
    inscription_date = models.DateTimeField(auto_now_add=True)
    remark = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{0} {1} mentor pour {2}".format(self.student.nom, self.student.prenom, self.discipline.name)

    def get_absolute_url(self):
        return reverse('pymentorat:mentor_update', kwargs={'id_mentor': self.pk})

    class Meta:
        verbose_name = "Elève mentor"
        verbose_name_plural = "Elèves mentors"


class EDA(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    year = models.IntegerField(default=CURRENT_YEAR)
    classe = models.CharField(max_length=12)
    inscription_date = models.DateTimeField(auto_now_add=True)
    remark = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{0} {1} eda pour {2}".format(self.student.nom, self.student.prenom, self.discipline.name)

    class Meta:
        verbose_name = "Elève demandeur d'aide"
        verbose_name_plural = "Elèves demandeurs d'aide"


class Contrat(models.Model):
    eda = models.ForeignKey(EDA, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    contrat_parent = models.ForeignKey('self', null=True, blank=True,  on_delete=models.CASCADE)
    begin_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Contrat {0} avec {1} en {2} - {3}".format(self.eda.student.nom, self.mentor.student.nom, self.discipline.name, self.begin_date)

    class Meta:
        verbose_name = "Contrat"
        verbose_name_plural = "Contrats"


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
