import csv
import datetime
import json
import threading
import logging
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from home.logindecorators import *
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives,EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models.query import QuerySet
from django.forms.models import inlineformset_factory, modelform_factory
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory, modelform_factory
# Create your views here.
from django.template.loader import get_template
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from psi_inventory import settings
from .forms import AddAssetForm, Assetwithdrawform, AssetRQForm, FileUploadForm, AssignmentForm, DeleteAssignment
from home.models import *
from django.views import View

from django.views.generic import ListView
from django.core.paginator import Paginator
ExcludedTypes = [
                    "AIR CONDITIONER",
                    "VEHICLE",
                     "product display Shelf",
                     "Cushined Sofa chairs-",
                     "FIRE EXTINGUISHER",
                     "FIRE EXTINGUISHER",
                     "Shelf",
                     "SOFA SET",
                     "BOOKSHELF",
                     "DRAWER",
                     "DRAWERS",
                     "TRUSHING MACHINE",
                     "FILING CABIN",
                     "INVERTER",
                     "FIREWALL",
                     "FILING CABINET",
                     "SAFE",
                     "FAN",
                     "MICROWAVE",
                     "WATER DISPENSER",
                     "SWITCHES",
                     "REFRIGERATOR",
                     "VEHICLE",
                     "TV",
                     "SERVER",
                     "TABLE",
                     "TENT",
                     "CHAIR",
                     "HIGH BACK ROTATING CHAIR",
                     "LOW BACK ROTATING CHAIR",
                     "SHREDDER",
                     "",
                     ]


logging.basicConfig(filename="ActivityLog.log",level=logging.DEBUG, format='%(levelname)s:%(lineno)d:%(asctime)s:%(message)s')

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def projectMatch(code):
                    if code == "351CCP1" or code =="351CCP2":
                        return "Common Cost"
                    elif code == "456531" or code =="640051" or code =="630051" or code =="6002" or code =="456951" or code =="610051" or code=="4686UG" or code=="4686SBU":
                        return "WHP"
                    elif code == "4254":
                        return "PFIZER"  
                    elif code == "4499":
                        return "MaNe"
                    elif code == "3901":
                        return "MUM"
                    elif code == "P2490" or code =="P3111" or code =="P51PPI":
                        return "PROGRAM INCOME"
                    elif code == "CMS":
                        return "CMS PROJECT"
                    elif code == "4115WSHTUNZA":
                        return "TUNZA"
                    elif code == "4482UG":
                        return "CM4FP"
                    elif code == "4562PERM" or code =="4562PM" or code =="4562SA":
                        return "BERGSTROM FOUNDATION"
                    elif code == "DISC":
                        return "4560UG"
                    elif code == "4677UGANDA":
                        return "HIVST"
                    elif code == "3646Y":
                        return "CDC"
                    elif code == "3706SUB":
                        return "CSF"
                    elif code == "4593NPIPSIUG":
                        return "NPI"
                    elif code == "4605":
                        return
                    elif code == "4625":
                        return "SELFCARE TBG"
                    elif code == "4666UG":
                        return "COVID-19"
                    elif code == "4726":
                        return "DKT"
                    elif code == "4447UG":
                        return "LEAP PROJECT"
                    elif code == "4588CVDUG":
                        return "CITY TO CITY"
                    else:
                        print("Failure to add run function project match")



@login_required(login_url='login')
# @allowed_users(allowed_roles=['Systems Administrator'])
@allowed_users(allowed_roles=['Admin', 'Finance', 'IT','Accountant','Assistant Accountant-Treasury'])
def assetsview(request):
    myassets = AssetTb.objects.all().order_by('-PurchaseDate', '-Ast_Tag_nbr')
    #Changing Asset Availability to Not-Assigned for all Assets

    # for item in myassets:
    #     item.Availability = "Not Assigned"
    #     item.save()
    # # employee = staff.objects.get(Username="macho.francis")
    count = []
    start = 0
    for tag in myassets:
        if tag.Item_Cost_USD > 950:
            start += 1
            count.append(1)
    above = sum(count)

    paginator = Paginator(myassets, 12)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    # Need to convert date object in returned values as a serializable value othwerwise get error Json cannot serialize date

    qs_json = json.dumps(list(AssetTb.objects.values()), default=myconverter)

    context = {'assets': myassets, 'above': above, 'qs_json': qs_json, 'page_obj': page_obj}

    # employee = staff.objects.all()
    #
    # qs_json = json.dumps(list(staff.objects.values()),default=myconverter)
    # context = {'employee':employee , 'qs_json': qs_json}
    Events.objects.create(

    EventType = "Assets Listing Page Access",
    EventSummary = f"{datetime.datetime.now()} : User {request.user} has accessed the assets listing page"
    )

    return render(request, "base/listing.html", context)


@login_required(login_url='login')
def AssetRequest(request):

    pooleddevices = AssetTb.objects.filter(Availability="Available").exclude(Asset_Type__in=ExcludedTypes)

    # requestFormSet = inlineformset_factory(staff, AssetRequest, fields=(
        # can_delete = False)
    requester = request.user.staff.Username
    print(requester)
    staffobj = staff.objects.get(Username=requester)
    myform = AssetRQForm(initial={'Username': staffobj})
   
    #Need to find a way of having the form have not displaying the Username so that form can be saved and username 
    #picked automatically
    domain = get_current_site(request).domain
                        # print(domain)

    link = reverse('homepage')
    print(link)
    full_link = 'https://'+domain+link
    if request.method == 'POST':
        #myform = RqForm(request.POST, instance=staffobj)
        myform = AssetRQForm(request.POST,instance=request.user)
       # print(myform)
        if myform.is_valid():
            
            #myform.Username = requester
           #print(myform.Username)
            deviceType = myform.cleaned_data.get("Device_Type")
            username = myform.cleaned_data.get("Username")
            myform.cleaned_data["Username"] = staffobj
            print(myform.cleaned_data)
            print(username)
            try:
                print("saving form")
                a = AssetRequests.objects.create(
                    Device_Type = myform.cleaned_data.get("Device_Type"),
                    Reason = myform.cleaned_data.get("Reason"),
                    Username = myform.cleaned_data.get("Username"),
                )
                if a:
                    Events.objects.create(

            EventType = "Asset Request",
            EventSummary = f"{datetime.datetime.now()} : User {request.user} requested for a pool device {deviceType}"
            )       
                    # Approvers = staff.objects.filter(staffrole='Admin')    
                    Approvers = staff.objects.filter(Username='fssemanda')    
                    
                    Emails = []
                    for user in Approvers:
                        Emails.append(user.email)
                        print(user.staffrole)
                        link = reverse('homepage')
                        link2 = 'https://'+domain+link
                        print(link2)
                        email_subject = f'{request.user.staff.Firstname} {request.user.staff.Lastname} is requesting for a {deviceType}'
                        email_body = f'Dear {user.Firstname},\n\n {request.user.staff.Firstname} {request.user.staff.Lastname} is requesting\
                            for a {deviceType}. \
                        \n\nClick on Link below to view request\n'+full_link
                            

                        email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[user.email,])
                        EmailThread(email).start()
                    messages.info(request,'Application for a permanent work tool submitted')
                    myform = AssetRQForm(initial={'Username': staffobj})
                else:
                    print("Failed to save")
            except Exception as e:
                print(e)
            

            #return redirect('/')
        else:
            print(f'Form has errors {myform.errors.as_text}')
            


    context = {'myform': myform, "pooleddevices":pooleddevices}

    return render(request, "base/Asset_Request.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Finance', 'IT','Assistant Accountant-Treasury'])
def asset_add(request):
    AssetObj = AssetTb.objects.all()
    
    response = ""

    myform = AddAssetForm()

    if request.method == 'POST':

        myform = AddAssetForm(request.POST)
        
        Ast_Tag_number =myform.data.get('Ast_Tag_nbr')

        print(Ast_Tag_number)
        
        if AssetTb.objects.filter(Ast_Tag_nbr=Ast_Tag_number).count() > 0:
                messages.warning(request, f'Asset {Ast_Tag_number} already exists in database')
        else:
            if myform.is_valid():
                Ast_Tag_number = myform.cleaned_data.get('Ast_Tag_nbr')
                Serial_Number = myform.cleaned_data.get('Serial_No')
                #Lawson_Asset_Number = myform.cleaned_data.get('Lawson_Asset_No')
                Asset_description = myform.cleaned_data.get('Ast_description')
                UGX = myform.cleaned_data.get('Item_Cost_UGX')
                USD = myform.cleaned_data.get('Item_Cost_USD')
                Type = myform.cleaned_data.get('Asset_Type')
                Model_Number = myform.cleaned_data.get('Model_No')
                ProjectCode = myform.cleaned_data.get('Project')
                
                Condition = myform.cleaned_data.get('Asset_Condition')
                Status = myform.cleaned_data.get('Asset_Status')
                #ProjectName = myform.cleaned_data.get('Project_Name')
                # Username = staffobj,
                Available = myform.cleaned_data.get('Availability')
                location = myform.cleaned_data.get('Location')
                purchaseDate = myform.cleaned_data.get('PurchaseDate')
                vendor = request.POST.get('Vendor')
                print(purchaseDate)
                

                ProjectName = projectMatch(ProjectCode)
                print(ProjectName)
                if not Ast_Tag_number:
                    messages.info(request, "Asset Engravement Number is Required")

                if not UGX or not USD:
                    messages.error(request, "Enter Asset Cost in Either USD or UGX Sections")
                if not Type:
                    messages.error(request, "Asset Type is required")
                if not Model_Number:
                    messages.error(request, "Model number is required")
                if not myform.cleaned_data.get('PurchaseDate'):
                    messages.error(request, "Date of Purchase is required")
                
                if AssetTb.objects.filter(Ast_Tag_nbr=Ast_Tag_number).count() > 0:
                    messages.info(request, f'Asset {Ast_Tag_number} already exists in database')

                elif Ast_Tag_number and UGX and USD and Model_Number and purchaseDate:

                    try:

                        AssetTb.objects.create(
                            #Blank_Column ="351",
                            Company="351",
                            Ast_Tag_nbr=Ast_Tag_number,
                            Serial_No=Serial_Number,
                            #Lawson_Asset_No=Lawson_Asset_Number,
                            Ast_description=Asset_description,
                            Item_Cost_UGX=UGX,
                            Item_Cost_USD=USD,
                            Asset_Type=Type,
                            Model_No=Model_Number,
                            Project=ProjectCode,
                            Asset_Condition=Condition,
                            Asset_Status=Status,
                            Project_Name=ProjectName,
                            # Username = staffobj,
                            Availability=Available,
                            Location=location,
                            PurchaseDate=purchaseDate
                        )
                        messages.success(request, f'Asset {Ast_Tag_number} has been added successfully')

                        Events.objects.create(

                        EventType = "Asset Addition",
                        EventSummary = f"{datetime.datetime.now()} : User {request.user} added asset {Ast_Tag_number} to the database"

                        )
                    except Exception as e:
                        
                        messages.error(request, f'Asset {Ast_Tag_number} could not be added.'
                        'Returned {e} . \nContact Systems Administrator')
                        print(e)
            else:
                print(f"Invalid {myform.errors}")

    context = {'AssetObj': AssetObj, "response": response, 'values': request.POST, 'myform':myform}

    return render(request, "base/add_asset.html", context)

def get_device(request):
        
      if request.method == 'GET':      
        if 'term' in request.GET:
            qs = AssetTb.objects.filter(Q(Ast_Tag_nbr__istartswith=request.GET.get('term'))
                                | Q(AstNo__istartswith=request.GET.get('term'))
                                | Q(Ast_Tag_nbr__icontains=request.GET.get('term'))
                                | Q(AstNo__icontains=request.GET.get('term'))
                                )
            Assets =list()
            for asset in qs:
                Assets.append(asset.Ast_Tag_nbr)
            return JsonResponse(Assets,safe=False)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['Admin', 'Finance', 'IT','Accountant'])
