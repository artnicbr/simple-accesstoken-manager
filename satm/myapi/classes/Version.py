from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
import datetime
from rest_framework.response import Response

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