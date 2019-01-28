from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Discipline, Student, Teacher, Mentor, EDA, Contract, Convocation
from .resources import StudentResource, TeacherResource, DisciplineResource

@admin.register(Discipline)
class DisciplineAdmin(ImportExportModelAdmin):
    resource_class = DisciplineResource

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource

@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    resource_class = TeacherResource

@admin.register(EDA)
class EDAAdmin(admin.ModelAdmin):
    pass

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    pass

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    pass

@admin.register(Convocation)
class ConvocationAdmin(admin.ModelAdmin):
    pass