def AssetRequestView(request, pk):
    excludes = ['Lost', 'Missing', 'Disposed-off','Disposed-of','DUE FOR DISPOSAL',"FAULTY","Faulty"]
    RequestObj = AssetRequests.objects.get(id=pk)
    Approver = staff.objects.get(Username=request.user)
    myform = AssetRQForm(instance=RequestObj)
    # AssetTb.objects.filter(Asset_Type__icontains="PRINTER COLOURED").update(Asset_Type="PRINTER")
    # pooleddevices = AssetTb.objects.filter(Availability="Available")
    AssignedObjects = Assignment.objects.all()
    AssignedEquipment=[]
   
    for Equipment in AssignedObjects:
        AssignedEquipment.append(Equipment.Ast_Tag_nbr)
    conditions = ["Faulty","obsolete","Bad"]
    pooleddevices = AssetTb.objects.exclude(Ast_Tag_nbr__in=AssignedEquipment).\
        exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).\
        exclude(Asset_Type__in=ExcludedTypes).\
        exclude(Asset_Condition__in=conditions).\
        order_by('Asset_Type')
    domain = get_current_site(request).domain
                        # print(domain)

    link = reverse('homepage')
    print(link)
    full_link = 'https://'+domain+link
    
    AssignmentObj = Assignment.objects.filter(Ast_Tag_nbr=RequestObj.Assigned_Device)
    francisobj = staff.objects.get(Username='fssemanda')
    print(Approver.staffrole)
    link = reverse('RQView', args=[RequestObj.id])
    link2 = 'https://'+domain+link
    print(link2)
    

    AssetManager = staff.objects.filter(staffrole="Asset Manager").get()
    if request.method == 'POST':
        if "approve" in request.POST:
            myform = AssetRQForm(request.POST, instance=RequestObj)
            print(request.POST)
            if Approver.staffrole=='Admin':
                try:
                    try:
                        RequestObj.Assigned_Device = AssetTb.objects.filter(Ast_Tag_nbr=request.POST['Ast_Tag_nbr']).get()
                    except Exception as e:
                        messages.error(request, f'Exception here {e}')
                        RequestObj.Assigned_Device = AssetTb.objects.filter(Ast_Tag_nbr=request.POST['Assigned_Device']).get()
                    RequestObj.AssetManagerApproval =  'Approved'
                    RequestObj.Status = 'In Process'
                    RequestObj.AssetMangerApprovalComments =  request.POST['AssetManagerApprovalComments']
                    RequestObj.Last_Modified = datetime.date.today()
                    RequestObj.save()
                    try:
                        AssetObj = AssetTb.objects.get(Ast_Tag_nbr=RequestObj.Assigned_Device)
                        AssetObj.Availability = "UNAVAILABLE FOR ASSIGNMENT"
                        AssetObj.save()
                    except Exception as e:
                        messages.error(request, f'Asset Manager exception occured here{e}')
                    merge_data = { 
            'Fname':RequestObj.Username.Firstname, 
            'Lname':RequestObj.Username.Lastname, 
            'Asset':RequestObj.Assigned_Device, 
            'Request':RequestObj.id, 
                'Condition':RequestObj.Assigned_Device.Asset_Condition,
                'Availability':RequestObj.Assigned_Device.Availability,
                'Current_user':AssignmentObj,
                'Location': RequestObj.Assigned_Device.Location,
                'Asset_Type': RequestObj.Assigned_Device.Asset_Type,
                'link':link2
                }
                    email_subject = f'Your request for a {RequestObj.Device_Type} has been Approved by IT'
                    email_body = f'Dear {RequestObj.Username.Firstname},\n IT department has Approved your request for a {RequestObj.Device_Type}. \
                    \n \n Comments: {RequestObj.AssetMangerApprovalComments}\
                        \n Next Approval Level: Financial Accounts'

                    email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[RequestObj.Username.email,])
                    EmailThread(email).start()

                    
                    email_subject = f'Request for Asset Assignment'
                    text_body = render_to_string("base/mail.txt", merge_data)
                    html_body = render_to_string("base/requestMail.html", merge_data)
                    
                    print(f'sending mail to {RequestObj.Username.Manager.email}')
                    msg = EmailMultiAlternatives(email_subject,text_body, from_email="helpdesk@psiug.org",
                            to=[RequestObj.Username.Manager.email])
                    msg.attach_alternative(html_body, "text/html")
                    EmailThread(msg).start()
                    Events.objects.create(

                EventType = "Asset Request",
                EventSummary = f"{datetime.datetime.now()} : Staff {request.user} has approved {RequestObj.Username} \'s request for {RequestObj.Assigned_Device}"

                )
                    messages.info(request, f"You have approved {RequestObj.Username}\'s request for {RequestObj.Assigned_Device}")
                    try:
                        Reject_others = AssetRequests.objects.filter(Q(Assigned_Device=RequestObj.Assigned_Device) 
                                                                    & Q(AssetManagerApproval="Pending"))
                        for i in Reject_others:
                                print(f'The following items are being rejected: {i} request from {i.Username}')
                                
                                
                                email_subject = f'Your request for a {i.Device_Type} has been Rejected'
                                email_body = f'Dear {i.Username.Firstname} {i.Username.Lastname},\n \
                                    IT department has rejected your request for a {i.Device_Type}.\
                                        \n \n Reason: Another user was assigned the same device you requested'

                                email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[i.Username.email,])
                                EmailThread(email).start()
                        print (f'Count of other requests to be rejected {Reject_others}')
                        
                        if Reject_others.count() > 0:
                            print(f'{Reject_others.count()} is greater than zero')
                            Reject_others.update(Status="Rejected")
                            Reject_others.update(AssetManagerApproval="Rejected")
                            # print('Items rejected')
                            Emails= []
                            
                           
                                
                        else:
                            print(f'No count {Reject_others.count()}') 
                             

                    except Exception as e:
                        print({e})
                        messages.error(request, f'An exception occured here{e}')     
                except Exception as e:
                    print(f'Another exception occured here{e}')
                    messages.error(request, f"Requested Action Failed (1). Contact \
                Systems Administrator. Error: {e}")
        
      
            elif Approver.staffrole == "Asset Manager" and RequestObj.AssetManagerApproval == "Approved":
                '''Checking if Logged in User is the Asset Manager'''
                merge_data = { 
        'Fname':RequestObj.Username.Firstname, 
        'Lname':RequestObj.Username.Lastname, 
        'Asset':RequestObj.Assigned_Device, 
        'Request':RequestObj.id, 
            'Condition':RequestObj.Assigned_Device.Asset_Condition,
            'Availability':RequestObj.Assigned_Device.Availability,
            'Current_user':AssignmentObj,
            'Location': RequestObj.Assigned_Device.Location,
            'Asset_Type': RequestObj.Assigned_Device.Asset_Type,
            'link':link2
            }
                try:
                    RequestObj.FinanceManagerApproval =  'Approved'
                    RequestObj.Status = 'Fully Approved'
                    RequestObj.FinanceManagerApprovalComments =  request.POST['FinanceManagerApprovalComments']
                    RequestObj.Last_Modified = datetime.date.today()
                    RequestObj.save()
                    email_subject = f'Your request for a {RequestObj.Device_Type} has been Approved by Financial Accounts'
                    email_body = f'Dear {RequestObj.Username.Firstname},\n Assets Manager {AssetManager.Username} has Approved your request for a {RequestObj.Device_Type}. \
                    \n \n Comments: {RequestObj.FinanceManagerApprovalComments}\
                        \nNext Approval Level: Fully Approved. \n\
                        Log into your account and accept device then proceed to pick it from IT'

                    email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[RequestObj.Username.email,])
                    EmailThread(email).start()
                    email_subject = f'Request for Asset Assignment'
                    text_body = render_to_string("base/mail.txt", merge_data)
                    html_body = render_to_string("base/requestMail.html", merge_data)
                    
                    print(f'sending mail to {Approver.email}')
                    msg = EmailMultiAlternatives(email_subject,text_body, from_email="helpdesk@psiug.org",
                            to=[Approver.email])
                    msg.attach_alternative(html_body, "text/html")
                    EmailThread(msg).start()
                    Events.objects.create(

                EventType = "Asset Request",
                EventSummary = f"{datetime.datetime.now()} : Staff {request.user} has approved {RequestObj.Username} \'s request for {RequestObj.Assigned_Device}"


                )
                    messages.info(request, f"You have approved {RequestObj.Username}\'s request for {RequestObj.Assigned_Device}")
                    return redirect('homepage')
                except Exception as e:
                    print({e})
                    messages.error(request, f"Requested Action Failed-(2). Contact \
                    Systems Administrator. Error: {e}")
                    return redirect('homepage')
                    
        else:
            """Rejection Else"""
            print('rejected')
            try: 
                if Approver.staffrole =='Admin' or Approver.staffrole == 'IT Support Assistant':
                    RequestObj.AssetManagerApproval =  'Rejected'
                    RequestObj.AssetMangerApprovalComments =  request.POST['AssetManagerApprovalComments']
                    RequestObj.save()
                    messages.error(request, f"Request Rejected Successfully")
                    email_subject = f'Your request for a {RequestObj.Device_Type} has been Rejected'
                    email_body = f'Dear {RequestObj.Username.Firstname},\n IT department has rejected your request for a {RequestObj}. \
                        \n \n Reason: {RequestObj.AssetMangerApprovalComments}'

                    email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[RequestObj.Username.email,])
                    EmailThread(email).start()
                    Events.objects.create(

                EventType = "Asset Request",
                EventSummary = f"{datetime.datetime.now()} : Staff {request.user} has Rejected {RequestObj.Username} \'s request for {RequestObj.Assigned_Device}"


                )
                    messages.info(request, f"You have rejected {RequestObj.Username}\'s request for {RequestObj.Assigned_Device}")
                # elif RequestObj.Username.Manager.Username == Approver.Username:
                #     RequestObj.SupervisorApproval =  'Rejected'
                #     RequestObj.SupervisorApprovalComments =  request.POST['SupervisorComments']
                #     RequestObj.save()
                #     messages.error(request, f"Requested Rejected Successfully")
                #     email_subject = f'Your request for a {RequestObj.Device_Type} has been Rejected'
                #     email_body = f'Dear {RequestObj.Username.Firstname},\n Your Supervisor has rejected your request for a {RequestObj}. \
                #     \n \n Reason: {RequestObj.SupervisorApprovalComments}'

                #     email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[RequestObj.Username.email,])
                #     EmailThread(email).start()
                #     Events.objects.create(

                # EventType = "Asset Request",
                # EventSummary = f"{datetime.datetime.now()} : Staff {request.user} has Rejected {RequestObj.Username} \'s request for {RequestObj.Assigned_Device}"


                # )
                #     messages.info(request, f"You have rejected {RequestObj.Username}\'s request for {RequestObj.Assigned_Device}")
                    return redirect('homepage')
                elif Approver.staffrole == "Asset Manager":
                    RequestObj.FinanceManagerApproval =  'Rejected'
                    RequestObj.FinanceManagerApprovalComments =  request.POST['FinanceManagerApprovalComments']
                    RequestObj.save()
                    messages.error(request, f"Requested Rejected Successfully")
                    email_subject = f'Your request for a {RequestObj.Device_Type} has been Rejected'
                    email_body = f'Dear {RequestObj.Username.Firstname},\n Assets Manager {AssetManager.Username} has rejected your request for a {RequestObj}.\
                        \n \n Reason: {RequestObj.FinanceManagerApprovalComments}'

                    email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[RequestObj.Username.email,])
                    EmailThread(email).start()
                    Events.objects.create(

                EventType = "Asset Request",
                EventSummary = f"{datetime.datetime.now()} : Staff {request.user} has Rejected {RequestObj.Username} \'s request for {RequestObj.Assigned_Device}"


                )
                    messages.info(request, f"You have rejected {RequestObj.Username}\'s request for {RequestObj.Assigned_Device}")
                    return redirect('homepage')
                else:
                    print("Rejection Failed")
                    messages.error(request, f"Requested Action Failed (3). Contact \
                    Systems Administrator.")
                    return redirect('homepage')
            except Exception as e:
                    print({e})
                    messages.error(request, f"Requested Action Failed (4). Contact \
                    Systems Administrator. Error: {e}")
                    return redirect('homepage')
        

    context = {'AssignedObjects':AssignedObjects,'pooleddevices':pooleddevices,'myform': myform, "RequestObj":RequestObj,"MyValues":request.POST.values()}

    return render(request, "base/Approve_Pool_Request.html", context)


