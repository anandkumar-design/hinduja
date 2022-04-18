class Response():
    SUCCESS = "Success"
    FAILURE = "Failure"
    ERROR_INVALID_USER_ID = "Invalid User id"
    ERROR_INVALID_USER_ROLE = "Invalid User role"
    BAD_REQUEST = "Some paramters are missing or invalid request"
    def sendsuccessResponse(self, data, message):
        responsedata={}
        responsedata['data']=data
        responsedata['message']=message
        responsedata['statuscode']=200
        if(data==None or data == []):
           responsedata['statuscode']=204
        return responsedata
    def senderrorResponse(self ,data,message):
        responsedata={}
        responsedata['data']=data
        responsedata['message']=message
        responsedata['statuscode']=400
        return responsedata
    def send_Invalid_request_response(self , data, message, error):
        responsedata={}
        responsedata['data']=data
        responsedata['message']=message
        responsedata['error']= error
        responsedata['statuscode']=400
        return responsedata
    def sendfailureResponse(self ,data,message):
        responsedata={}
        responsedata['data']=data
        responsedata['message']=message
        responsedata['statuscode']=500
        return responsedata
    
    def sendredirectionResponse(self ,data,message):
        responsedata={}
        responsedata['data']=data
        responsedata['message']=message
        responsedata['statuscode']=302
        return responsedata
    
    def sendmessageresponse(self,data,message,contact):
        responsedata={}
        responsedata['data']=data
        responsedata['message']=message
        responsedata['contact']= contact
        responsedata['statuscode']=204
        return responsedata