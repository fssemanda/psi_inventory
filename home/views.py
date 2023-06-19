# from audioop import avg
from datetime import datetime, timedelta
from genericpath import exists
#from dateutil.relativedelta import relativedelta
import time
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.views import generic
#from django_auth_ldap.backend import LDAPBackend
from django.http import JsonResponse
from assets.forms import CreateUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .logindecorators import *
from django.contrib.auth.models import Group
from django.db.models import Q, F, Sum,Count,Avg,Min
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.views import View
from sqlparse import tokens
from base64 import urlsafe_b64decode, urlsafe_b64encode
#from .MyLDAPBackend import MyLDAPBackend
from django.core.mail import EmailMultiAlternatives,EmailMessage
from .models import *
from random import randint, random, choice, sample,shuffle,seed
import threading
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

@unauthorizedUser_func
def LoginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #user = LDAPBackend().authenticate(request,username=username, password=password)
        user = authenticate(request,username=username, password=password)
        print(user)

        # if user is not None:
        #     login(request, user,backend='django_auth_ldap.backend.LDAPBackend')
        #     return redirect('homepage')
        # else:
        #     messages.info(request, 'Invalid login/Password')

        if user is not None:
            login(request, user)
            Events.objects.create(

            EventType = "Log in Event",
            EventSummary = f"{datetime.now()} : User {request.user} logged in successfully"

        )

            return redirect('/')
        else:
            messages.info(request, 'Invalid login/Password')
    context = {}

    return render(request,'base/login.html', context)

@unauthorizedUser_func
# def RegisterPage(request):
#     RegisterForm = CreateUserForm()
#
#     if request.method == 'POST':
#         RegisterForm = CreateUserForm(request.POST)
#         if RegisterForm.is_valid():
#
#             user=RegisterForm.save()
#
#             uname = RegisterForm.cleaned_data.get('username')
#
#             group = Group.objects.get(name='staffgrp')
#
#             user.groups.add(group)
#
#             staff.objects.create(
#                 Username = user,
#
#
#             )
def RegisterPage(request):
    myform = CreateUserForm()

    if request.method == "POST":
        myform = CreateUserForm(request.POST)
        if myform.is_valid():
            user = myform.save()
            uname = myform.cleaned_data.get('username')

            messages.success(request, 'Successfully Created user ' + uname)

            Events.objects.create(

                EventType = "Account Creation",
                EventSummary = f"{datetime.now()} : User Account {uname} created"

            )

            return redirect('login')



    context = {'myform': myform}
    return render(request, "base/register.html", context)


