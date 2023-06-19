import datetime
from datetime import datetime, date
from shutil import ExecError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from home.models import AssetTb, Assignment, Events, staff, Ajaxsend, Disposal
from django.contrib import messages
from django.shortcuts import render, redirect
from home.logindecorators import *
from assets.forms import disposalCommentsForm,auctionForm
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Avg,Count, Sum, Min,Max
from home.logindecorators import *
import xlsxwriter
import io

@login_required(login_url='login')
@allowed_users(allowed_roles=['Finance','Admin', 'Asset Managers', 'IT','EMT','Accountant','Finance Managers','Procurement'])
def auctions(request):
    ForDisposal = AssetTb.objects.filter(Availability__iexact="Due for Disposal").order_by("Asset_Type")
    
    
    disposalObj = AssetTb.objects.filter(Q(disposal__CR_Approval="Pending"))
    # .prefetch_related("Ast_Tag_nbr").annotate(Disp=Count("Ast_Tag_nbr__Ast_Tag_nbr"))
    
    disposalObjcount = disposalObj.count()
    context = {"disposalObj": disposalObj, "disposalObjcount": disposalObjcount}
    return render(request, 'base/disposal_list.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Asset Managers', 'IT','EMT','Accountant','Finance Managers', 'Procurement'])
def auction_list(request):

    #Auction_items = Disposal.objects.all().prefetch_related('Ast_Tag_nbr')
    Auction_items = Disposal.objects.filter(CheckedOut=True).prefetch_related('Ast_Tag_nbr').order_by("Ast_Tag_nbr__Asset_Type")

    
    Total_purchase_Value = 0
    TIR = 0.0

    for item in Auction_items:

        TIR = float(item.disposalIncome + TIR)
    
    for item in Auction_items:
        Total_purchase_Value = item.Ast_Tag_nbr.Item_Cost_UGX+Total_purchase_Value

    
    
    context = {'Auction_items':Auction_items, 'TPV':Total_purchase_Value, 'TIR':TIR}
    
    

   
    
    return render(request, 'base/AuctionList.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Asset Managers', 'IT'])
def dispose(request, pk):

    Disposal_item = AssetTb.objects.get(Ast_Tag_nbr = pk)
    
        
    #if 'term' in request.GET:
        

    form =  disposalCommentsForm(instance = Disposal_item)
    
    
    if request.method == 'POST':
        
        # disposalObj = Disposal.objects.get(Ast_Tag_nbr = pk)
        
        # form = disposalCommentsForm(request.POST, request.FILES)
        
        Explanation = request.POST['disposalExplanation']
        SalvageAmount =request.POST['fairMarketValue']
        # disposalAttachment = request.FILES['attachment']
        
        
        
        try:
            if not Disposal.objects.filter(Ast_Tag_nbr=pk).exists():
                disposalObj=Disposal.objects.create(
                    Ast_Tag_nbr = AssetTb.objects.get(Ast_Tag_nbr=request.POST['Ast_Tag_nbr']),
                    fairMarketValue = SalvageAmount,
                    disposalExplanation = Explanation,
                    
                   

        ) 
                Events.objects.create(
            EventType = "Asset Added to disposal list",
            EventSummary = f"{datetime.now()} : User {request.user}  added {disposalObj} to the disposals list"
                    
                    # attachment=disposalAttachment
                    
                )
            else:
                disposalObj = Disposal.objects.filter(Ast_Tag_nbr=pk).update(
                    fairMarketValue = SalvageAmount,
                    disposalExplanation = Explanation,
                    # attachment=disposalAttachment,
                    CR_Approval="Pending"
                )
                            
        except Exception as e:
            messages.info(request,f"{e}")
        
        
        # if form.is_valid():
        #     form.save()
        #     disposalObj = Disposal.objects.get(Ast_Tag_nbr = request.POST['Ast_Tag_nbr'])
            
            
        #     messages.info(request, f"form is valid")

            # Add update logic which shouldn't be a form.save

            # disposalObj.disposalExplanation = form.cleaned_data.get('disposalExplanation')
            # disposalObj.fairMarketValue = form.cleaned_data.get('fairMarketValue')
            # #disposalObj. = form.cleaned_data.get('fairMarketValue')

            # #Remove the attachment and have it attached during the auction stage. No reason for attaching it to fill our database and yet it could be rejected anyway.

            # disposalObj.attachment = 

            
            
        messages.info(request, f"Asset has has been added to the Assets for disposal list")
    # else:
    #     messages.info(request, f" Could not be added")


        Disposal_item.Availability = "DUE FOR DISPOSAL"

        Disposal_item.save()
        return redirect('reports_all')
    
    depreciatedvalue =  depreciation(request,pk)
        
    context = {'form':form, "depreciation": depreciatedvalue}
        # return redirect('disposal')
    return render(request, 'base/disposalcomments.html', context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Asset Managers', 'IT','EMT',])   
def crApprovalList(request):

    ApprovalObjects = Disposal.objects.filter(CR_Approval='Pending')


    context = {'ApprovalObjects':ApprovalObjects}

    return render (request, 'base/crapprovallist.html', context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'IT','EMT'])
