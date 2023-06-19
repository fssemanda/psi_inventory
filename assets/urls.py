from django.urls import path
from home.logindecorators import allowed_users, unauthorizedUser_func
from home.views import stockView
from .views import *
from django.contrib.auth.decorators import login_required
#assetsview, AssetRequest, AssetRequestView, Reject, Fileupload, deleteItem,auctionList,asset_add, 
#editItem, assetAssignment, assign_asset,assign_device, pool_equip_request,pool_equip_request
urlpatterns = [
    path('assets/', assetsview,name="view_assets"),
    path(r'assetRequest/', AssetRequest,name="AssetRQ"),
    path(r'requestView/<str:pk>', AssetRequestView,name="RQView"),
    path(r'reject/<str:pk>',Reject,name="reject"),
    path(r'upload/',Fileupload,name="upload"),
    path('detail/<pk>',stockView,name='assetdetails'),
    path(r'deleteitem/<str:pk>',deleteItem,name='delete-item'),
    path(r'edit-item/<str:pk>',editItem,name='edit_item'),
    path(r'auctionlist',auctionList,name='auction-list'),
    path(r'addasset',asset_add,name='add-asset'),
    path(r'assignasset/',assetAssignment,name='assetAssignment'),
    path(r'assign/<str:pk>',assign_asset,name='assign'),
    path(r'assigned/<str:pk>',assign_device,name='assigned'),
    path(r'pooldevice/<str:pk>',pool_equip_request,name='poolassignment'),
    path(r'withdraw-item/<str:pk>',RemoveAssignment,name='withdraw-item'),
    path(r'withdraw-list',withdrawList,name='withdraw-list'),
    path(r'withdraw/<str:pk>',withdraw,name='withdraw'),
    path(r'get_asset/',get_device,name='get_asset'),
    path(r'accept_asset/',Acceptance,name='accept_asset'),
    # path(r'search',csrf_exempt(search_assets),name="asset_search"),
    path(r'handover/',csrf_exempt(handover),name='handover'),
     path(r'requestapproval/<pk>/<uidb64>/<token>',  login_required(login_url="login")(allowed_users(['Accountant-AP','Asset Manager','Systems Administrator','Admin']) ( ApproveRequest.as_view())),name='approve-reject'),
    path(r'asset-request/<str:pk>',SendApprovalRequest.as_view(),name="approval-request"),
    
    

]
