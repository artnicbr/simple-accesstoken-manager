from django.urls import re_path
from .views import VersionView
from .views import UserView
from .views import TokenView

urlpatterns = [
    re_path(r'^version/$', VersionView.as_view()),
    re_path(r'^auth/$', UserView.as_view()),
    re_path(r'^validate/$', TokenView.as_view()),
]