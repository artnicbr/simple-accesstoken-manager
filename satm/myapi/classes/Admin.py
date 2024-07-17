from django.shortcuts import render
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .Log import LogRecord
from ..models import User
import hashlib

class AdminView(APIView):
    def put(self, request, format=None):

        resp = None

        try:
            username = request.data["user-data"]["login-raw"]
            password = request.data["user-data"]["password-raw"]
            email = request.data["user-data"]["email"]

            u = User()
            u.LOGIN = hashlib.sha256(username.encode('utf-8')).hexdigest()
            u.PASS = hashlib.sha256(password.encode('utf-8')).hexdigest()
            u.EMAIL = email

            u.save()

            generated_token = hashlib.sha256((username[:32] + password[32:]).encode('utf-8')).hexdigest()
            resp = {
                "status": True,
                "token": generated_token,
                "ID": u.ID
            }

        except Exception as ex:
            resp = {
                "status": False,
                "error": str(ex)
            }

            LogRecord.save("Register", request.data, resp)
            print(str(ex))
            raise
        return Response(resp)