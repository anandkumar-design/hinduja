from django.http import HttpResponse,JsonResponse
from django.utils.deprecation import MiddlewareMixin
from login_app import views
from.import settings,unauthorizedUrls,UserRolebasedAuthorizedUrls
from student_details import commonresponse

# class JWTAuthenticationMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if not 'HTTP_TOKEN'  in request.META:
#             return JsonResponse("Token not availabel plese send token",safe=False)
        
        # check_token=views.decode_and_take_username(request)
        # if check_token==True:
        #     return request.POST.get('HTTP_TOKEN')
        # else:
        #     return JsonResponse("INVALID TOKEN",safe=False)

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        #Authoried url
        PATH_INFO = request.META['PATH_INFO']
        if PATH_INFO in UserRolebasedAuthorizedUrls.al_super_user:
            if not 'HTTP_TOKEN'  in request.META:
                return JsonResponse(commonresponse.Response.senderrorResponse(None,None,"Token not availabel plese send token"),safe=False)
            check_token=views.decode_and_take_username(request)
            if check_token==True:
                return request.POST
            else:
                return JsonResponse(commonresponse.Response.senderrorResponse(None,None,"INVALID TOKEN"),safe=False)
            
        #unauthoried url
        if PATH_INFO in unauthorizedUrls.urls:
            return request.POST
        else:
            return JsonResponse(commonresponse.Response.senderrorResponse(None,None,"INVALID URL"),safe=False)