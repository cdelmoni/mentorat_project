from django.urls import path, include
from django_filters.views import FilterView

from . import views
from .models import Contract

app_name='pymentorat'

urlpatterns = [
    # Login page
    path(
        'accounts/',
        include('django.contrib.auth.urls')
    ),
    # Home page
    path(
        '',
        views.index,
        name='index'
    ),
    # Student's pages
    path(
        'student/',
        views.student_filter_list,
        name='student_list'
    ),
    path(
        'student/<int:id_student>/',
        views.student_details,
        name='student_details'
    ),
    path(
        'student_update/<int:id_student>/',
        views.student_update,
        name='student_update'
    ),
    # Teacher's pages
    path(
        'teacher/',
        views.teacher_filter_list,
        name='teacher_list'
    ),
    path(
        'teacher_update/<int:id_teacher>/',
        views.teacher_update,
        name='teacher_update'
    ),
    # Mentor's pages
    path(
        'mentors/',
        views.mentor_filter_list,
        name='mentor_list'
    ),
    path(
        'mentor/<int:id_mentor>/',
        views.mentor_details,
        name='mentor_details'
    ),
    path(
        'mentor_create/',
        views.mentor_create,
        name='mentor_create'
    ),
    path(
        'mentor_create/<int:id_student>/',
        views.mentor_create_from_student,
        name='mentor_create_from_student'
    ),
    path(
        'mentor_update/<int:id_mentor>/',
        views.mentor_update,
        name='mentor_update')
    ,
    # EDA's pages
    path(
        'eda/',
        views.eda_filter_list,
        name='eda_list'
    ),
    path(
        'eda_nomentor/',
        views.eda_filter_nomentor_list,
        name='eda_nomentor_list'
    ),
    path(
        'eda/<int:id_eda>/',
        views.eda_details,
        name='eda_details'
    ),
    path(
        'eda_create/',
        views.eda_create,
        name='eda_create'
    ),
    path(
        'eda_create/<int:id_student>/',
        views.eda_create_from_student,
        name='eda_create_from_student'
    ),
    path(
        'eda_update/<int:id_eda>/',
        views.eda_update,
        name='eda_update'
    ),
    # Contract's pages
    path(
        'contract/',
        views.contract_filter_list,
        name='contract_list'
    ),
    path(
        'contract_create/<int:id_eda>/',
        views.contract_create_from_eda,
        name='contract_create'
    ),
    path(
        'contract_update/<int:id_contract>/',
        views.contract_update,
        name='contract_update'
    ),
    path(
        'contract_list/',
        views.SimpleContractListView.as_view(),
        name='contract_simple_list'
    ),
    path(
        'contract_print/<int:id_contract>/',
        views.contract_pdf,
        name='contract_pdf'
    ),
    path(
        'convocation_create/<int:id_contract>/',
        views.convocation_create_from_contract,
        name='convocation_create'
    ),
    path(
        'convocation_print/<int:id_convocation>/',
        views.convocation_pdf,
        name='convocation_pdf'
    ),
    # For Class Based Views
    # path(
    #     'contrat/',
    #     view=FilterView.as_view(model=Contract),
    #     name='contract_list'
    # ),
    # path(
    #     'contrat_create/',
    #     view=views.ContractCreateView.as_view(),
    #     name='contract_list'
    # ),
]
