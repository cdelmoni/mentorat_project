from django_filters import FilterSet, OrderingFilter

from .models import Mentor, EDA, Student, Teacher

class MentorFilter(FilterSet):
    class Meta:
        model = Mentor
        fields = {
            'student__nom': ['contains'],
            'discipline': ['exact'],
            'year': ['exact']
        }


class EDAFilter(FilterSet):
    class Meta:
        model = EDA
        fields = {
            'student__nom': ['contains'],
            'discipline': ['exact'],
            'year': ['exact']
        }

class StudentFilter(FilterSet):
    class Meta:
        model = Student
        fields = {
            'nom': ['contains'],
            'prenom': ['contains'],
        }

class TeacherFilter(FilterSet):
    class Meta:
        model = Teacher
        fields = {
            'nom': ['contains'],
            'prenom': ['contains'],
        }
