from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    Roll_No = models.IntegerField(primary_key=True)

class marks(models.Model):
    Roll_No = models.ForeignKey(Student,on_delete=models.CASCADE)
    English = models.IntegerField()
    Tamil = models.IntegerField()
    maths = models.IntegerField()


