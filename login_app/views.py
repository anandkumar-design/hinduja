from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from student_details import commonresponse
from login_app import repository
from .models import Failed_count
from student_details import connection
import datetime
from student_details import jwt_token_genration
from django.db.models import Q
import datetime
from .import repository

@api_view(['POST'])
def create_user(request):
    data=User.objects.create(
        password=request.data['password'],
        last_login = datetime.datetime.now(),
        is_superuser = request.data['is_superuser'],
        username = request.data['username'],
        last_name = request.data['last_name'],
        email = request.data['email'],
        is_staff = request.data['is_staff'],
        date_joined = datetime.datetime.now(),
        first_name = request.data['first_name']
    )
    if (data.id)>0:
        return JsonResponse("Created sucessfully",safe=False)
    else:
        return JsonResponse("unabel to create",safe=False)

@api_view(['GET'])
def hash_password(request):
    for user in User.objects.all():
        user.set_password(user.password)
        user.save()
    return JsonResponse("password hashed sucessfully",safe=False) 

# @api_view(['POST'])
def Genrate_jwt_token_with_info(user_name):
    new_data=[]
    query = """select * from auth_user where username = "{}" """.format(user_name)
    print(query)
    data_obj=connection.sql_execution()
    data=data_obj.my_custom_sql(query)
    new_data.append(data)
    if len(data)>0:
        ecoded_data_obj=jwt_token_genration.jwt_()
        encode_data = ecoded_data_obj.encode_token(data)
        new_data.append(encode_data)
        return new_data
        

def decode_and_take_username(request):
    decode_obj = jwt_token_genration.jwt_()
    decode_data = decode_obj.decode_the_data(request)
    print('decode_data',decode_data)
    try:
        user_name=decode_data['value'][0]['username']
        password = decode_data['value'][0]['password']
        data=User.objects.filter(Q(username__iexact=user_name) & Q(password__iexact=password))
        print('m',data)
        if data.exists():
            return True
    except:
        return False


@api_view(['POST'])
def login_auth(request):
    print(request)
    user_name = request.data["username"]
    print(user_name)
    password= request.data["password"]
    if str(user_name).endswith(".com"):
        check_mail = User.objects.filter(email=request.data['username']).count()
        if (check_mail)>1:
            return JsonResponse(commonresponse.Response.senderrorResponse(None,None,"This user is duplicated please check"),safe=False)
        else:
            check_data = User.objects.filter(email=request.data['username']).values()
            user_name=check_data[0]['username']
    check_user = User.objects.filter(Q(username__iexact=user_name))
    if not check_user.exists():
        return JsonResponse(commonresponse.Response.senderrorResponse(None,None,"User does not exists please create user"),safe=False)
    check_admin_login = User.objects.filter(username__iexact=user_name).values_list('is_superuser')
    if check_admin_login[0][0]==0:
        return JsonResponse(commonresponse.Response.senderrorResponse(None,None,"This login is only for super user"),safe=False)
    check_data = User.objects.filter(username__iexact=user_name).values_list("password","id")
    user_id = check_data[0][1]
    if(repository.check_count().check_failure_count(user_id)==True):
        return JsonResponse(commonresponse.Response.senderrorResponse(None,None,"User locked please contact admin"),safe=False)
    if password!=check_data[0][0]:
        update_failed_count = repository.check_count().update_failed_count(user_id)
        if (update_failed_count)>0:
            return JsonResponse(commonresponse.Response.senderrorResponse(None,None,"Invalid password please try again"),safe=False)
    if password==check_data[0][0]:
        reset_count=Failed_count.objects.filter(username_id=user_id)
        if reset_count.exists():
            data = reset_count.update(
                count=0,
                updated_timestamp=datetime.datetime.now()
            )
    user_info=Genrate_jwt_token_with_info(user_name)
    return JsonResponse(commonresponse.Response.sendsuccessResponse(None,user_info,"Success"),safe=False)


@api_view(['POST'])
def unlock_user(request):
    user_name = request.data['username']
    data=User.objects.filter(username=user_name).values_list('id')
    id=data[0][0]
    data1=Failed_count.objects.filter(username_id=id).update(
        count = 0,
        updated_timestamp = datetime.datetime.now()
    )
    if (data1)>0:
        return JsonResponse(commonresponse.Response.sendsuccessResponse(None,None,"Reset Success"),safe=False)