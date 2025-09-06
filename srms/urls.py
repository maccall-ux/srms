from django.urls import path
from .views import *

app_name='srms'

urlpatterns = [
    path('',index,name='index'),
    path('admin_login/',admin_login,name='admin_login'),
    path('admin_dashboard/',admin_dashboard,name='admin_dashboard'),
    path('admin_logout/',admin_logout,name='admin_logout'),
    path('create_class/',create_class,name='create_class'),
    path('manage_classes/',manage_classes,name='manage_classes'),
    path('edit_class/<int:class_id>/',edit_class,name='edit_class'),
    path('create_subject/',create_subject,name='create_subject'),
    path('manage_subjects/',manage_subjects,name='manage_subjects'),
    path('edit_subject/<int:subject_id>/',edit_subject,name='edit_subject'),
    path('add_subject_combination/',add_subject_combination,name='add_subject_combination'),
    path('manage_subjects_combination/',manage_subjects_combination,name='manage_subjects_combination'),
    path('add_student/',add_student,name='add_student'),
    path('manage_students/',manage_students,name='manage_students'),
    path('edit_student/<int:student_id>/',edit_student,name='edit_student'),
    path('add_notice/',add_notice,name='add_notice'),
    path('manage_notice/',manage_notice,name='manage_notice'),
    path('add_result/',add_result,name='add_result'),
    path('get_students_subjects/',get_students_subjects,name='get_students_subjects'),
    path('manage_result/',manage_result,name='manage_result'),
    path('edit_result/<int:student_id>/',edit_result,name='edit_result'),
    path('change_password/',change_password,name='change_password'),
    path('search_result/',search_result,name='search_result'),
    path('check_result/',check_result,name='check_result'),
    path('notice_detail/<int:notice_id>/',notice_detail,name='notice_detail'),
]