def Reject(request, pk):
    AssetObj = AssetRequests.objects.get(id=pk)

    if request.method == 'POST':
        AssetObj.delete()
        return redirect('/')
        Events.objects.create(

            EventType = "Asset Request Rejected",
            EventSummary = f"{datetime.datetime.now()} : User {request.user} has rejected {AssetObj.Username}\'s asset request"

            )
    context = {'Asset': AssetObj}

    

    return render(request, "base/delete.html", context)

def checkAvailability(user,value1,value2):
    if(value1 == value2):
        pass
    else:
        return logging.info(f"{user} has edited Asset details from {value1} to {value2}")

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Asset Managers', 'IT','Assistant Accountant-Treasury'])
def editItem(request, pk):
    AssetObj = AssetTb.objects.get(Ast_Tag_nbr=pk)
    staffobj = staff.objects.get(Username=request.user)

    AllAssetObj = AssetTb.objects.all()

    myform = AddAssetForm(instance=AssetObj)

    if request.method == 'POST':
        Ast_Tag_number = request.POST.get('Ast_Tag_nbr')        
        Serial_Number = request.POST.get('Serial_No')    
        Asset_description = request.POST.get('Ast_description')
        UGX = request.POST.get('Item_Cost_UGX')
        USD = request.POST.get('Item_Cost_USD')
        Type = request.POST.get('Asset_Type')
        Model_Number = request.POST.get('Model_No')
        ProjectCode = request.POST.get('Project')
        Condition = request.POST.get('Asset_Condition')
        Status = request.POST.get('Asset_Status')
        #ProjectName = request.POST.get('Project_Name')
        # Username = staffobj,
        Available = request.POST.get('Availability')
        location = request.POST.get('Location')
        purchaseDate = request.POST.get('PurchaseDate')
        comments = request.POST.get('Comments')
        vendor = request.POST.get('Vendor')
        astNo = request.POST.get('AstNo')

        print(purchaseDate)

        if not Ast_Tag_number:
            messages.info(request, "Asset Engravement Number is Required")
        elif not UGX or not USD:
            messages.error(request, "Enter Asset Cost in Either USD or UGX Sections")
        elif not Type:
            messages.error(request, "Asset Type is required")
        elif not Model_Number:
            messages.error(request, "Model number is required")
        elif not request.POST.get('PurchaseDate'):
            messages.error(request, "Date of Purchase is required")
        else:
            
            try:
                modifications=[]
                modifications.append(checkAvailability(request.user,  AssetObj.Ast_Tag_nbr,Ast_Tag_number))
                
                modifications.append (checkAvailability(request.user, AssetObj.Serial_No,Serial_Number ))
                checkAvailability(request.user,AssetObj.Ast_description,Asset_description )
                checkAvailability(request.user,float(AssetObj.Item_Cost_UGX), float(UGX))
                checkAvailability(request.user, float(AssetObj.Item_Cost_USD) , float(USD))
                checkAvailability(request.user, AssetObj.Asset_Type, Type)
                checkAvailability(request.user, AssetObj.Model_No , Model_Number )
                checkAvailability(request.user, AssetObj.Project ,ProjectCode , )
                checkAvailability(request.user,   AssetObj.Asset_Condition , Condition, )
                checkAvailability(request.user, AssetObj.Asset_Status, Status )
                # modifications.append(checkAvailability(request.user,  AssetObj.Project_Name , ProjectName ))
                checkAvailability(request.user,  AssetObj.Availability, Available )
                checkAvailability(request.user,  AssetObj.Location, location )
                checkAvailability(request.user,  AssetObj.PurchaseDate , purchaseDate )

                '''Instead of Editing the AssetTB Object, I am creating a new object of the change log model '''

                # AssetObj.Ast_Tag_nbr = Ast_Tag_number
                # AssetObj.Serial_No = Serial_Number
                # AssetObj.Ast_description = Asset_description
                # AssetObj.Item_Cost_UGX = UGX
                # AssetObj.Item_Cost_USD = USD
                # AssetObj.Asset_Type = Type
                # AssetObj.Model_No = Model_Number
                # AssetObj.Project = ProjectCode
                # AssetObj.Asset_Condition = Condition
                # AssetObj.Asset_Status = Status
                # AssetObj.Project_Name = ProjectName
                # # Username = staffobj
                # AssetObj.Availability = Available
                # AssetObj.Location = location
                # AssetObj.PurchaseDate = purchaseDate
                

                # AssetObj.save()

                print(request.user)
                ProjectName = projectMatch(ProjectCode)
                ChangeLog.objects.create(
                        Requester = request.user,
                        
                        AstTagnbr=Ast_Tag_number,
                        SerialNo=Serial_Number,             
                        AstDescription=Asset_description,
                        ItemCostUGX=UGX,
                        ItemCostUSD=USD,
                        AssetType=Type,
                        ModelNo=Model_Number,
                        Project=ProjectCode,
                        AssetCondition=Condition,
                        AssetStatus=Status,
                        ProjectName=ProjectName,
                        # Username = staffobj,
                        Availability=Available,
                        Location=location,
                        Vendor = vendor,
                        AstNo = astNo,
                        Modifications = modifications,
                        PurchaseDate=purchaseDate,
                        RequesterComments = comments,
                        
                    )
                domain = get_current_site(request).domain

                print(domain)

                link = reverse('approval_list')
                print(link)
                full_link = 'http://'+domain+link

                print(full_link)

                Approvers = staff.objects.filter(staffrole='Finance')|staff.objects.filter(staffrole='Admin')
                Emails = ['macho.francis2@gmail.com']
                for user in Approvers:
                    Emails.append(user.email)

                    print(Emails)

                    email_subject = f'Approval Request for Modification of {Ast_Tag_number}'
                    email_body = f'Dear {user.Firstname},\n {request.user.first_name} is requesting for approval to modify {Ast_Tag_number}. Click on Link below to view request\n'+full_link

                    email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[user.email,])
                    EmailThread(email).start()

                print("First mail sent")

                messages.success(request, f'Request to make changes on {Ast_Tag_number} has been submitted successfully')
                Events.objects.create(

                        EventType = "Asset Modification",
                        EventSummary = f"{datetime.datetime.now()} : User {request.user} has made changes to {Ast_Tag_number}. The changes are pending approval"

                        )
                return redirect('view_assets')

            except:
                ValueError()
                messages.info(request, f'Asset {Ast_Tag_number} could not be updated. Contact Systems Administrator')
                return redirect('/edit-item/' + Ast_Tag_number)

    context = {'values': AssetObj, 'AllAssetObj': AllAssetObj, 'myform':myform}

    return render(request, "base/itemedit.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Finance', 'IT','Assistant Accountant-Treasury'])
def Fileupload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            obj = CsvUpload.objects.get(Parsed=False)
            with open(obj.file_name.path, 'r') as f:
                reader = csv.reader(f)
                try:
                    next(reader)
                    for row in reader:
                        UGX_value = row[5]
                        UGX_value = UGX_value.replace(",", "")
                        UGX_value = float(UGX_value)

                        USD_value = row[4]
                        USD_value = USD_value.replace(",", "")
                        USD_value = float(USD_value)

                        # The date split it via / then tuple unpack it and compose a new string i required structure.

                        DateFormat = row[15]

                        DateFormat1 = DateFormat.split('/')
                        print(DateFormat1)
                        NewDate = "-".join([DateFormat1[2], DateFormat1[0],
                                            DateFormat1[1]])

                        print(NewDate)

                        # staffobj = staff.objects.get(Username='kakooza')

                        # AssetNo = AssetTb.objects.filter(Ast_Tag_nbr=row[0])

                        # print(AssetNo)

                        # if AssetNo is not None:
                        if AssetTb.objects.filter(Ast_Tag_nbr=row[0]).exists():
                            continue
                        else:
                            AssetTb.objects.create(
                                Ast_Tag_nbr=row[0],
                                Serial_No=row[1],
                                AstNo=row[2],
                                Ast_description=row[3],
                                Item_Cost_UGX=UGX_value,
                                Item_Cost_USD=USD_value,
                                Asset_Type=row[6],
                                Model_No=row[7],
                                Project=row[8],
                                Asset_Condition=row[9],
                                Asset_Status=row[10],
                                Project_Name=row[11],
                                # Username = staffobj,
                                Availability=row[12],
                                Location=row[13],
                                Vendor = row[14],
                                PurchaseDate=NewDate,
                                Comments = row[16]

                            )

                            messages.info(request, f'Asset {row[0]} has been added to the Database')
                            Events.objects.create(

                            EventType = "Asset Addition",
                            EventSummary = f"{datetime.datetime.now()} : User {request.user} has added Asset {row[0]} to the database"

                            )

                        # print(row[4])
                        # print(type(row[4]))

                        # print(type(value))
                    obj.Parsed = True
                    obj.save()

                except Exception as e:
                    obj.Parsed = True
                    obj.save()
                    return e
        return redirect('reports')
    else:
        form = FileUploadForm()

    context = {'form': form}

    return render(request, 'base/upload.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Finance', 'IT', 'Accountant','Assistant Accountant-Treasury'])
