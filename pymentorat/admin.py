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
    list_display = [
        'name',
        'vorname',
        'id_OD'
    ]
    search_fields = ('name', 'vorname', 'id_OD')
    ordering = ['name']

@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    resource_class = TeacherResource
    list_display = [
        'name',
        'vorname',
        'id_OD'
    ]
    search_fields = ('name', 'vorname', 'id_OD')
    ordering = ['name']

@admin.register(EDA)
class EDAAdmin(admin.ModelAdmin):
    list_display = [
        'student',
        'discipline',
        'inscription_date',
        'is_active',
    ]
    list_filter = (
        'discipline',
        'inscription_date',
        'is_active',
    )
    fields = [
        'student',
        'discipline',
        'inscription_date',
        'is_active',
    ]
    search_fields = ('student__name','student__vorname',)
    ordering = ['inscription_date',]

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = [
        'student',
        'discipline',
        'inscription_date',
        'is_active',
    ]
    list_filter = (
        'discipline',
        'inscription_date',
        'is_active',
    )
    search_fields = ('student__name', 'student__vorname',)
    ordering = ['inscription_date', ]

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    pass

@admin.register(Convocation)
class ConvocationAdmin(admin.ModelAdmin):
    pass


