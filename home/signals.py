from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import AssetTb, ChangeLog, staff, Assignment
from django.contrib.auth.models import Group


def user_profile(sender, instance, created, **kwargs):

    if created:
        group = Group.objects.get(name='staff')
        instance.groups.add(group)
        staff.objects.create(
            user=instance,
            Username=instance.username,
            Firstname = instance.first_name,
            Lastname = instance.last_name,
            email = instance.email,
            staff_status = True

        )
        print("Profile created")
    else:
        print("Not created")

post_save.connect(user_profile, sender=User)

# @receiver(post_save, sender = Assignment)
# def update_assetstatus(sender, instance, created, **kwargs):
#     if created == False:
#
#         AssetObj.Asset_Status = Status



# def changelog_signal(sender, instance, created, **kwargs):
    
#     ChangeLog.objects.create(
#         user = instance.user

#     )
        

# post_save.connect(changelog_signal, sender=AssetTb)