def deleteItem(request, pk):
    AssetObj = AssetTb.objects.get(Ast_Tag_nbr=pk)
    No = AssetObj.Ast_Tag_nbr
    AssetObj.delete()
    messages.success(request, f'Asset {No} has been deleted successfully')

    return redirect('view_assets')
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Finance', 'IT','Accountant'])
def RemoveAssignment(request, pk):
    #wont work because we are pulling an ID
    AssignmentObj= Assignment.objects.get(id=pk)

    domain = get_current_site(request).domain
    print(domain)

    link = reverse('approval_list')
    print(link)
    full_link = 'http://'+domain+link

    print(full_link)

    myid = AssignmentObj.id

    Approvers = staff.objects.filter(staffrole='Finance')|staff.objects.filter(staffrole='Admin')
    Emails = ['macho.francis2@gmail.com']
    for user in Approvers:
        Emails.append(user.email)

        print(Emails)

        email_subject = f'Approval to Modify Staff Asset Assignment {AssignmentObj.Ast_Tag_nbr}'
        email_body = f'Dear {user.Firstname},\n\n {request.user.first_name} is requesting for approval to remove Asset - {AssignmentObj.Ast_Tag_nbr} from {AssignmentObj.Username}\'s list of Assigned Assets. Click on Link below to view request\n'+full_link

        # email_subject = f'Approval Request for Modification of {Ast_Tag_number}'
        # email_body = 'TEST'
        # email_subject2 = f'Second Request for Modification of {Ast_Tag_number}'
        # email_body2 = 'Another one'

        email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[user.email,])
        EmailThread(email).start()

    DeleteAssignment.objects.create(
        AssignmentID = AssignmentObj
        

    )

    print("First mail sent")

    Events.objects.create(

                            EventType = "Asset Withdrawal",
                            EventSummary = f"{datetime.datetime.now()} : User {request.user} has requested for withdraw of Asset {AssignmentObj.Ast_Tag_nbr} from {AssignmentObj.Username}"

                            )

    messages.success(request, f'Request to remove asset assignment has been sent.')

    return redirect('assetAssignment')
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Finance', 'IT','Accountant'])
def withdrawList(request):

    DeleteAssignmentObj = DeleteAssignment.objects.filter(Response="Pending")
    
    context={'DeleteAssignmentObj':DeleteAssignmentObj}

    return render(request, 'base/Assetwithdrawlist.html', context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Finance', 'IT','Accountant'])
def withdraw(request,pk):
    DeleteAssignmentObj = DeleteAssignment.objects.get(id=pk)
   
    AssignmentObj = Assignment.objects.get(id=DeleteAssignmentObj.AssignmentID.id)

    form = Assetwithdrawform(instance=DeleteAssignmentObj)

    if request.method=='POST':
        
        form= Assetwithdrawform(request.POST, instance=DeleteAssignmentObj)

        print(request.POST.get('Response'))
        print(request.POST.get('Comments'))
        print(request.POST.get('AssignmentID'))

        

        if form.is_valid():
            form.save
            if request.POST.get('Response')=='Approved':
                AssetTb.objects.filter(Ast_Tag_nbr=AssignmentObj.Ast_Tag_nbr).update(Availability="AVAILABLE")
                AssignmentObj.delete()
                # email_subject = f'Approval to Modify Staff Asset Assignment {AssignmentObj.Ast_Tag_nbr}'
                # email_body = f'Dear {user.Firstname},\n\n {request.user.first_name} is requesting for approval to remove Asset - {AssignmentObj.Ast_Tag_nbr} from {AssignmentObj.Username}\'s list of Assigned Assets. Click on Link below to view request\n'+full_link

            

                # email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[user.email,])
                # EmailThread(email).start()
                Events.objects.create(

                            EventType = "Asset Withdrawal",
                            EventSummary = f"{datetime.datetime.now()} : User {request.user} has approved withdraw of Asset {AssignmentObj.Ast_Tag_nbr} from {AssignmentObj.Username}"

                            )
                return redirect('withdraw-list')
            elif request.POST.get('Response')=='Rejected':
                DeleteAssignmentObj.delete()
                messages.error(request, f"Request has been rejected. Comments: {request.POST.get('Comments')}")
                

        else:
            print("Form invalid")

    context =  {'form':form, 'AssignmentObj':AssignmentObj,'DeleteAssignmentObj':DeleteAssignmentObj}

    return render (request, 'base/withdraw.html', context)

    


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Finance', 'IT','Accountant'])
class itemsView(ListView):
    model = AssetTb
    template_name = 'base/listing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs_json"] = json.dumps(list(AssetTb.objects.values()))
        return context

@allowed_users(allowed_roles=['Admin', 'Finance', 'IT'])
def auctionList(request):
    Mylist = AssetTb.objects.all()

    qs_json = json.dumps(list(AssetTb.objects.values()), default=myconverter)
    context = {'Mylist': Mylist, 'qs_json': qs_json}

    return render(request, 'base/AuctionList.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Finance', 'IT','Accountant','Assistant Accountant-Treasury'])
