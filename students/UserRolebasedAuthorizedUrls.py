from .import settings

uri=settings.urlmappingAuth

al_super_user={
    uri+"/student_details/Grade_of_student":False,
    uri+"/student_details/create_student":False,
    uri+"/student_details/sql_execution":False,
    uri+"/student_details/student_details":False,
    uri+"/student_details/upate_or_create_marks":False,
    uri+"/student_details/upate_by_subject":False,
    uri+"/student_details/marks_of_students":False,
    uri+"/student_details/show_student_withcontain":False,
    uri+"/student_details/check":False,
    uri+"/student_details/range_sql":False,
    uri+"/login/create_user":False,
    uri+"/login/hash_password":False,
}