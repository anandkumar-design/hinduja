from .models import Student,marks

class DealerAppRepository():
    def CreateStudentBulkUpload(self,passData):
        print(passData)
        responseDict = {}
        data = Student.objects.create(
            first_name = passData['first_name'],
            last_name = passData['last_name']
        )
        responseDict['Updated_Remarks'] = "Students created successfully"
        return responseDict