def Logout(request):
    Events.objects.create(

    EventType = "Log out Event",
    EventSummary = f"{datetime.now()} : User {request.user} logged out"
    )
    logout(request)
    


    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    myGroups = request.user.groups.all()[0].name    
    
    # AssetTb.objects.filter(Q(Availability__icontains="DUE FOR DISPOSAL") ,Asset_Type__icontains="TABLET").update(Asset_Status="VERIFIED")
    # AssetTb.objects.filter(Q(assignment__Username="pmasson")).update(Location="CR'S OFFICE")

    # AssetRequests.objects.filter(Assigned_Device="PACE-LP-WHP-46").update(AssetManagerApproval="Pending")
    # AssetRequests.objects.filter(Assigned_Device="PACE-LP-WHP-46").update(Status="Pending")
    # AssetRequests.objects.filter(Assigned_Device="PACE-LP-WHP-46").update(AssetManagerApproval="Pending")
    
    # finder = AssetTb.objects.filter(Ast_Tag_nbr__icontains="PSI/").delete()
    # print(finder)

    # a = Assignment.objects.all()
    
    # for i in a:
    #     AssetTb.objects.filter(Ast_Tag_nbr = i.Ast_Tag_nbr).update(Availability="ASSIGNED")
    
    excludes = ['Lost', 'Missing', 'Disposed-of', 'Disposed-Off', 'DISPOSED-OF', "DISPOSED-OFF",'Due for Disposal']
    #Total_Assets_count = AssetTb.objects.all().count()
    Total_Assets =AssetTb.objects.all().\
        exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).order_by('-PurchaseDate', '-Ast_Tag_nbr')
    inventory_count = AssetTb.objects.all().\
        exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).count()
    asset_requests = AssetRequests.objects.filter(AssetManagerApproval = "Pending")
    processing = AssetRequests.objects.filter(Status = "In Process")
    asset_requests_count =  AssetRequests.objects.filter(Status = "Pending")
    employee = staff.objects.filter(staff_status=True).order_by('Username')
    AssignmentDeletionObj = DeleteAssignment.objects.all().count()
    crApprovalObjects = Disposal.objects.filter(CR_Approval='Pending').count()

    

    paginator = Paginator(employee, 6)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    mylist=[]
    Assets = AssetTb.objects.all().order_by('Ast_Tag_nbr','Location')\
    .exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes)
    ModObjects = ChangeLog.objects.filter(FAMApproval='Pending').count()
    # print(ModObjects)
    for item in Assets:
        mylist.append(item.Item_Cost_USD)
    Total = (sum(mylist))

    Dimes=AssetTb.objects.all().\
        exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).aggregate(Dimes=Sum('Item_Cost_USD'))
        
    # print(Dimes.values())

    above_5years = []

    todays_date =  datetime.date(datetime.today())
    num_days = 0
    for item in Total_Assets:
        #purchaseDate = datetime.date(item.PurchaseDate)
        #print(todays_date)
        #print(item.PurchaseDate)
       
        num_days = todays_date-item.PurchaseDate
        num_days = num_days.days
        stringify =  str(num_days)
        # Checking if the difference between today and the purchase date is larger than 5 years
        #print(stringify)
        if num_days >= 1825:
            #print((num_days))
            #print(item)
            above_5years.append(item.Ast_Tag_nbr)
    above_5years_count=len(above_5years)
    excludes = ['Lost', 'Missing', 'Disposed-off','Disposed-of',]
    AssetObj = AssetTb.objects.all().\
        exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes)
    BookValue=0.0
    Salvage = 0.0
    Life = 5
    k=0.0
    Dep=0.0
    Total_Depreciation=0.0
    Actual_Dep_Per_year=0.0
    
    Date = AssetObj.aggregate(MinimumDate=Min('PurchaseDate'))
    
    # print(Date.values)
    items = AssetTb.objects.filter(PurchaseDate__lte= "2006-09-24")
    # print(items)
    # print(items.count())
    
    # for item in Date:
    #     print(item.MinimumDate)
    
    for asset in AssetObj:
        if asset.Asset_Type == "LAPTOP":
            Salvage=100.0
            
        elif asset.Asset_Type == "DESKTOP":
            Salvage=50.0
        elif asset.Asset_Type == "SERVER":
            Salvage=3000.0
        elif asset.Asset_Type == "VEHICLE":
            Salvage=8000.0
        elif asset.Asset_Type == "INVERTER":
            Salvage=200.0
        elif asset.Asset_Type == "SWITCHES":
            Salvage=100.0
        elif asset.Asset_Type == "AIR CONDITIONER":
            Salvage=150.0
        elif asset.Asset_Type == "REFRIGERATOR":
            Salvage=150.0
        elif asset.Asset_Type == "PHOTOCOPIER":
            Salvage=150.0
        elif asset.Asset_Type == "TENT":
            Salvage=100.0
            Life = 7
        else:
            Salvage = 40
        BookValue = asset.Item_Cost_USD
        ItemsList = []

        
        
        for k in range (0, Life):
            Dep = ((BookValue-Salvage)*k)/Life 
            Actual_Dep_Per_year = ((BookValue-Salvage)* (Life-k))/Life
            
            ItemsList.append({
                f'{asset}':[Dep,Actual_Dep_Per_year]
            })
            if Life-k == 1:
                Total_Depreciation +=  Actual_Dep_Per_year
        
            
            # print (f'{asset}------{k}---------{Dep:,.2f}--------{Actual_Dep_Per_year:,.2f}')
            
    if request.method=='POST':
        name =  request.POST.get('uname')
        employee =  staff.objects.filter(Q(Username__icontains=name)|Q(Firstname__icontains=name)|Q(Lastname__icontains=name))
        paginator = Paginator(employee, 6)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)
        


    context={'Total_Depreciation':Total_Depreciation,'processing':processing,'Total_Assets': Total_Assets, 
             "Total_Assets":Total_Assets, 'Total': Total, 'employee':employee,"inventory_count":inventory_count,
             "Asset_Requests":asset_requests, "request_count":asset_requests_count, 'above_5years':above_5years,
             'above_5years_count':above_5years_count,'ModObjects':ModObjects, 'page_obj':page_obj,'AssignmentDeletionObj':AssignmentDeletionObj,'crApprovalObjects':crApprovalObjects,
             'myGroups':myGroups}

    return render(request, "base/home.html",context)


