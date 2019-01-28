from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError

from core.models import TimeStampedModel
from .apps import CURRENT_YEAR


class Discipline(TimeStampedModel):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Branche"
        verbose_name_plural = "Branches"


class Student(TimeStampedModel):
    name = models.CharField('Nom', max_length=50)
    vorname = models.CharField('Prénom', max_length=50)
    email = models.EmailField('E-mail', null=True, blank=True)
    portable = models.CharField('Portable', max_length=13, null=True, blank=True)
    tel = models.CharField('Téléphone', max_length=13, null=True, blank=True)
    id_OD = models.CharField(max_length=10, unique=True)
    classe = models.CharField('Classe actuelle', max_length=12, null=True, blank=True)

    def __str__(self):
        return "{0} {1}".format(self.name, self.vorname)

    class Meta:
        verbose_name = "Elève"
        verbose_name_plural = "Elèves"

    def get_absolute_url(self):
        return reverse('pymentorat:student_details', kwargs={'id_student': self.pk})


class Teacher(TimeStampedModel):
    name = models.CharField('Nom', max_length=50)
    vorname = models.CharField('Prénom', max_length=50)
    id_OD = models.CharField(max_length=8, unique=True, null=True)

    def __str__(self):
        return "{0} {1}".format(self.name, self.vorname)

    class Meta:
        verbose_name = "Maître"
        verbose_name_plural = "Maîtres"


class Mentor(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    year = models.PositiveIntegerField('Année', default=CURRENT_YEAR)
    inscription_date = models.DateTimeField("Date d'inscription", auto_now_add=True)
    remark = models.TextField('Remarque', null=True, blank=True)
    is_active = models.BooleanField('Actif', default=True, null=False, blank=False)

    class Meta:
        verbose_name = "Elève mentor"
        verbose_name_plural = "Elèves mentors"

    def __str__(self):
        return "{0} {1} mentor pour {2}".format(self.student.name, self.student.vorname, self.discipline.name)

    def clean(self):
        count_same_mentors = Mentor.objects.filter(year=CURRENT_YEAR,
                                                   student=self.student,
                                                   discipline=self.discipline).count()
        if count_same_mentors != 0:
            raise ValidationError(
                "Ce mentor existe déjà !",
                code='eda_not_unique'
            )

    def get_absolute_url(self):
        return reverse('pymentorat:mentor_update', kwargs={'id_mentor': self.pk})

    def get_nb_contracts(self):
        nb = Contract.objects.filter(mentor=self, end_date=None).count()
        return nb


class EDA(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    year = models.PositiveIntegerField('Année', default=CURRENT_YEAR)
    inscription_date = models.DateTimeField("Date d'inscription", auto_now_add=True)
    remark = models.TextField('Remarque', null=True, blank=True)
    is_active = models.BooleanField('Actif', default=True, null=False, blank=False)

    class Meta:
        verbose_name = "Elève demandeur d'aide"
        verbose_name_plural = "Elèves demandeurs d'aide"

    def __str__(self):
        return "{0} {1} eda pour {2}".format(self.student.name, self.student.vorname, self.discipline.name)

    def clean(self):
        count_same_edas = EDA.objects.filter(year=CURRENT_YEAR,
                                             student=self.student,
                                             discipline=self.discipline).count()
        if (count_same_edas != 0):
            raise ValidationError(
                "Cet EDA existe déjà !",
                code='eda_not_unique'
            )

    def get_absolute_url(self):
        return reverse('pymentorat:eda_update', kwargs={'id_eda': self.pk})

    def get_nb_contracts(self):
        nb = Contract.objects.filter(eda=self, end_date=None).count()
        return nb


class Contract(TimeStampedModel):
    eda = models.ForeignKey(EDA, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    contract_parent = models.ForeignKey('self', null=True, blank=True,  on_delete=models.CASCADE)
    year = models.PositiveIntegerField('Année', default=CURRENT_YEAR)
    begin_date = models.DateField('Date de début', auto_now_add=True)
    end_date = models.DateField('Date de fin', null=True, blank=True)
    remark = models.TextField('Remarque', null=True, blank=True)


    class Meta:
        verbose_name = "Contrat"
        verbose_name_plural = "Contrats"


    def __str__(self):
        return "Contrat {0} avec {1} en {2} - {3}".format(self.eda.student.name, self.mentor.student.name,
                                                          self.discipline.name, self.begin_date)


    def clean(self):
        # Don't allow to have a contract with an incorrect discipline
        if (self.eda.discipline != self.discipline) or (self.mentor.discipline != self.discipline):
            raise ValidationError(
                "La discipline de l'EDA, du mentor et du contrat ne correspondent pas.",
                code='invalid_discipline'
            )

        if (self.eda.year != self.year) or (self.mentor.year != self.year):
            raise ValidationError(
                "Année incohérente entre EDA, mentor et contrat.",
                code='invalid_year'
            )


    def get_absolute_url(self):
        return reverse('pymentorat:contract_update', kwargs={'id_contract': self.pk})

class Convocation(TimeStampedModel):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    date = models.DateField('Date de rendez-vous')
    time = models.TimeField('Heure du rendez-vous')
    place = models.CharField('Lieu de rendez-vous', default="devant la salle des maîtres", max_length=64)
    message = models.CharField('Message', null=True, blank=True, max_length=64)

    class Meta:
        verbose_name = "Convocation"
        verbose_name_plural = "Convocations"

    def __str__(self):
        return "Convocation {0} et {1} le {2} à {3} ".format(self.contract.eda.student.__str__(),
                                                      self.contract.mentor.student.__str__(),
                                                      self.date,
                                                      self.time)
