from django.contrib import admin
from .models import Discipline, Student, Teacher, Mentor, EDA, Contract, Convocation

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass

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
