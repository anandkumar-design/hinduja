from django.shortcuts import render
from student_details . models import Student,marks
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StudentName
from django.shortcuts import render, get_object_or_404
from rest_framework import generics,mixins,viewsets


# Non Primary key operation
class student_classbased(APIView):
    def get(self,request):
        data=Student.objects.all().values()
        return Response(data)

    def post(self,request):
        serializer = StudentName(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error)

#using Api view
class student_pk_operation(APIView):
    def get_data(self,request):
        print(request)
        try:
            return Student.objects.get(Roll_No=request.data['Roll_No'])
            print('f',Roll_no)
        except Student.DoesNotExist:
            raise Http404

    def get(self,request):
        data = self.get_data(request)
        serializer = StudentName(data)
        return Response(serializer.data)

    def put(self,request):
        user_data = self.get_data(request)
        serializer = StudentName(user_data,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self,request):
        user_data = self.get_data(request)
        user_data.delete()
        return Response("Deleted sucessfully")

# using mixins
class Studentlist(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentName

    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)


class StudentDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentName

    def get(self,Roll_No):
        return self.retrieve(Roll_No)

    def put(self,request):
        return self.update(request.data['Roll_No'])

    def delete(self,request):
        return self.destroy(request.data['Roll_No'])

#using Genrics views
class Studtent_list(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentName

class Studtent_Detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentName

#Using viewset
#Refer router in main urls
class Studentviewset(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentName
