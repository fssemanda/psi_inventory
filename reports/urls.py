from django.urls import path
from .views import *

urlpatterns = [

    path(r'reports/',reports,name='reports'),
    path(r'csvexport/',csvexport,name='export_csv'),
    path(r'excelexport/',pdfexport,name='export_pdf'),
    path(r'pdfexport/',excelexport,name='export_excel'),
    path(r'reports-all-inventory/',allAssetObjects,name='reports_all'),
    path(r'getasset', GetAsset, name="getasset"),
    path(r'depreciation/',Depreciation,name='depreciation'),
    # path(r'reports/',reports,name='reports'),
    # path(r'reports/',reports,name='reports'),

]