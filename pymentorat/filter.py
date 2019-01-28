from django_filters import FilterSet, OrderingFilter, CharFilter, NumberFilter
from django.forms import IntegerField

from .models import Mentor, EDA, Student, Teacher, Contract
from .apps import CURRENT_YEAR

class MentorFilter(FilterSet):
    class Meta:
        model = Mentor
        fields = {
            'student__name': ['icontains'],
            'discipline': ['exact'],
            'year': ['exact']
        }


class EDAFilter(FilterSet):
    class Meta:
        model = EDA
        fields = {
            'student__name': ['icontains'],
            'discipline': ['exact'],
            'year': ['exact']
        }

class StudentFilter(FilterSet):
    class Meta:
        model = Student
        fields = {
            'name': ['icontains'],
            'vorname': ['icontains'],
        }

class TeacherFilter(FilterSet):
    class Meta:
        model = Teacher
        fields = {
            'name': ['icontains'],
            'vorname': ['icontains'],
        }


class ContractFilter(FilterSet):

    def __init__(self, *args, **kwargs):
        super(ContractFilter, self).__init__(*args, **kwargs)
        #self.filters["begin_date"].label = 'Toto'

    class Meta:
        model = Contract
        fields = {
            'eda__student__name': ['icontains'],
            'mentor__student__name': ['icontains'],
            'discipline': ['exact'],
            'begin_date': ['gt'],
            'end_date': ['lt'],
        }




