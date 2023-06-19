from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import agingGraph

from .views import *


urlpatterns = [

    path(r'search',csrf_exempt(search_assets),name="asset_search"),

    path(r'analytics/',graphview,name="Analytics"),

    path(r'asset_type_summary',graphing, name ="typesummary"),
    path(r'aging/',agingGraph, name ="aging"),
    path(r'depreciation_stats/',Dep, name ="depreciation_stats"),
]