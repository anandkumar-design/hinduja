import jwt
import traceback

encoded='secret'

class jwt_():
    def encode_token(self,data):
        try:
            b={}
            encoded_jwt = jwt.encode({"value": data}, encoded, algorithm="HS256")
            b["jwt"]=encoded_jwt
            return b
        except Exception:
            print(traceback.format_exc())
            return 400

    def decode_the_data(self,request):
        try:
            if request.META['HTTP_TOKEN']!=None:
                decode_jwt = jwt.decode(request.META['HTTP_TOKEN'], key=encoded, algorithms="HS256")
                print("Hello")
                return decode_jwt
        except Exception as e:
            print(e)
            print('f',traceback.format_exc())
            return 400

    # def jwtTokenGenerator(self,data={}):
    #     try:
    #        encoded = base64.b64decode('YWxzbHRlbGVtYXRpY3NhdXRob3JpemF0aW9udG9rZW4=').decode("utf-8")
    #        jwt_token=jwt.encode({'sub1':data, 'sub':data[0]['loginid'].lower(),'exp':datetime.datetime.utcnow()++ datetime.timedelta(seconds=3600*24)},encoded, algorithm='HS256',).decode("utf-8")   
    #        return jwt_token
    #     except Exception:
    #         print(traceback.format_exc())
    #         return 400