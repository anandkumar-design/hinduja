from .import repository
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from student_details import commonresponse
from .models import Student,marks
from .import connection
from .import constants
from .serializer import studentserializer
from django.db.models import Q,Sum,Max,F
from .decorators import allowed_states,check_user_exists,token_decorator
from.import commonresponse
import xlsxwriter
import io
import pandas as pd
import json
from students import AWSFilemanager
import datetime
import os


@api_view(['POST'])
def create_student(request):
    print(request.data)
    create_sutdent=Student.objects.create(
        first_name=request.data['first_name'],
        last_name=request.data['last_name']
    )
    if len(create_sutdent.first_name)>0:
        return JsonResponse("Created sucessfully",safe=False)
    else:
        return JsonResponse("unabel to create",safe=False)

@api_view(['GET'])
@token_decorator(['request'])
def sql_execution(request):
    query="select * from student_details_student"
    data_obj = connection.sql_execution()
    data = data_obj.my_custom_sql(query)
    if len(data)>0:
        return JsonResponse(data,safe=False)

@api_view(['GET']) 
def student_details(request):
    data=Student.objects.filter(Roll_No=request.GET['Roll_No']).values()
    return JsonResponse(list(data),safe=False)

@api_view(['POST'])
def upate_or_create_marks(request):
    if "Roll_No" not in request.data:
        return JsonResponse("Roll_no parameter is missing",safe=False) 
    check_roll_no=marks.objects.filter(Roll_No=request.data['Roll_No'])
    if check_roll_no.exists():
        update_marks=check_roll_no.update(
            English = request.data['English'],
            Tamil = request.data['Tamil'],
            maths = request.data['maths']
        )
        if (update_marks)>0:
            return JsonResponse("updated sucessfully",safe=False)
        else:
            return JsonResponse("uabel to update",safe=False)
    else:
        if not all(k in request.data for k in("Roll_No","English","Tamil","maths")):
            return JsonResponse("Some parameter is missing",safe=False) 
        roll_no=Student.objects.get(Roll_No=request.data['Roll_No'])
        create_Student=marks.objects.create(
            Roll_No = roll_no,
            English = request.data['English'],
            Tamil = request.data['Tamil'],
            maths = request.data['maths']
        )
        if (create_Student.id)>0:
            return JsonResponse("Created sucessfully",safe=False)
        else:
            return JsonResponse("uabel to Create",safe=False)


@api_view(['POST'])
def marks_of_students(request):
    if "Roll_No" not in request.data:
        return JsonResponse("Roll_no parameter is missing",safe=False)
    data=marks.objects.filter(Roll_No=request.data['Roll_No']).select_related('Roll_No')
    serialized_data = studentserializer(data,many=True)
    return JsonResponse(list(serialized_data.data),safe=False)

# @api_view(['POST'])
# def upate_by_subject(request):
#     if "Roll_No" not in request.data:
#         return JsonResponse("Roll_no parameter is missing",safe=False)
#     if not any(k in request.data for k in ('Tamil','English','maths')):
#         return JsonResponse("required not in request",safe=False)
#     data=marks.objects.filter(Roll_No=request.data['Roll_No'])
#     if data.exists():
#         for k,v in request.data.items():
#             if k==constants.marks[1]:
#                 data.update(Tamil=request.data['Tamil'])
#             if k==constants.marks[2]:
#                 data.update(English=request.data['English'])
#             if k==constants.marks[3]:
#                 data.update(maths=request.data['maths'])
#     if len(data)>0:
#         return JsonResponse("updated sucessfully",safe=False)

@api_view(['POST'])
def upate_by_subject(request):
    if "Roll_No" not in request.data:
        return JsonResponse("Roll_no parameter is missing",safe=False)
    try:
        data=marks.objects.get(Roll_No=request.data['Roll_No'])
        if constants.marks[1] in request.data and request.data["Tamil"] != None:
            data.Tamil = request.data['Tamil']
        data.save()
        if constants.marks[2] in request.data and  request.data["English"] != None:
            data.English = request.data['English']
        data.save()
        if constants.marks[3] in request.data and request.data["maths"] != None:
            data.maths = request.data['maths']
        data.save()
        return JsonResponse("updated sucessfully",safe=False)
    except Exception as e:
        print(e)
        return JsonResponse("Roll_no does not exists",safe=False)

@api_view(['POST'])
# @token_decorator(['request'])
def Grade_of_student(request):
    print(request.META)
    if "Roll_No" not in request.data:
        return JsonResponse("Roll_no parameter is missing",safe=False)
    data = marks.objects.annotate(the_sum=Sum(F("English")+F("Tamil")+F("maths"))).filter(Roll_No=request.data['Roll_No']).select_related('Roll_No')
    first_name=data[0].Roll_No.first_name
    last_name = data[0].Roll_No.last_name
    avg_of_student=(data[0].the_sum/3)
    if avg_of_student>90:
        return JsonResponse("{} {} Grade is A".format(first_name,last_name),safe=False)
    if avg_of_student>80 and avg_of_student<90:
        return JsonResponse("{} {} Grade is B".format(first_name,last_name),safe=False)
    if avg_of_student>70 and avg_of_student<80:
        return JsonResponse("{} {} Grade is C".format(first_name,last_name),safe=False)
    if avg_of_student>60 and avg_of_student<70:
        return JsonResponse("{} {} Grade is D".format(first_name,last_name),safe=False)
    if avg_of_student>50 and avg_of_student<60:
        return JsonResponse("{} {} Grade is E".format(first_name,last_name),safe=False)
    else:
        return JsonResponse("{} {} Grade is F".format(first_name,last_name),safe=False)

