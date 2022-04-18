import pandas as pd
from .import service


class studentAppRepository():
    def studentDelarBulkUpload(self,passData):
        for key, values in passData.FILES.items():
            excel_data_df = pd.read_excel(values, sheet_name='Sheet1')
            json_str = excel_data_df.to_json(orient='records')
            # print('json_str',json_str)
            df1 = pd.DataFrame(excel_data_df, columns =[
            'first_name',
            'last_name'
            ])
            removeNone = df1.dropna(how='all')
            replaceNone = removeNone.fillna('None')
            DelarData = replaceNone.reset_index().to_dict('records')
        if DelarData !=[]:
            for delardata in DelarData:
                dictData = {}
                Remarks = ""
                response ={}
                if delardata !=[]:
                    dictData['first_name']=delardata['first_name']
                    dictData['last_name']=delardata['last_name']
                    response=service.DealerAppRepository.CreateStudentBulkUpload(None,dictData)
                return response


