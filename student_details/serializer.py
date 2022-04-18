from rest_framework import serializers
from .models import Student,marks

class studentserializer(serializers.ModelSerializer):
    first_name=serializers.CharField(source='Roll_No.first_name')

    class Meta:
        model=marks
        fields = ('first_name','Roll_No','English','Tamil','maths')
