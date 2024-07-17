from django.shortcuts import render
import json
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
import datetime
from rest_framework.response import Response
import hashlib

#MODELS
from .models import User
from .models import Token
from .Log import LogRecord

# Create your views here.
class VersionView(APIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]    
    curdate = (datetime.datetime.now() + datetime.timedelta(hours=-3)).strftime("%d/%m/%Y %H:%M:%S")

    def post(self, request, format='json'):
        resp = { 
                "version": "0.0.3",
                "date": self.curdate
            }
            
        return Response(resp)
    
    def get(self, request, format='html'):
        
        resp = { 
            'info':{
                'version': '0.0.3',
                'date': self.curdate
            }
        }

        return Response(resp, template_name = 'version.html')

class UserView(APIView):
    def post(self, request, format=None):
        try:
            user = User.objects.filter(
                LOGIN=request.data["username"],
                PASS=request.data["password"])

            username = request.data["username"][:32]
            password = request.data["password"][32:]

            resp = None

            if len(user) == 1:
                t = Token()
                t.TOKEN = hashlib.sha256(str(username + password).encode('utf-8')).hexdigest()
                t.UPTO = (datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp()
                t.SECRET_KEY = hashlib.sha256(str(datetime.datetime.now().timestamp()).encode('utf-8')).hexdigest()
                t.save()

                resp = {
                    "status": True,
                    "secret-key": t.SECRET_KEY
                }
            
            else:
                resp = {}

            LogRecord.save("Login", request.data, resp)
            return Response(resp)
        
        except Exception as ex:
            LogRecord.save("Login", request.data, resp)
            print(str(ex))
            raise

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