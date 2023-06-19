from django.urls import path
from .views import *

urlpatterns = [
    
    path(r'disposal/', auctions, name="disposal"),
    path(r'auction/', auction_list, name="auction"),
    path('disposal/<str:pk>', dispose, name="dispose"),
    path('dynamicadd/', dynamicadd, name='dynamicadd'),
    path('requestapi/', testsDataAPI, name='TestApi'),
    path('deleteitem/', deleteItem, name='deleteitem'),
    path('updateitem/', updateItem, name='itemupdate'),
    path('createitem/', createItem, name='itemcreate'),
    path('itemadd/', dynadd, name='itemadd'),
    path('remove/<str:pk>', remove, name='remove'),
    path('auction-list/', asset_auction_list, name='auction-list'),
    path('auction/<str:pk>', asset_auction, name='asset_auction'),
    path('crapprovallist', crApprovalList, name='crapprovallist'),
    path('crapproval/<str:pk>', crApproval, name='crapproval'),
    path('cr-reject/<str:pk>', crReject, name='cr-rejection'),
    path(r'export-list', Export, name='export-list'),


]