def assetAssignment(request):
    # Assignedassets = AssetTb.objects.filter(Availability="Assigned")
    All_Assigned_devices = Assignment.objects.select_related('Username').all().order_by('Username', '-Ast_Tag_nbr')
    Num_assigned = All_Assigned_devices.count()

    paginator = Paginator(All_Assigned_devices, 15)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {"All_Assigned_devices":All_Assigned_devices, "Num_assigned":Num_assigned, 'page_obj':page_obj}
    return render(request, 'base/assetassignment.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Finance', 'IT','Accountant','Assistant Accountant-Treasury'])
def assign_asset(request, pk):
    newpk = pk.strip()
    print(newpk)
    AssignObj = AssetTb.objects.get(Ast_Tag_nbr=newpk)


    myAssignmentForm = AssignmentForm(instance=AssignObj)
    form = FileUploadForm()

    #CurrentAssignment = AssignObj.objects.get(Ast_Tag_nbr=newpk)

    if request.method == 'POST':
        try:
            myAssignmentForm = AssignmentForm(request.POST)
            if myAssignmentForm.is_valid():
                myAssignmentForm.save()
                messages.success(request, f"Asset has been assigned to {myAssignmentForm.cleaned_data.get('Username')}")
                Device = myAssignmentForm.cleaned_data.get('Ast_Tag_nbr')
                AssetTb.objects.filter(Ast_Tag_nbr=Device).update(Availability="ASSIGNED")
            else:
                try:
                    Assigned_devices = Assignment.objects.get(Ast_Tag_nbr=newpk)
                    messages.error(request,
                                   f"Failed. Asset is currently assigned to {Assigned_devices.Username}")
                    return redirect('view_assets')
                except LookupError as e:
                    print(e)
        except Exception as e:
            messages.error(request,
                           f"Asset Can be Assigned twice. Asset is currently assigned {e}")
            print(e)


    context = {"myAssignmentForm": myAssignmentForm, "AssignObj": AssignObj, }
    return render(request, 'base/assign.html', context)

@allowed_users(allowed_roles=['Admin', 'Finance', 'IT','Accountant'])
def assign_device(request):


    # if request.method == "POST":
    #     Username = request.POST.get('Username')
    #     Asset_No = request.POST.get('Ast_Tag_nbr')
    #
    #     AssignObj = AssetTb.objects.get(Ast_Tag_nbr=Asset_No)
    #
    #     Assignment.objects.create(
    #         Username = Username,
    #         Ast_Tag_nbr = Asset_No
    #     )
    #
    #
    #
    # print(AssignObj.Ast_Tag_nbr)
    #
    # Assignments = Assignment.objects.all()
    # #
    # #myAssignmentForm = AssignmentForm(instance=AssignObj)
    # #
    # ##   print(AssignObj)
    #
    # # context = { "AssignObj":AssignObj}"Assignments":Assignments
    # context = {"myAssignmentForm": myAssignmentForm, "AssignObj": AssignObj, }
    return render(request, 'base/assign.html',)

