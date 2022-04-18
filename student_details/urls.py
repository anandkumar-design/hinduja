from django.urls import path
from .import views

urlpatterns = [
    path('create_student',views.create_student),
    path('sql_execution',views.sql_execution),
    path('student_details',views.student_details),
    path('upate_or_create_marks',views.upate_or_create_marks),
    path('upate_by_subject',views.upate_by_subject),
    path('marks_of_students',views.marks_of_students),
    path('Grade_of_student',views.Grade_of_student),
    path('show_student_withcontain',views.show_student_withcontain),
    path('check',views.check),
    path('range_sql',views.range_sql),
    path('Excel_download',views.Excel_download),
    path('student_bulkupload_template',views.student_bulkupload_template),
    path('student_bulkupload',views.student_bulkupload),
    path('read_excel',views.read_excel),
]
