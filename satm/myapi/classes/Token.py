from django.shortcuts import render
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
import datetime
from rest_framework.response import Response

from ..models import Token
from .Log import LogRecord

class TokenView(APIView):
    def post(self, request, format=None):
        try:
            lastToken = Token.objects.filter(TOKEN=request.data['token']).order_by('-UPTO').first()
            resp = None

            if lastToken != None:
                if request.data['secret-key'] == lastToken.SECRET_KEY:
                    upto = lastToken.UPTO
                    if upto >= int(datetime.datetime.now().timestamp()):
                        lastToken.UPTO = (datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp()
                        lastToken.save()
                        resp = {"valid": True}
                    else:
                        resp = {"valid": False, "code": "0001-72", "message": "Expired token"}
                
                else:
                    resp = {"valid": False, "code": "0002-75", "message": "Invalid secret key"}
            else:
                resp = {"valid": False, "code": "0003-77", "message": "Token not found"}
            
            LogRecord.save("Authentication", request.data, resp)
            return Response(resp)
        
        except Exception as ex:
            LogRecord.save("Authentication", request.data, resp)
            print(str(ex))
            raise