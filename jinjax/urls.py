from django.urls import path
# from authentication.views import *
from django.contrib.auth import views as auth_views
from .views import *
urlpatterns = [
    path('<str:uname>/printprofile', printProfile, name='printprofile')
]
