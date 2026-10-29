# File：cors.py.py
# Author：信思智学
# Date ：2025/8/15 15:17
# Info：
# from django.utils.deprecation import MiddlewareMixin
# from django.utils.deprecation import MiddlewareMixin
# class CorsMiddleWare(MiddlewareMixin):
#     def process_response(self,request,response):
#         # options请求就是非简单请求的预检请求
#         if request.method=="OPTIONS":
#             response["Access-Control-Allow-Headers"]='Content-Type, *'  # 注意：通常不建议使用 '*'，应该明确列出允许的头
#             response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
#             response['Access-Control-Max-Age'] = 86400  # 预检请求的缓存时间（秒）
#         response["Access-Control-Allow-Origin"] = "*" # 注意：'*' 允许所有来源，但出于安全考虑，建议使用具体的来源
#         return response
#
# app/cors.py
class CorsMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # 统一给所有响应添加跨域头
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        response["Access-Control-Max-Age"] = "86400"
        return response