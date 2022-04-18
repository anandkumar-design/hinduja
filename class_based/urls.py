from django.urls import path,include
from class_based import views
from class_based.views import student_classbased,student_pk_operation,Studentlist,StudentDetail,Studtent_list,Studtent_Detail
from rest_framework.routers import DefaultRouter
from student_details . models import Student

# router = DefaultRouter
# router.register('Student',views.Studentviewset)
# urlpatterns=[
#     path('',include(router.urls))
# ]

urlpatterns = [
    path('student_classbased/',student_classbased.as_view()),
    path('student_pk_operation/',student_pk_operation.as_view()),
    path('Studentlist/',Studentlist.as_view()),
    path('StudentDetail/<int:Roll_No>',StudentDetail.as_view()),
    path('Studtent_list/',Studtent_list.as_view()),
    # path('Studtent_Detail/',Studtent_Detail.as_view()),
    path('<int:Student_Roll_No>/<int:pk>/',Studtent_Detail.as_view(),name='Studtent_Detail'),
]

