from student_details . models import Student,marks
from rest_framework import serializers


class StudentName(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields ="__all__"
