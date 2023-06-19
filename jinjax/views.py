from django.shortcuts import render
from home.models import staff
from django.db.models import Sum,Count, Q
import jinja2
import pdfkit   

# Create your views here.

def printProfile(request,uname):
    staffobj = staff.objects.get(Username=uname)
    AssignedDevices = staffobj.assignment_set.all()
    
    FinanceManager = staff.objects.get(staffrole__icontains="Financial Accounts Manager")
    
    AssignedDevices_count = AssignedDevices.count()
    AssignedAssetsValue = AssignedDevices.aggregate(value=Sum("Ast_Tag_nbr_id__Item_Cost_USD"))
    
    myGroups = request.user.groups.all()[0].name    
   
    context={'staffobj':staffobj,'AssignedDevices':AssignedDevices, 
             'AssignedDevices_count':AssignedDevices_count,
              'AssignedAssetsValue':AssignedAssetsValue,"FinanceManager":FinanceManager,
             }
    
    template_loader= jinja2.FileSystemLoader('./jinjax/templates/jinjax/')
    template_env=jinja2.Environment(loader=template_loader)
    
    template=template_env.get_template("userDevicePrint.jinja")
    
    output_text = template.render(context)
    
    config=pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    
    pdfkit.from_string(output_text,f'{staffobj.Username}.pdf', configuration=config, css='https://attachments-psiug.s3.us-east-2.amazonaws.com/css/style.css')
    
    # return HttpResponse(request,"Printed")
    
    return render(request, 'jinjax/userDevicePrint.jinja', context)