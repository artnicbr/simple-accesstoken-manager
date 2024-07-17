from django.db import models
import datetime

class Token(models.Model):
    ID = models.BigAutoField(primary_key=True)
    TOKEN = models.CharField(max_length=256)
    UPTO = models.IntegerField(default=(datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat())
    IPADDR = models.CharField(max_length=16, default='127.0.0.1')
    SECRET_KEY = models.CharField(max_length=256, default=None, null=True)
    TIMESTAMP_INS = models.DateTimeField(default=datetime.datetime.now())
    TIMESTAMP_UPD = models.DateTimeField(null=True, default=None)

    class Meta:
        managed = True
        db_table = 'TM_TOKENS'

class User(models.Model):
    ID = models.BigAutoField(primary_key=True)
    LOGIN = models.CharField(max_length=256)
    PASS = models.CharField(max_length=256)
    EMAIL = models.CharField(max_length=512)
    TIMESTAMP_INS = models.DateTimeField(default=datetime.datetime.now())
    TIMESTAMP_UPD = models.DateTimeField(null=True, default=None)

    class Meta:
        managed = True
        db_table = 'TM_USERS'

class Log(models.Model):
    ID = models.BigAutoField(primary_key=True)
    ACTION = models.CharField(max_length=32)
    PAYLOAD = models.CharField(max_length=4096)
    RESPONSE = models.CharField(max_length=4096)
    TIMESTAMP_INS = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        managed = True
        db_table = 'TM_LOGS'