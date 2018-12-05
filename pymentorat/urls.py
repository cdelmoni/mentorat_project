from django.urls import path, include

from . import views

app_name='pymentorat'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('mentors/', views.mentor_filter_list, name='mentor_list'),
    path('mentor_create/', views.mentor_create, name='mentor_create'),
    path('mentor_update/<int:id_mentor>/', views.mentor_update, name='mentor_update'),
    path('eda/', views.eda_filter_list, name='eda_list'),
    path('eda_create/', views.eda_create, name='eda_create'),
    path('eda_update/<int:id_eda>/', views.eda_update, name='eda_update'),
    path('student/', views.student_filter_list, name='student_list'),
    path('student_update/<int:id_student>/', views.student_update, name='student_update'),
    path('teacher/', views.teacher_filter_list, name='teacher_list'),
    path('teacher_update/<int:id_teacher>/', views.teacher_update, name='teacher_update'),
]