@api_view(['POST'])
def show_student_withcontain(request):
    data=Student.objects.filter(first_name__icontains=request.data['first_name']).values("first_name")
    return JsonResponse(list(data),safe=False)

@api_view(['POST'])
@allowed_states(['request'])
def check(request):
    if not all(k in request.data for k in ("from_range","to_range")):
        return JsonResponse("some parameter is missing",safe=False)
    if request.data['from_range'] in (0,"",):
        return JsonResponse("Invalid parameter",safe=False)
    create=Student.objects.filter(Roll_No__range=(request.data['from_range'],request.data['to_range'])).values()
    return JsonResponse(list(create),safe=False)

@api_view(['POST'])
def range_sql(request):
    print(request.META)
    from_rang=request.data["from"]
    to_range = request.data["to"]
    query = """SELECT * from student_details_student WHERE Roll_No BETWEEN {} AND {}""".format(from_rang,to_range)
    data=connection.sql_execution().my_custom_sql(query)
    if len(data)>0:
        return JsonResponse(commonresponse.Response.sendsuccessResponse(None,data,"Success"),safe=False)
    else:
        return JsonResponse(commonresponse.Response.senderrorResponse(None,None,"Error in getting data"),safe=False)

@api_view(['GET'])
def Excel_download(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('student_details')
    bold = workbook.add_format({'bold': True})
    data=Student.objects.all()
    # Start from the first cell. Rows and columns are zero indexed.
    row = 1
    col = 0
    for my_row in data:
        worksheet.write(row, col, my_row.first_name)
        worksheet.write(row, col+1, my_row.last_name)
        worksheet.write(row, col+2, my_row.Roll_No)
        row += 1
    # Write the title for every column in bold
    worksheet.write('A1', 'first_name', bold)
    worksheet.write('B1', 'last_name', bold)
    worksheet.write('C1', 'Roll_No', bold)
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=student_details.xlsx"
    return response

@api_view(['GET'])
def student_bulkupload_template(request):
    df1 = pd.DataFrame({'first_name':[], 'last_name':[]})
    writer = pd.ExcelWriter('student_bulkupload_template.xlsx', engine='xlsxwriter')
    df1.to_excel(writer, sheet_name='Sheet1', startrow=0, startcol=0, index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']
    header_format = workbook.add_format()
    header_format.set_bold()
    # Setting the column width
    worksheet.set_column('A:B', 20)
    # Write the column headers with the defined format.
    for col_num, value in enumerate(df1.columns.values):
        worksheet.write(0, col_num, value, header_format)
    worksheet.data_validation('A2:A1000', {'validate': 'custom', 'value': '=ISTEXT(A2)', 'input_title': 'Enter a non numeric value','error_message': 'Enter a string not a number'})
    worksheet.data_validation('B2:B1000', {'validate': 'custom', 'value': '=ISTEXT(B2)', 'input_title': 'Enter a non numeric value','error_message': 'Enter a string not a number'})
    writer.save()
    file = 'student_bulkupload_template.xlsx'
    print('f',file)
    if os.path.exists(file):
        with open(file, 'rb') as fh:
            if fh != None :
                response = HttpResponse(fh,content_type='application/force-download')
                response['Content-Disposition'] = 'attachment; filename=' + file
                response['status'] = 200
                response['file'] = fh
                response['message'] = 'success'
                # os.remove(file)
                return response
    else:
        return HttpResponse("File not found")

@api_view(['POST'])
def student_bulkupload(request):
    valid_extensions =  ['.xlsx', '.xls']  
    for key,values in request.FILES.items():
        fileType = AWSFilemanager.checkfiletype(values, valid_extensions)
        if fileType == "invalid format":
            return JsonResponse(commonresponse.Response.send_Invalid_request_response(None, [],'File format not supported', "Error"),safe = False)
        else:
            delarBulkUpload = repository.studentAppRepository.studentDelarBulkUpload(None,request)
            print('f',delarBulkUpload)
            return JsonResponse(commonresponse.Response.sendsuccessResponse(None, delarBulkUpload, "File uploaded sucessfully"), safe = False)

@api_view(['POST'])
def read_excel(request):
    table_list=[]
    new_table_list=[]
    date=""
    dft=pd.read_csv('C:/Users/17995/Desktop/New folder (4)/students//currenttablebackup20220307.csv.csv',usecols = ['OBU_ID','EVENT_UTC'])
    dft['EVENT_UTC'] = dft['EVENT_UTC'].astype(str).str[:-6]
    for filename in os.listdir('C:/Users/17995/Desktop/New folder (4)/students'):
        if filename.endswith('.csv'):
            table_list.append(pd.read_csv(filename,sep="|",on_bad_lines='skip'))
            new_table_list.append(filename.split(".")[0])
    print(new_table_list)
    for i in new_table_list[0]:
        if i.isnumeric():
            date+=i
    datetime_obj=datetime.datetime.strptime(date, "%Y%m%d").date()
    original_date = datetime_obj.strftime("%d-%m-%Y")
    print(original_date)
    dft['equal_to_ten'] = dft['OBU_ID'].apply(lambda x: 'True' if len(x) == 10 else 'False')
    dft['is_reporting'] =  dft['EVENT_UTC'].apply(lambda x: '1' if x == original_date else '0')
    subsetDataFrame = dft[dft['equal_to_ten'] == 'True']
    print(subsetDataFrame)
    json_data = subsetDataFrame.to_json(orient='records')
    return JsonResponse(commonresponse.Response.sendsuccessResponse(None, json.loads(json_data), "sucess"), safe = False)

