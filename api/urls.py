from django.urls import path
from home.models import *
from .views import * 

urlpatterns = [
    path('', apiOverview, name='apiview'),
    path('asset-list/', assetList, name='asset-list'),
    path('match-list/', MatchAsset, name='match-asset'),
    path('asset-create/', createAsset, name='asset-create'),
    path('asset-detail/<str:pk>', assetdetail, name='asset-detail'),
    path('asset-update/<str:pk>', assetUpdate, name='asset-update'),
    path('asset-delete/<str:pk>', assetDelete, name='asset-delete'),
    path('login-api', apiLogin, name='login-api'),
  #  path('verification/', verify, name='verification'),
    path('verification/<str:pk>', verifyAsset, name='vAsset'),
    path('assign/', assign, name='assign_api'),
    path('users_query/', UsersQuery, name='users_query'),
    path('users_listing/', UsersListing, name='users_listing'),
    
]