def crApproval(request, pk):
    
    ApprovalObject = Disposal.objects.get(Ast_Tag_nbr=pk)

    form = disposalCommentsForm(instance=ApprovalObject)

    todays_date =  date.today()
    num_days = todays_date-ApprovalObject.Ast_Tag_nbr.PurchaseDate
    num_days = num_days.days
    stringify =  str(num_days)
    years = f'{num_days/365:10.1f}'

    if request.method == 'POST':
        form = disposalCommentsForm(request.POST, instance=ApprovalObject)
        if form.is_valid():
            form.save()
            ApprovalObject.CR_Approval='Approved'
            ApprovalObject.save()
            messages.info(request, "You have approved this item for disposal")
            Events.objects.create(
            EventType = "Item disposal Approved",
            EventSummary = f"{datetime.now()} : User {request.user} approved an asset {ApprovalObject.Ast_Tag_nbr} for disposal")
        else:
            messages.info(request, "Item could not be added on the list. Check with Systems Administrator")
            
        return redirect('crapprovallist')

    context = {'ApprovalObject': ApprovalObject,'form':form,'years':years}
    
    return render (request, 'base/crapproval.html', context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','IT','EMT'])
def crReject(request, pk):
    '''Method to reject an item from being disposed and removed from the disposal list'''
    
    ApprovalObject = Disposal.objects.get(Ast_Tag_nbr=pk)

    form = disposalCommentsForm(instance=ApprovalObject)

    todays_date =  datetime.date.today()
    num_days = todays_date-ApprovalObject.Ast_Tag_nbr.PurchaseDate
    num_days = num_days.days
    stringify =  str(num_days)
    years = f'{num_days/365:10.1f}'

    if request.method == 'POST':
        form = disposalCommentsForm(request.POST, instance=ApprovalObject)
        if form.is_valid():
            form.save()
            ApprovalObject.CR_Approval='Rejected'
            ApprovalObject.save()
            messages.info(request, "You have rejected this items disposal request")
            Events.objects.create(
            EventType = "Item Disposal rejected",
            EventSummary = f"{datetime.now()} : User {request.user} approved an asset {ApprovalObject.Ast_Tag_nbr} for disposal")
        else:
            messages.info(request, "Error occured. Check with Systems Administrator")
            
        return redirect('crapprovallist')


    context = {'ApprovalObject': ApprovalObject,'form':form,'years':years}
    
    return render (request, 'base/crrejection.html', context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','IT','EMT','Accountant','Finance Managers'])
def remove(request, pk):
    disposalObject = AssetTb.objects.get(Ast_Tag_nbr=pk)

    # disposalObject.Asset_Condition = ""
    disposalObject.Availability = "AVAILABLE"

    disposalObject.save()
    disposalObj = AssetTb.objects.filter(Asset_Condition="DUE FOR DISPOSAL")
    disposalObjcount = disposalObj.count()
    
    try:
        Disposal.objects.get(Ast_Tag_nbr=pk).delete()

        context = {"disposalObj": disposalObj, "disposalObjcount": disposalObjcount}
        messages.info(request, f"{disposalObject} has been removed from the disposal list")
        Events.objects.create(
                EventType = "Edit/Change Event",
                EventSummary = f"{datetime.now()} : User {request.user} removed an asset {disposalObject.Ast_Tag_nbr} from the disposal list")
        #return render(request, 'base/listing.html', context)
    except Exception as e:
        messages.error(request, f"Error Contact Admin: Error Description: {e}")

    return redirect('disposal')
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'IT','Finance Managers', 'Procurement'])
def asset_auction(request,pk):
    '''Method for auctioning items'''
    ApprovalObject = Disposal.objects.get(Ast_Tag_nbr=pk)  #.prefetch_related('Ast_tag_nbr')
    AssetObj = AssetTb.objects.get(Ast_Tag_nbr=pk)
    # ------------------------------------------------------------------
    
    if request.method=='POST':
        form = auctionForm(request.POST,request.FILES,instance=ApprovalObject)
        if form.is_valid():
            form.save()
            
            AssetObj
            messages.info(request, "Item sale completed")
            AssetObj.Availability="DISPOSED-OF"
            AssetObj.Location="DISPOSED-OF"
            AssetObj.Asset_Status="VERIFIED"
            AssetObj.save()
            try:
                ApprovalObject.CheckedOut=True
                ApprovalObject.save()
            except Exception as e:
                messages.error(request, f"{e}")
            
            Events.objects.create(
            EventType = "Item Auctioned",
            EventSummary = f"{datetime.now()} : User {request.user} added flag \'AUCTIONED\' an asset {ApprovalObject.Ast_Tag_nbr}")
            try:
                Device = Assignment.objects.get(Ast_Tag_nbr=AssetObj.Ast_Tag_nbr)
                messages.info(request,  f"Device assignment removed from {Device.Username}'s devices")
                Device.delete()
                return redirect('auction-list')
            except Exception as e:
                messages.error(request,f"Device not assigned to any user. Could not be unassigned: Error: {e}")
                
                return redirect('auction-list')
            
            
        else:
            messages.error(request, f"Item sale could not be completed")
            
            
    form = auctionForm(instance=ApprovalObject)

    context = {'ApprovalObject': ApprovalObject,'form':form,}
    
    return render(request, 'base/AuctionSingleItem.html',context)






