from django.shortcuts import render
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
import datetime
from rest_framework.response import Response
import hashlib
import json

from ..models import User
from ..models import Token
from .Log import LogRecord

class UserView(APIView):
    def get(self, request, format="json"):
        resp = None
        try:
            resp = {"data": json.loads(serialize("json", User.objects.all(), fields=("LOGIN","EMAIL", "TIMESTAMP_INS", "TIMESTAMP_UPD")))}
                             
        except Exception as ex:
            LogRecord.save("Login", request.data, resp)
            resp = {
                "status": False,
                "code": "U01-026",
                "message": str(ex)
            }
            print(str(ex))

        return Response(resp)

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