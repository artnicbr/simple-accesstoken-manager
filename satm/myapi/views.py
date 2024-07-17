from django.shortcuts import render

#MODELS
from .models import User
from .models import Token

# Imported Views
from .classes.Version import VersionView
from .classes.User import UserView
from .classes.Token import TokenView
from .classes.Admin import AdminView

# Static classes
from .classes.Log import LogRecord