def pool_equip_request(request, pk):
    """
    Remember to change Asset manager approval object in that the moment the Asset manager approval for 
    A pool object is "Approved" then remove that object from the pool devices immediately until the device is returned
    Device will always be temporarily added to the user assigned devices once the request is approved by the Final person 
    for the length of time its in their custody until the device is handed over back to IT and IT confirms receipt
    """
    assetRqObj = AssetTb.objects.get(Ast_Tag_nbr = pk)
    staffobj =  staff.objects.get(Username = request.user)
    print(staffobj)
    #myform = RqForm(initial={'Username': staffobj})
    
    form =  AssetRQForm(instance=assetRqObj)
    
    if AssetRequests.objects.filter(Q(Assigned_Device=assetRqObj) & Q(AssetManagerApproval="Pending")).exists():
        messages.error(request, "1. There is another request in the system for this Device \n")
        messages.info(request, "2. Qeueing and Assigment will be based on either Priority or First Come First Serve")

    if request.method == 'POST':
        
        MyAst_Tag_nbr = request.POST.get("Ast_Tag_nbr")
        Reason = request.POST.get("Reason")
        """
            In future there is need to add some AJAX that checks this on the fly so that as someone clicks
            on the request device button, a pop shows up telling them this same message below
        """
        if AssetRequests.objects.filter(Q(Assigned_Device=MyAst_Tag_nbr) & Q(Username=staffobj) & Q(AssetManagerApproval="Pending")).exists():
            messages.warning(request, f'You already have a request in the system for this Asset')
            return redirect('AssetRQ')
        else:
            existingRequestObjects = AssetRequests.objects.filter(Q(Assigned_Device=MyAst_Tag_nbr) & Q(AssetManagerApproval="Pending"))
            Current_Requests=[]
            for item in existingRequestObjects:
                    Current_Requests.append(item.Username)

            NewRequestObject=AssetRequests.objects.create(
                    Assigned_Device = assetRqObj,
                    Device_Type = assetRqObj.Asset_Type,
                    #Status = ,
                    Username = staffobj,
                    Reason = Reason,
                )
            
            print(f'This is the ID of the new request {NewRequestObject.id}')
            
            domain = get_current_site(request).domain
                        # print(domain)

            link = reverse('homepage')
            print(link)
            full_link = 'https://'+domain+link

            print(full_link)
            messages.success(request, "Your Request for a pool device has been placed "\
                                "successfully. Wait for a confirmation Email to pick Equipment")
            Events.objects.create(

                EventType = "Asset Request",
                EventSummary = f"{datetime.datetime.now()} : Staff {request.user} is requesting for temporary assignment of {assetRqObj.Ast_Tag_nbr}"

                )
            AssignmentObj = Assignment.objects.filter(Ast_Tag_nbr=assetRqObj)
            
            # Approvers = staff.objects.filter(staffrole='Admin')
            Approvers = staff.objects.filter(Username='fssemanda')
            Emails = []
            for user in Approvers:
                Emails.append(user.email)

                print(Emails)
                francisobj = staff.objects.get(Username='fssemanda')
                print(francisobj.staffrole)
                link = reverse('RQView', args=[NewRequestObject.id])
                link2 = 'https://'+domain+link
                print(link2)
                email_subject = f'Request for Temporary Assignment of IT Pool Asset'

                merge_data = { 
                              'Fname':staffobj.Firstname, 
                              'Lname':staffobj.Lastname, 
                              'Asset':assetRqObj, 
                              'Request':NewRequestObject.id, 
                                'Condition':assetRqObj.Asset_Condition,
                                'Availability':assetRqObj.Availability,
                                'Current_user':AssignmentObj,
                                'Location': assetRqObj.Location,
                                'Asset_Type': assetRqObj.Asset_Type,
                                'link':link2
                                }
                text_body = render_to_string("base/mail.txt", merge_data)
                html_body = render_to_string("base/requestMail.html", merge_data)
                
                print(f'sending mail to {user.email}')
                msg = EmailMultiAlternatives(email_subject,text_body, from_email="helpdesk@psiug.org",
                        to=[user.email])
                msg.attach_alternative(html_body, "text/html")
                EmailThread(msg).start()
                # msg.send()
                # EmailThread(email).start()
                    
                print(Emails)
            return redirect('AssetRQ')

    context = {'assetRqObj':assetRqObj, 'form':form}

    return render(request, 'base/assetpool.html', context)
@csrf_exempt
@login_required(login_url='login')
def Acceptance(request):
    
    if request.method == 'GET':
        pk = request.GET['pk']

        RequestObj = AssetRequests.objects.get(id=pk)
        AssetObj = AssetTb.objects.get(Ast_Tag_nbr=RequestObj.Assigned_Device)
        
        Asset_Details = [

            {
                 'Ast_Tag':AssetObj.Ast_Tag_nbr,
                 'AstNo':AssetObj.AstNo,
                 
                    'Model_No' :AssetObj.Model_No,
                         'Serial_No':AssetObj.Serial_No,
                        'Asset_Type':AssetObj.Asset_Type,
                        'Asset_Condition':AssetObj.Asset_Condition,
            }
        ]
        
        data = Asset_Details
        print(data)
        
        AssetObj.Availability = "ASSIGNED"
        AssetObj.save()
        
        Assignment.objects.create(
            Username = RequestObj.Username,
            Ast_Tag_nbr = RequestObj.Assigned_Device
            
        )
        
        RequestObj.Status = "User Accepted"
        RequestObj.save()
        Events.objects.create(

            EventType = "Asset accepted",
            EventSummary = f"{datetime.datetime.now()} : User {RequestObj.Username} has Accepted {AssetObj.Ast_Tag_nbr}"

            )
        
        return JsonResponse(list(data),safe=False)
    
    context={}
    
    return render(request, "base/staff_Asset_details.html",context)



class SendApprovalRequest(View):
    
    def get(self,request,pk):
        assetRqObj = AssetTb.objects.get(Ast_Tag_nbr = pk)
        
        context={'assetRqObj':assetRqObj, }
        return render(request,'base/assetpool.html', context)

    def post(self,request,pk):
        assetRqObj = AssetTb.objects.get(Ast_Tag_nbr = pk)
        staffobj =  staff.objects.get(Username = request.user)
        MyAst_Tag_nbr = request.POST.get("Ast_Tag_nbr")
        Reason = request.POST.get("Reason")
        """
            In future there is need to add some AJAX that checks this on the fly so that as someone clicks
            on the request device button, a pop shows up telling them this same message below
        """
        if AssetRequests.objects.filter(Q(Assigned_Device=MyAst_Tag_nbr) & Q(Username=staffobj) & Q(AssetManagerApproval="Pending")).exists():
            messages.warning(request, f'You already have a request in the system for this Asset')
            return redirect('AssetRQ')
        else:
            existingRequestObjects = AssetRequests.objects.filter(Q(Assigned_Device=MyAst_Tag_nbr) & Q(AssetManagerApproval="Pending"))
            Current_Requests=[]
            for item in existingRequestObjects:
                    Current_Requests.append(item.Username)

            NewRequestObject=AssetRequests.objects.create(
                    Assigned_Device = assetRqObj,
                    Device_Type = assetRqObj.Asset_Type,
                    #Status = ,
                    Username = staffobj,
                    Reason = Reason,
                )
            NewRequestObject.save()
            print(f'This is the ID of the new request {NewRequestObject.id}')
            
            domain = get_current_site(request).domain
                        # print(domain)

            link = reverse('homepage')
            print(link)
            full_link = 'https://'+domain+link

            print(full_link)
            messages.success(request, "Your Request for a pool device has been placed "\
                                "successfully. Wait for a confirmation Email to pick Equipment")
            Events.objects.create(

                EventType = "Asset Request",
                EventSummary = f"{datetime.datetime.now()} : Staff {request.user} is requesting for temporary assignment of {assetRqObj.Ast_Tag_nbr}"

                )
            AssignmentObj = Assignment.objects.filter(Ast_Tag_nbr=assetRqObj)
            
            # Approvers = staff.objects.filter(staffrole='Admin')
            Approvers = staff.objects.filter(Username='fssemanda')
            Emails = []
            for user in Approvers:
                Emails.append(user.email)

                # print(Emails)
                # francisobj = staff.objects.get(Username='fssemanda')
                # print(francisobj.staffrole)
                # link = reverse('RQView', args=[NewRequestObject.id])
                # link2 = 'https://'+domain+link
                # print(link2)
                # email_subject = f'Request for Temporary Assignment of IT Pool Asset'

                # merge_data = { 
                #               'Fname':staffobj.Firstname, 
                #               'Lname':staffobj.Lastname, 
                #               'Asset':assetRqObj, 
                #               'Request':NewRequestObject.id, 
                #                 'Condition':assetRqObj.Asset_Condition,
                #                 'Availability':assetRqObj.Availability,
                #                 'Current_user':AssignmentObj,
                #                 'Location': assetRqObj.Location,
                #                 'Asset_Type': assetRqObj.Asset_Type,
                #                 'link':link2
                #                 }
                # text_body = render_to_string("base/mail.txt", merge_data)
                # html_body = render_to_string("base/requestMail.html", merge_data)
                
                # print(f'sending mail to {user.email}')
                # msg = EmailMultiAlternatives(email_subject,text_body, from_email="helpdesk@psiug.org",
                #         to=[user.email])
                # msg.attach_alternative(html_body, "text/html")
                # EmailThread(msg).start()
                # msg.send()
                # EmailThread(email).start()
                    
                # print(Emails)
            # return redirect('AssetRQ')

        
                # email = request.POST['email']

                # print(email)

                context = {'values':request.POST,}

                current_site=get_current_site(request)

                requesting_user = User.objects.filter(username=request.user)
                anid = NewRequestObject.id
                if requesting_user.exists():
                    email_contents ={
                        'user':requesting_user[0],
                        'domain':current_site.domain,
                        'pk':urlsafe_base64_encode(force_bytes(anid)),
                        'uid': urlsafe_base64_encode(force_bytes(requesting_user[0].pk)),
                        'token':PasswordResetTokenGenerator().make_token(requesting_user[0]),

                    }

                    link = reverse('approve-reject',kwargs = {'pk':email_contents['pk'],'uidb64': email_contents['uid'], 'token': email_contents['token']})

                    email_subject = 'Asset Device Request'
                    reset_url = 'http://'+current_site.domain+link

                    email_body = f'Dear employee,\n\n Please follow this link to approve device request\n'+reset_url


                    

                    email = EmailMessage(email_subject, email_body,'helpdesk@psiug.org',[user.email])
                    
                    EmailThread(email).start()

                    messages.success(request, 'Asset Request submitted')

            return render(request,'base/assetpool.html',context)

