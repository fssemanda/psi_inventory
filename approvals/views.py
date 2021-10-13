import json

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail.message import EmailMessage
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.urls import reverse

from assets.forms import AccountantApprovalform, ChangeLogForm, SupervisorApprovalForm
from home.logindecorators import allowed_users
from datetime import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render, redirect
from home.models import AssetRequests, AssetTb, ChangeLog, staff
from psi_inventory import settings
import sys
from assets.views import myconverter


import threading

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)
# Create your views here.


@login_required(login_url='login')
@allowed_users(allowed_roles=['approver', 'Supervisor', 'Finance', 'Admin', 'IT'])


def approvalList(request):

    ModObjects = ChangeLog.objects.all().order_by('LogDate')

    paginator = Paginator(ModObjects, 12)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    # Need to convert date object in returned values as a serializable value othwerwise get error Json cannot serialize date

    qs_json = json.dumps(list(AssetTb.objects.values()), default=myconverter)

    context = {'ModObjects': ModObjects, 'qs_json': qs_json, 'page_obj': page_obj}


    return render(request, 'base/approvals.html',context)

def mod_approvals(request, id):

    ModObject = ChangeLog.objects.get(id=id)
    staffobj = staff.objects.get(Username=request.user)
    OriginalObject = AssetTb.objects.get(Ast_Tag_nbr=ModObject.AstTagnbr)

    print(f'staffObj represents {ModObject.Requester.staff.Firstname}')

    ApprovalObjectForm = ChangeLogForm(instance=ModObject)

    if request.method == 'POST':
        print("Passed")
        
        ApprovalObjectForm = ChangeLogForm(request.POST, instance=ModObject)
        
        print(request.POST.get('LogDate'))

        domain = get_current_site(request).domain

        link = reverse('mod-approvals', kwargs = {'id':ModObject.id})

        full_link = 'http://'+domain+link

        if ApprovalObjectForm.is_valid():

                print("Form is valid")
            
                ApprovalObjectForm.save()
            
                ApprovalStatus = ApprovalObjectForm.cleaned_data.get('FAMApproval')
                
                if ApprovalStatus != 'Approved':

                    try:

                        print("In mail")

                        domain = get_current_site(request).domain

                        link = reverse('mod-approvals', kwargs = {'id':ModObject.id})
        
                        print(link)
                        full_link = 'http://'+domain+link

                        print(full_link)

                        Approvers = staff.objects.filter(staffrole='Finance')
                        Emails = ['macho.francis2@gmail.com']
                        for user in Approvers:
                            Emails.append(user.email)

                            print(Emails)

                            email_subject = f'Request for Modification of {ModObject.AstTagnbr} Rejected'
                            email_body = f'Dear {ModObject.Requester.staff.Firstname},\n\n {request.user.first_name} has rejected your  to modify {ModObject.AstTagnbr}. \n \n Click on Link below to view request\n'+full_link


                            email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[user.email,])
                            EmailThread(email).start()
                                
                        

                    except RuntimeError as e:
                        print(e, file=sys.stderr)
                else:
                    Approvers = staff.objects.filter(staffrole='Finance')
                       
                    for user in Approvers:

                        email_subject = f'Request for Modification of {ModObject.AstTagnbr} Approved'
                        email_body = f'Dear {ModObject.Requester.staff.Firstname},\n\n {request.user.first_name} has Approved your  to modify {ModObject.AstTagnbr}.'
                        ' \n \n Click on Link below to view request\n'+full_link+'\n \n Changes should reflect Immediatelty'



                        email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[user.email,])
                        EmailThread(email).start()
        else:
            print("Form invalid")

    context = {'ModObject': ModObject, 'ApprovalObjectForm': ApprovalObjectForm, 'staffobj':staffobj, 'OriginalObject':OriginalObject}
    return render(request, "base/approvaldetails.html", context)

def dev_approvals(request):
    pass