def asset_auction_list(request):
    '''Lists approved items for auction so that Finance / Procurement staff can log in and adding details like item selling price'''

    items =  Disposal.objects.filter(CheckedOut="False").prefetch_related('Ast_Tag_nbr').order_by("Ast_Tag_nbr").order_by("Ast_Tag_nbr__Asset_Type")
    
    # for item in items:
    #     item.disposalDate=date(2022,11,11)
    
    if request.method=="POST":
        # print(request.)
        Ast_Tag = request.POST.get("Ast_Tag")
        items = Disposal.objects.filter(Q(Ast_Tag_nbr__Ast_Tag_nbr__icontains=Ast_Tag) |
                                     Q(Ast_Tag_nbr__Ast_Tag_nbr__iexact=Ast_Tag) |
                                     Q(Ast_Tag_nbr__Asset_Type__iexact=Ast_Tag) |
                                     Q(Ast_Tag_nbr__Asset_Type__icontains=Ast_Tag) |
                                     Q(Ast_Tag_nbr=Ast_Tag), CheckedOut="False"
                                     ).prefetch_related('Ast_Tag_nbr').order_by("Ast_Tag_nbr").order_by("Ast_Tag_nbr__Asset_Type")
    
    

        

    context={'items':items, 'values':request.POST}
    
    

    return render(request, 'base/auction-items.html', context)
