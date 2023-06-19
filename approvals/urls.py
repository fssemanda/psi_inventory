from django.urls import path


from .views import *
#assetsview, AssetRequest, AssetRequestView, Reject, Fileupload, deleteItem,auctionList,asset_add, 
#editItem, assetAssignment, assign_asset,assign_device, pool_equip_request,pool_equip_request
urlpatterns = [
    path(r'dev-approvals/<str:pk>', dev_approvals,name="dev-approvals"),
    path('mod-approvals/<id>', mod_approvals,name="mod-approvals"),
    path('', approvalList,name="approval_list"), 
    
    

]
