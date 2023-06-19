from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *


urlpatterns = [

    path(r'userupload',UserUpload,name="UploadUsers"),

    path(r'assignments/',AssetAssignment,name="Assignments"),

    # path(r'asset_type_summary',graphing, name ="typesummary"),
]