@login_required(login_url='login')
def staffFunction(request, uname):

    staffobj = staff.objects.get(Username=uname)
    AssignedDevices = staffobj.assignment_set.all()
    
    AssignedDevices_count = AssignedDevices.count()
    AssignedAssetsValue = AssignedDevices.aggregate(value=Sum("Ast_Tag_nbr_id__Item_Cost_USD"))
    
    myGroups = request.user.groups.all()[0].name    
    
    # if staffobj.staffrole == "Asset Manager":
    #     ApprovalRequests = Ass
    
    ApprovalRequests = AssetRequests.objects.all()
    if staffobj.staffrole == "Admin":
        ApprovalRequests = AssetRequests.objects.filter(Q(SupervisorApproval="Pending") | Q(FinanceManagerApproval="Pending"),
                                                        AssetManagerApproval="Pending" )
    elif staffobj.staffrole == "Asset Manager":
          ApprovalRequests = AssetRequests.objects.filter(
                                                          Q(AssetManagerApproval="Approved"), Q(FinanceManagerApproval="Pending")
                                                        )
    
    else:
        ApprovalRequests = AssetRequests.objects.filter(
        
       
         Q(FinanceManagerApproval="Pending") | Q(AssetManagerApproval="Pending"), Q(Username=staffobj)
                                                    
                                           
                                                    )
    print(ApprovalRequests.query)
    
    AcceptanceObj = AssetRequests.objects.filter(Q(Username=staffobj.Username) & Q(Status="Fully Approved"))
    
    context={'staffobj':staffobj,'AssignedDevices':AssignedDevices, 
             'AssignedDevices_count':AssignedDevices_count,
             'ApprovalRequests':ApprovalRequests, 'AssignedAssetsValue':AssignedAssetsValue,'AcceptanceObj':AcceptanceObj,
             'myGroups':myGroups
             }
    return render(request, "base/staff_Asset_details.html",context)


def switchUserType(request):
    
    # switch = staff.objects.get(user=request.user)
    
    myGroups = request.user.groups.all()[0].name
    print(myGroups)
    print(request.user.groups)
    
    
    
    if "IT" == myGroups or myGroups == "Finance":
        aGroup=Group.objects.get(name="IT")
        aGroup2=Group.objects.get(name="staff")
        request.user.groups.remove(aGroup)
        request.user.groups.add(aGroup2)
        return redirect('homepage')
    else:
        aGroup=Group.objects.get(name="IT")
        aGroup2=Group.objects.get(name="staff")
        request.user.groups.remove(aGroup2)
        request.user.groups.add(aGroup)
        return redirect('homepage')  


def baseview(request):

    context={}

    return render(request,'base.html',context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['Admin','Finance', 'IT',])
