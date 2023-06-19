from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
import logging
from .models import AssetTb

from .views import asset_add

logging.basicConfig(filename="ActivityLog.log",level=logging.DEBUG, format='%(levelname)s:%(lineno)d:%(asctime)s:%(message)s')
def createAssetSignal(sender, instance, created, **kwargs):
    
    print(f"{instance} is as here")
    if created:
        
        AssetObj = AssetTb.objects.get(Ast_Tag_nbr=instance.Ast_Tag_nbr)
        
        if not AssetObj.Project_Name:
            AssetObj.Project_Name= asset_add.projectMatch(AssetObj.Project)
        else:
            print(f"{AssetObj} is Assigned to {AssetObj.Project_Name}")


post_save.connect(createAssetSignal, sender=AssetTb)
