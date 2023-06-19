from django.urls import path
from .views import *

urlpatterns = [
    path('qrcodegen/', QrGen,name="qrgen"),
    path('bulk/', QrBulk,name="bulk"),

    ]