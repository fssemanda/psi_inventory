from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(staff)
admin.site.register(AssetTb)
admin.site.register(AssetRequests)
admin.site.register(CsvUpload)
admin.site.register(Verified)
admin.site.register(Assignment)
admin.site.register(Ajaxsend)
admin.site.register(ChangeLog)
admin.site.register(Events)
admin.site.register(DeleteAssignment)
admin.site.register(Disposal)

