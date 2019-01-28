from django_filters import FilterSet

from .models import Mentor, EDA, Student, Teacher, Contract


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


class MentorFilter(FilterSet):
    class Meta:
        model = Mentor
        fields = {
            'student__name': ['icontains'],
            'discipline': ['exact']
        }


class EDAFilter(FilterSet):
    class Meta:
        model = EDA
        fields = {
            'student__name': ['icontains'],
            'discipline': ['exact']
        }


class ContractFilter(FilterSet):

    def __init__(self, *args, **kwargs):
        super(ContractFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = Contract
        fields = {
            'eda__student__name': ['icontains'],
            'mentor__student__name': ['icontains'],
            'discipline': ['exact'],
            'begin_date': ['gt'],
            'end_date': ['lt'],
        }