def stockView(request,pk):
    
    AssetObj =  AssetTb.objects.get(Ast_Tag_nbr=pk)

    if Assignment.objects.filter(Ast_Tag_nbr=AssetObj).exists():
        
        Current_User = Assignment.objects.filter(Ast_Tag_nbr=AssetObj).get()

        print(Current_User.id)

        context = {'AssetObj':AssetObj, 'Current_User':Current_User}

        return render(request, 'base/stockdetail.html', context)
    context = {'AssetObj':AssetObj,}
    return render(request, 'base/stockdetail.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['User'])
def my_staff(request, uname):
    staffobj = staff.objects.get(Username=uname)
    requisitions = staffobj.request_set.all()
    rqs = staffobj.assignment_set.all().count()



    ##requisitions = rqFilter.qs
    context = {'staffobj': staffobj, 'requisitions': requisitions, 'rqs': rqs,} #'rqFilter': rqFilter}
    return render(request, "base/staff.html", context)

def nonauthorizedview(request):

    return render(request, 'base/Notauthorized.html')

@unauthorizedUser_func
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Finance', 'IT',])
def assetAssignment(request):



    context={}
    return render(request, 'base/assetassignment.html', context)

def events(request):

    myevents = Events.objects.all()

    context={'myevents':myevents}
    
    return render(request, 'base/events.html', context)

def randomizer(request):
    AllStaff = staff.objects.all()
    staffList =[]
    for staffs in AllStaff:
        staffList.append(staffs.Username)
    seed(1)
    print(staffList)
    list1 = [1,2,4,5,7,3,0,9]
    print(list1)
    shuffle(staffList)
    print(staffList)
    
    return HttpResponse(request,list1)

class RequestPasswordResetEmail(View):
    
    def get(self,request):

        

        return render(request,'base/password_reset.html')

    def post(self,request):
        
        email = request.POST['email']

        print(email)

        context = {'values':request.POST,}

        # if not validate_email(str(email)):
        #     messages.error(request, "Please enter a valid Email")
            
        #     return render(request,'base/password_reset.html',context)

        current_site=get_current_site(request)

        user = User.objects.filter(email=email)

        if user.exists():
            email_contents ={
                'user':user[0],
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0]),


            }
            

            link = reverse('new-password',kwargs = {'uidb64': email_contents['uid'], 'token': email_contents['token']})

            email_subject = 'Password Reset Request'
            reset_url = 'http://'+current_site.domain+link

            email_body = f'Dear employee,\n\n Please follow this link to reset password\n'+reset_url


            

            email = EmailMessage(email_subject, email_body,'helpdesk@psiug.org',[user[0].email])
            
            EmailThread(email).start()

            messages.success(request, 'Password reset link has been sent')

            return render(request,'base/password_reset.html',context)

class PasswordReset(View):

    def get(self, request, uidb64, token):

        context = {
            'uidb64':uidb64,
            'token':token 
                   }
        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))

            print(user_id)

            user = User.objects.get(pk=user_id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, "Password Reset Link already used. Please request for new link")
                return redirect('login')
        except Exception as e:
            messages.info(request,"Password Reset Failed.")
            
            return render(request, 'base/set-new-password.html', context)

        return render(request, 'base/set-new-password.html', context)
    def post(self, request, uidb64, token):
        context = {
            'uidb64':uidb64,
            'token':token 
                   }

        password = request.POST['password']
        password2 = request.POST['password1']

        if password != password2:
            messages.error(request, "Passwords do not match")
            return render(request, 'base/set-new-password.html', context)
        if len(password) < 6:
            messages.error(request, "Password should be longer than 6 Characters")
            return render(request, 'base/set-new-password.html', context)
        
        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)
            print(user.last_name)
            print(password)
            user.set_password(password)
            user.save()

            messages.success(request,"Your Password has been reset successfully")

            return redirect('login')
        except Exception as e:
            messages.info(request,"Password Reset Failed. Contact HR or Systems Administrator")
            print(f'Error is {e}')
            return render(request, 'base/set-new-password.html', context)


class SetupUsers(View):
    
    def get(self, request):
        current_site=get_current_site(request)

        myList = User.objects.all()
        
        for listItem in myList:
            user = User.objects.get(username=listItem)

            # if user.exists():
            email_contents ={
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':PasswordResetTokenGenerator().make_token(user),

            }
            print(f'Username is {user}')

            link = reverse('new-password',kwargs = {'uidb64': email_contents['uid'], 'token': email_contents['token']})

            email_subject = 'Account setup for Asset Management System'
            reset_url = 'https://'+current_site.domain+link
            
            site_url = "https://inventory.psiug.org"

            email_body = f'Dear {user.first_name},\n\n An account has been created for you on the PSI Asset Management system. \n\n Your username is: {user} \n Please follow this link to setup your password\n'+reset_url+'\n\n For any assistance reach out to the Financial Accounts team or IT team. \n\n As per the earlier invitation sent out by the Financial accounts department, a training on how to use the system will take place on Tuesday \ as per the schedule in the invitation\n After successful account setup, you can visit'+site_url+' to access the system\n\n Regards, \n\n Sarah'


            

            email = EmailMessage(email_subject, email_body,'helpdesk@psiug.org',[user.email])
            
            EmailThread(email).start()

            messages.success(request, 'Invitation Email has been sent')

        return render(request,'base/password_reset.html')
    

def printUserForm(request,uname):
    
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
    # return render(request, "base/staff_Asset_details.html",)/

    
    return render(request, "home/UserForm.html", context)

def printPDF(request):
    
    """To be implemented"""
    
    return JsonResponse({"Message":"Works"}, safe=False)
    
    
    