class ApproveRequest(View):
    
    def get(self, request, pk, uidb64, token):

        context = {
            'uidb64':uidb64,
            'token':token, 
            'pk':pk
                   }
        excludes = ['Lost', 'Missing', 'Disposed-off','Disposed-of','DUE FOR DISPOSAL',"FAULTY","Faulty"]
        AssignedObjects = Assignment.objects.all()
        AssignedEquipment=[]
        
        for Equipment in AssignedObjects:
            AssignedEquipment.append(Equipment.Ast_Tag_nbr)
        conditions = ["Faulty","obsolete","Bad"]
        pooleddevices = AssetTb.objects.exclude(Ast_Tag_nbr__in=AssignedEquipment).\
            exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).\
            exclude(Asset_Type__in=ExcludedTypes).\
            exclude(Asset_Condition__in=conditions).\
            order_by('Asset_Type')
            
        try:
           
            user_id = force_text(urlsafe_base64_decode(uidb64))
            
            pk = force_text(urlsafe_base64_decode(pk))
            
            RequestObj = AssetRequests.objects.get(id=pk)
            
            user = User.objects.get(pk=user_id)
            print(RequestObj)
            if not PasswordResetTokenGenerator().check_token(user, token) and not PasswordResetTokenGenerator().check_token(pk, token):
                messages.info(request, "Link already used")
                return redirect('homepage')
            Approver = staff.objects.get(Username=request.user)
            myform = AssetRQForm(instance=RequestObj)
            print(user_id)
            print(pk)

            
           
            
        except Exception as e:
            messages.info(request,f"{e}.")
            
            return render(request, 'base/Approve_Pool_Request.html', context)
        context = {'uidb64':uidb64,
            'token':token
           , 'pk':pk ,'AssignedObjects':AssignedObjects,'pooleddevices':pooleddevices,'myform': myform, "RequestObj":RequestObj,"MyValues":request.POST.values()}

        return render(request, 'base/Approve_Pool_Request.html', context)
    
    def post(self, request, pk , uidb64, token):
        context = {
            'uidb64':uidb64,
            'token':token
           , 'pk':pk 
                   }

        
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            requestId = force_text(urlsafe_base64_decode(pk))
            user = User.objects.get(pk=user_id)
            print(user.last_name)
            
            excludes = ['Lost', 'Missing', 'Disposed-off','Disposed-of','DUE FOR DISPOSAL',"FAULTY","Faulty"]
            RequestObj = AssetRequests.objects.get(id=requestId)
            print(RequestObj)
            Approver = staff.objects.get(Username=request.user)
            myform = AssetRQForm(instance=RequestObj)
            # AssetTb.objects.filter(Asset_Type__icontains="PRINTER COLOURED").update(Asset_Type="PRINTER")
            # pooleddevices = AssetTb.objects.filter(Availability="Available")
            AssignedObjects = Assignment.objects.all()
            AssignedEquipment=[]
        
            for Equipment in AssignedObjects:
                AssignedEquipment.append(Equipment.Ast_Tag_nbr)
            conditions = ["Faulty","obsolete","Bad"]
            pooleddevices = AssetTb.objects.exclude(Ast_Tag_nbr__in=AssignedEquipment).\
                exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).\
                exclude(Asset_Type__in=ExcludedTypes).\
                exclude(Asset_Condition__in=conditions).\
                order_by('Asset_Type')
            domain = get_current_site(request).domain
                                # print(domain)

            link = reverse('homepage')
            print(link)
            full_link = 'https://'+domain+link
            
            AssignmentObj = Assignment.objects.filter(Ast_Tag_nbr=RequestObj.Assigned_Device)
            # francisobj = staff.objects.get(Username='fssemanda')
            print(Approver.staffrole)
            link = reverse('RQView', args=[RequestObj.id])
            link2 = 'https://'+domain+link
            print(link2)
            

            AssetManager = staff.objects.filter(staffrole="Asset Manager").get()
            if request.method == 'POST':
                if "approve" in request.POST:
                    myform = AssetRQForm(request.POST, instance=RequestObj)
                    
                    print(request.POST)
                    if Approver.staffrole=='Admin':
                        try:
                            try:
                                RequestObj.Assigned_Device = AssetTb.objects.filter(Ast_Tag_nbr=request.POST['Ast_Tag_nbr']).get()
                            except Exception as e:
                                messages.error(request, f'Exception here {e}')
                                RequestObj.Assigned_Device = AssetTb.objects.filter(Ast_Tag_nbr=request.POST['Assigned_Device']).get()
                            RequestObj.AssetManagerApproval =  'Approved'
                            RequestObj.Status = 'In Process'
                            RequestObj.AssetMangerApprovalComments =  request.POST['AssetManagerApprovalComments']
                            RequestObj.Last_Modified = datetime.date.today()
                            RequestObj.save()
                            try:
                                AssetObj = AssetTb.objects.get(Ast_Tag_nbr=RequestObj.Assigned_Device)
                                AssetObj.Availability = "UNAVAILABLE FOR ASSIGNMENT"
                                AssetObj.save()
                            except Exception as e:
                                messages.error(request, f'Asset Manager exception occured here{e}')
                            merge_data = { 
                    'Fname':RequestObj.Username.Firstname, 
                    'Lname':RequestObj.Username.Lastname, 
                    'Asset':RequestObj.Assigned_Device, 
                    'Request':RequestObj.id, 
                        'Condition':RequestObj.Assigned_Device.Asset_Condition,
                        'Availability':RequestObj.Assigned_Device.Availability,
                        'Current_user':AssignmentObj,
                        'Location': RequestObj.Assigned_Device.Location,
                        'Asset_Type': RequestObj.Assigned_Device.Asset_Type,
                        'link':link2
                        }
                            email_subject = f'Your request for a {RequestObj.Device_Type} has been Approved by IT'
                            email_body = f'Dear {RequestObj.Username.Firstname},\n IT department has Approved your request for a {RequestObj.Device_Type}. \
                            \n \n Comments: {RequestObj.AssetMangerApprovalComments}\
                                \n Next Approval Level: Financial Accounts'

                            email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[RequestObj.Username.email,])
                            EmailThread(email).start()

                            
                            email_subject = f'Request for Asset Assignment'
                            text_body = render_to_string("base/mail.txt", merge_data)
                            html_body = render_to_string("base/requestMail.html", merge_data)
                            
                            print(f'sending mail to {RequestObj.Username.Manager.email}')
                            msg = EmailMultiAlternatives(email_subject,text_body, from_email="helpdesk@psiug.org",
                                    to=[RequestObj.Username.Manager.email])
                            msg.attach_alternative(html_body, "text/html")
                            EmailThread(msg).start()
                            Events.objects.create(

                        EventType = "Asset Request",
                        EventSummary = f"{datetime.datetime.now()} : Staff {request.user} has approved {RequestObj.Username} \'s request for {RequestObj.Assigned_Device}"

                        )
                            messages.info(request, f"You have approved {RequestObj.Username}\'s request for {RequestObj.Assigned_Device}")
                            try:
                                Reject_others = AssetRequests.objects.filter(Q(Assigned_Device=RequestObj.Assigned_Device) 
                                                                            & Q(AssetManagerApproval="Pending"))
                                for i in Reject_others:
                                        print(f'The following items are being rejected: {i} request from {i.Username}')
                                        
                                        
                                        email_subject = f'Your request for a {i.Device_Type} has been Rejected'
                                        email_body = f'Dear {i.Username.Firstname} {i.Username.Lastname},\n \
                                            IT department has rejected your request for a {i.Device_Type}.\
                                                \n \n Reason: Another user was assigned the same device you requested'

                                        email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[i.Username.email,])
                                        EmailThread(email).start()
                                print (f'Count of other requests to be rejected {Reject_others}')
                                
                                if Reject_others.count() > 0:
                                    print(f'{Reject_others.count()} is greater than zero')
                                    Reject_others.update(Status="Rejected")
                                    Reject_others.update(AssetManagerApproval="Rejected")
                                    # print('Items rejected')
                                    Emails= []
                                    
                                
                                        
                                else:
                                    print(f'No count {Reject_others.count()}') 
                                    

                            except Exception as e:
                                print({e})
                                messages.error(request, f'An exception occured here{e}')     
                        except Exception as e:
                            print(f'Another exception occured here{e}')
                            messages.error(request, f"Requested Action Failed (1). Contact \
                        Systems Administrator. Error: {e}")
                
            
                    elif Approver.staffrole == "Asset Manager" and RequestObj.AssetManagerApproval == "Approved":
                        '''Checking if Logged in User is the Asset Manager'''
                        merge_data = { 
                'Fname':RequestObj.Username.Firstname, 
                'Lname':RequestObj.Username.Lastname, 
                'Asset':RequestObj.Assigned_Device, 
                'Request':RequestObj.id, 
                    'Condition':RequestObj.Assigned_Device.Asset_Condition,
                    'Availability':RequestObj.Assigned_Device.Availability,
                    'Current_user':AssignmentObj,
                    'Location': RequestObj.Assigned_Device.Location,
                    'Asset_Type': RequestObj.Assigned_Device.Asset_Type,
                    'link':link2
                    }
                        try:
                            RequestObj.FinanceManagerApproval =  'Approved'
                            RequestObj.Status = 'Fully Approved'
                            RequestObj.FinanceManagerApprovalComments =  request.POST['FinanceManagerApprovalComments']
                            RequestObj.Last_Modified = datetime.date.today()
                            RequestObj.save()
                            email_subject = f'Your request for a {RequestObj.Device_Type} has been Approved by Financial Accounts'
                            email_body = f'Dear {RequestObj.Username.Firstname},\n Assets Manager {AssetManager.Username} has Approved your request for a {RequestObj.Device_Type}. \
                            \n \n Comments: {RequestObj.FinanceManagerApprovalComments}\
                                \nNext Approval Level: Fully Approved. \n\
                                Log into your account and accept device then proceed to pick it from IT'

                            email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[RequestObj.Username.email,])
                            EmailThread(email).start()
                            email_subject = f'Request for Asset Assignment'
                            text_body = render_to_string("base/mail.txt", merge_data)
                            html_body = render_to_string("base/requestMail.html", merge_data)
                            
                            print(f'sending mail to {Approver.email}')
                            msg = EmailMultiAlternatives(email_subject,text_body, from_email="helpdesk@psiug.org",
                                    to=[Approver.email])
                            msg.attach_alternative(html_body, "text/html")
                            EmailThread(msg).start()
                            Events.objects.create(

                        EventType = "Asset Request",
                        EventSummary = f"{datetime.datetime.now()} : Staff {request.user} has approved {RequestObj.Username} \'s request for {RequestObj.Assigned_Device}"


                        )
                            messages.info(request, f"You have approved {RequestObj.Username}\'s request for {RequestObj.Assigned_Device}")
                            return redirect('homepage')
                        except Exception as e:
                            print({e})
                            messages.error(request, f"Requested Action Failed-(2). Contact \
                            Systems Administrator. Error: {e}")
                            return redirect('homepage')
                            
                else:
                    """Rejection Else"""
                    print('rejected')
                    try: 
                        if Approver.staffrole =='Admin' or Approver.staffrole == 'IT Support Assistant':
                            RequestObj.AssetManagerApproval =  'Rejected'
                            RequestObj.AssetMangerApprovalComments =  request.POST['AssetManagerApprovalComments']
                            RequestObj.save()
                            messages.error(request, f"Request Rejected Successfully")
                            email_subject = f'Your request for a {RequestObj.Device_Type} has been Rejected'
                            email_body = f'Dear {RequestObj.Username.Firstname},\n IT department has rejected your request for a {RequestObj}. \
                                \n \n Reason: {RequestObj.AssetMangerApprovalComments}'

                            email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[RequestObj.Username.email,])
                            EmailThread(email).start()
                            Events.objects.create(

                        EventType = "Asset Request",
                        EventSummary = f"{datetime.datetime.now()} : Staff {request.user} has Rejected {RequestObj.Username} \'s request for {RequestObj.Assigned_Device}"


                        )
                            messages.info(request, f"You have rejected {RequestObj.Username}\'s request for {RequestObj.Assigned_Device}")
                            return redirect('homepage')
                        elif Approver.staffrole == "Asset Manager":
                            RequestObj.FinanceManagerApproval =  'Rejected'
                            RequestObj.FinanceManagerApprovalComments =  request.POST['FinanceManagerApprovalComments']
                            RequestObj.save()
                            messages.error(request, f"Requested Rejected Successfully")
                            email_subject = f'Your request for a {RequestObj.Device_Type} has been Rejected'
                            email_body = f'Dear {RequestObj.Username.Firstname},\n Assets Manager {AssetManager.Username} has rejected your request for a {RequestObj}.\
                                \n \n Reason: {RequestObj.FinanceManagerApprovalComments}'

                            email=EmailMessage(email_subject,email_body,'helpdesk@psiug.org',[RequestObj.Username.email,])
                            EmailThread(email).start()
                            Events.objects.create(

                        EventType = "Asset Request",
                        EventSummary = f"{datetime.datetime.now()} : Staff {request.user} has Rejected {RequestObj.Username} \'s request for {RequestObj.Assigned_Device}"


                        )
                            messages.info(request, f"You have rejected {RequestObj.Username}\'s request for {RequestObj.Assigned_Device}")
                            return redirect('homepage')
                        else:
                            print("Rejection Failed")
                            messages.error(request, f"Requested Action Failed (3). Contact \
                            Systems Administrator.")
                            return redirect('homepage')
                    except Exception as e:
                            print({e})
                            messages.error(request, f"Requested Action Failed (4). Contact \
                            Systems Administrator. Error: {e}")
                            return redirect('homepage')
                

            

            # messages.success(request,"Your Password has been reset successfully")

            # return redirect('homepage')
        except Exception as e:
            context = {'uidb64':uidb64,
            'token':token
           , 'pk':pk ,'AssignedObjects':AssignedObjects,'pooleddevices':pooleddevices,'myform': myform, "RequestObj":RequestObj,"MyValues":request.POST.values()}

            # return render(request, "base/Approve_Pool_Request.html", context)

            messages.info(request,"Action not successful. Contact Systems Administrator")
            print(f'Error is {e}')
            return render(request, 'base/Approve_Pool_Request.html', context)



   
def handover(request):
    
    #  AssetTb.objects.filter(Ast_Tag_nbr=AssignmentObj.Ast_Tag_nbr).update(Availability="AVAILABLE")
    if request.method == 'POST':
        search_str = json.loads(request.body).get('pk')
        # AssignmentObject =  Assignment.objects.get(Ast_Tag_nbr=request.POST.get('Ast_Tag_nbr'))
        AssignmentObject =  Assignment.objects.get(Ast_Tag_nbr=search_str)
        
        if DeleteAssignment.objects.filter(AssignmentID=AssignmentObject.id).exists():
            return JsonResponse({"Message":"You have already handed over device. Wait for Acceptance confirmation"},safe=False)
        else:
            DeleteAssignment.objects.create(
                AssignmentID = AssignmentObject.id
            )
            data = [{
                "Message":"Device Returned. Wait for confirmation"
            }]
            return JsonResponse(data, safe=False)
    
    else:
        print(request.POST)
        data = [
                request.body
            ]
        return JsonResponse(data, safe=False)