def Export(request):
    items =  Disposal.objects.filter(CheckedOut="False").prefetch_related('Ast_Tag_nbr')
    
    # 'Disposal-List.xlsx'
    output = io.BytesIO()
    
    workbook = xlsxwriter.Workbook(output,{'in_memory': True})
    worksheet = workbook.add_worksheet()
    columns =  [
        'AST-TAG-NBR',
        'ASSET-TYPE',
        'CONDITION',
        'AST-DESCRIPTION',
        'MODEL',
        'LOCATION', 
        'ACTIVITY',
        'Cost (UGX)',
        'Cost_USD',  
        'FAIR MARKET VALUE (UGX)',
        'PURCHASE DATE',
        'DISPOSAL COMMENTS',
        
                    
                ]
    rows = items.values_list(
            'Ast_Tag_nbr',
            'Ast_Tag_nbr_id__Asset_Type',
            'Ast_Tag_nbr_id__Asset_Condition',
            'Ast_Tag_nbr_id__Ast_description',
            'Ast_Tag_nbr_id__Model_No',
            'Ast_Tag_nbr_id__Location',   
            'Ast_Tag_nbr_id__Project_Name',
            'Ast_Tag_nbr_id__Item_Cost_UGX',
            'Ast_Tag_nbr_id__Item_Cost_USD',
            'fairMarketValue',
            'Ast_Tag_nbr_id__PurchaseDate',
            
            'disposalExplanation', )
    
    headerFormat = workbook.add_format({'bold':True})
    currency_format = workbook.add_format({'num_format': '#,##0.00'})
    currency_format2 = workbook.add_format({'num_format': '$#,##0.00'})
    row = 0
    col = 0
    # print(len(columns))
    # worksheet.write(row+3, col,row)
    for col_num in range(len(columns)):
        # print(columns[9])
        worksheet.write(row, col_num+1, columns[col_num],headerFormat)
        
        
    for row_item in rows:
        worksheet.write(row+1, col,row+1)
        row+=1
        for col_num in range(len(row_item)):
           
            if col_num == 8:
                print(f'currency {row_item[col_num]}')
                ausd = row_item[col_num]
                worksheet.write(row, col_num+1, ausd,currency_format2)
            
            elif col_num == 7 or col_num == 9:
                print(f'currency {row_item[col_num]}')
                ausd = row_item[col_num]
                worksheet.write(row, col_num+1, ausd,currency_format)
            elif col_num == 10:
                
                # print(f'I am row {row_item[col_num]}')
                # mydate = datetime(row_item[col_num])
                # print(mydate)
                date = datetime.strptime(str(row_item[col_num]), "%Y-%m-%d")
                date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})
                worksheet.write(row, col_num+1, date,date_format)
            else:
                worksheet.write(row, col_num+1, row_item[col_num])
        # row+=1
    workbook.close()
    output.seek(0)
    filename = 'django_simple.xlsx'
    response = HttpResponse(
    output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


    

def dynamicadd(request):
    items = AssetTb.objects.all()

    context = {'items': items}

    return render(request, 'base/Dynamicadd.html', context)


def testsDataAPI(s):
    data = AssetTb.objects.all()

    # data = ProductsSerializer(data).data

    for i in data:
        PP = i.PName
        dataList = []
        print(PP)

        dataList.append({'name': PP, 'result': i.available_quantity,
                         'description': i.Expirydate, })

    return JsonResponse(dataList, safe=False)


@csrf_exempt
def createItem(request):
    if request.method == 'POST':
        Ast_Tag_number = request.POST.get('Ast_Tag_nbr')
        Serial_Number = request.POST.get('Serial_No')
        Lawson_Asset_Number = request.POST.get('Lawson_Asset_No')
        Asset_description = request.POST.get('Ast_description')
        UGX = request.POST.get('Item_Cost_UGX')
        USD = request.POST.get('Item_Cost_USD')
        Type = request.POST.get('Asset_Type')
        Model_Number = request.POST.get('Model_No')
        ProjectCode = request.POST.get('Project')
        Condition = request.POST.get('Asset_Condition')
        Status = request.POST.get('Asset_Status')
        ProjectName = request.POST.get('Project_Name')
        # Username = staffobj,
        Available = request.POST.get('Availability')
        location = request.POST.get('Location')
        purchaseDate = request.POST.get('PurchaseDate')

        AssetTb.objects.create(
            Ast_Tag_nbr=Ast_Tag_number,
            Serial_No=Serial_Number,
            Lawson_Asset_No=Lawson_Asset_Number,
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
            PurchaseDate=purchaseDate,

        )
    return JsonResponse('Test Created!', safe=False)


@csrf_exempt
def updateItem(request):
    objId = request.POST.get('id')
    result = request.POST.get('result')

    test = Ajaxsend.objects.get(id=objId)
    test.result = result
    test.save()

    return JsonResponse('Test Updated!', safe=False)


@csrf_exempt
def deleteItem(request):
    print('Delete called!')
    objId = request.POST.get('id')
    test = Ajaxsend.objects.get(id=objId)
    test.delete()

    return JsonResponse('Test Deleted!', safe=False)


@csrf_exempt
def dynadd(request):
    items = AssetTb.objects.all()

    context = {'items': items}
    for item in items:
        print(item)
    return render(request, 'base/itemadd.html', context)


def depreciation(request,Ast_Tag_nbr):
    try:
        AssetObj = AssetTb.objects.filter(Ast_Tag_nbr=Ast_Tag_nbr).get()
        
        BookValue=0.0
        Salvage = 0.0
        Life = 0
        k=0.0
        Dep=0.0
        Total_Depreciation=0.0
        Actual_Dep_Per_year=0.0
        print(AssetObj.PurchaseDate)
        todays_date =  datetime.date.today()
        num_days = todays_date-AssetObj.PurchaseDate
        num_days = num_days.days
        print (num_days)
        # stringify =  str(num_days)
        Life = num_days/365
        Life = int(Life)
        print(f"{Life} years")

        if AssetObj.Asset_Type == "LAPTOP":
            Salvage=200000
            
        elif AssetObj.Asset_Type == "DESKTOP":
            
            Salvage=150000
        elif AssetObj.Asset_Type == "SERVER":
            Salvage=10000000
        elif AssetObj.Asset_Type == "VEHICLE":
            Salvage=20000000
        elif AssetObj.Asset_Type == "INVERTER":
            Salvage=600000
        elif AssetObj.Asset_Type == "SWITCHES":
            Salvage=350000
        elif AssetObj.Asset_Type == "AIR CONDITIONER":
            Salvage=400000
        elif AssetObj.Asset_Type == "REFRIGERATOR":
            Salvage=400000
        elif AssetObj.Asset_Type == "PHOTOCOPIER":
            Salvage=400000
        elif AssetObj.Asset_Type == "TENT":
            Salvage=350000
            
        else:
            Salvage = 130000
        BookValue = AssetObj.Item_Cost_USD
        BookValue2 = AssetObj.Item_Cost_UGX
        ItemsList = []
            
        for k in range (0, Life):
            Dep = ((BookValue2-Salvage)*k)/Life 
            Actual_Dep_Per_year = ((BookValue2-Salvage)* (Life-k))/Life
            
            print(f"{Dep}---------------------{Actual_Dep_Per_year}")
            
            # ItemsList.append({
            #     f'{AssetObj}':[Dep,Actual_Dep_Per_year]
            # })
            if Life-k == 1:
                Total_Depreciation +=  Actual_Dep_Per_year
                messages.info(request,f"{Total_Depreciation}")
    except Exception as e:
        messages.info(request,message=f"{e}")
    return int(Total_Depreciation)
