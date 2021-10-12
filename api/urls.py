from django.urls import path
from home.models import *
from .views import *

urlpatterns = [
    path('', apiOverview, name='apiview'),
    path('asset-list/', assetList, name='asset-list'),
    path('asset-create/', createAsset, name='asset-create'),
    path('asset-detail/<str:pk>', assetdetail, name='asset-detail'),
    path('asset-update/<str:pk>', assetUpdate, name='asset-update'),
    path('asset-delete/<str:pk>', assetDelete, name='asset-delete'),
    path('verification/', verify, name='verification'),
    path('item-create/', create, name='item-create'),
    path('item-detail/<str:pk>', detail, name='item-detail'),
    path('item-update/<str:pk>', update, name='item-update'),
    path('item-delete/<str:pk>', delete, name='item-delete'),
]


