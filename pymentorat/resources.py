from import_export import resources
from .models import Discipline, Student, Teacher

class DisciplineResource(resources.ModelResource):
    class Meta:
        model = Discipline


class StudentResource(resources.ModelResource):
    class Meta:
        model = Student


class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher
