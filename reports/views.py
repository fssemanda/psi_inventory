from queue import LifoQueue
import xlwt
from django.contrib import messages
import logging
from assets.forms import AddAssetForm
import datetime
from datetime import timedelta
import json

from django.http import JsonResponse, HttpResponse, response
from home.models import *
from django.db.models import query
from django.shortcuts import render
import csv
from django.core.paginator import Paginator
import tempfile
from django.template.loader import render_to_string
#from weasyprint import HTML
from django.db.models import Sum, Q,F, Count, Min,Max

logging.basicConfig(filename="ActivityLog.log",level=logging.INFO, format='%(levelname)s:%(lineno)d:%(asctime)s:%(message)s')

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

# Create your views here.

def check(variable):
    return variable != '' and variable is not None

def GetAsset(request):
    if request.method == 'GET':
        if 'term' in request.GET:
            qs = AssetTb.objects.filter(Ast_Tag_nbr__icontains=request.GET.get('term')) | AssetTb.objects.filter(AstNo__icontains=request.GET.get('term'))
            usernames =list()
            for singleAsset in qs:
                usernames.append(singleAsset.Ast_Tag_nbr)
            return JsonResponse(usernames,safe=False)
    return render(request,'base/testingjq.html')

def reports(request):

    #tabobjs = AssetTb.objects.filter(Ast_Tag_nbr__icontains="-TAB-").update(Asset_Status="UNVERIFIED")


# Bashir Kabuye
# Betty Nakabiito Musoke
# Joyce Zalwago
# Ben Kihika
# Jimmy Okot
# Lynette Awat
# Eunice Harriet Mulungi
# Raymond Mugirigi
# Ritah Namusisi
# Yusuf Ssebuuma
# Drati Amagu Samson
# Geofrey Ssekalembe
# Susan Acom
# Josephine Kasaija
# Ibra Kazibwe
# Majourine Nansasi
# Dauda Ziraba
# Daphne Kukunda
# Andrew Kironde
# Kenneth Wadenga
# Kenneth Kiiza
# Sarah Nansubuga
# Lilian Kyarikunda
# Martin Kazibwe
    # inactivestaff = ["ymugerwa", "smutono", "bkihika", "bmusoke", "dkukunda", "gssekalembe", "hkaula", "hmurungi", "ikazibwe",
    #                  "jnamitala", "jzalwango", "lkyarikunda", "kkiiza", "mdai", "rnamusisi", "rmugirigi", "yssebuuma","akironde","jokot"]
    # inactivestaff = ["one"]
    # for user in inactivestaff:
    #         staff.objects.filter(Username=user).update(staff_status=False)

    # myobj = AssetTb.objects.all()
    # for item in myobj:
    #     item.Vendor = item.Vendor.strip()
    #     item.save()

    # AssetTb.objects.filter(Availability="Disposed-of").update(Availability='DISPOSED-OF')

   # queryObj =  AssetTb.objects.all().order_by('-PurchaseDate', '-Ast_Tag_nbr')
    excludes = ['Lost', 'Missing', 'Disposed-off','DISPOSED-OF','DUE FOR DISPOSAL']
    # queryObj =  AssetTb.objects.all().select_related('assignment').order_by('Ast_Tag_nbr','Location')\
    # .exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes)
    # myform =  AddAssetForm(request.POST)

    
   
    excludes = ['Lost', 'Missing', 'Disposed-off','Disposed-of']
    AllObjects =  AssetTb.objects.select_related('assignment').all().order_by('-PurchaseDate', 'Ast_Tag_nbr')\
    .exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).order_by('Location')
    
    #print(queryObj.values_list())
    
    #queryObj =  AssetTb.objects.select_related('assignment')

    #queryObj = AssetTb.objects.prefetch_related('Assignment__username')#.annotate(returned=Count('assignment__Username'))
    queryObj = Assignment.objects.select_related('Ast_Tag_nbr').order_by('Username_id__Username', 'Ast_Tag_nbr')#\
    # .exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes)
    # .order_by('-PurchaseDate', 'Ast_Tag_nbr')\
    # .exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes)
    todays_date = datetime.date.today()
    year_ago = todays_date - datetime.timedelta(days=365)
    Three_Years_ago = todays_date - datetime.timedelta(days=365 * 3)
    Five_Years_ago = todays_date - datetime.timedelta(days=365 * 5)
    Desktops =  AssetTb.objects.filter(Asset_Type__iexact="Desktop").exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).count()
    Unusable_Desktops =  AssetTb.objects.filter(Q(PurchaseDate__lte=Five_Years_ago)|Q(Asset_Condition="Faulty")|
                                                Q(Asset_Condition='Bad') |  
                                                Q(Asset_Condition__iexact="Obsolete"), 
                                                Asset_Type__iexact="Desktop").exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).count()

    
    Desktops_Above =  AssetTb.objects.filter(Q(PurchaseDate__lte=Five_Years_ago)
      ).filter(Asset_Type__iexact="Desktop").exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).count()                                          
    
    
    Laptops =  AssetTb.objects.filter(Asset_Type__iexact="LAPTOP").exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).count()
    Unusable_Laptops =  AssetTb.objects.filter(Q(PurchaseDate__lte=Five_Years_ago)|Q(Asset_Condition="Faulty")| Q(Asset_Condition='Bad') |
     Q(Availability='Disposed-Of')
     
     | Q(Asset_Condition__iexact="Obsolete"),Asset_Type__iexact="Laptop").exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).count()

    Laptops_Above =  AssetTb.objects.filter(Q(PurchaseDate__lte=Five_Years_ago)
      ).filter(Asset_Type__iexact="Laptop").exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).count()
    
    #Consider using distinct maybe on select related to return just a single user even where a user is assgined more than 1 device.
    
    ActiveStaff = staff.objects.filter(staff_status=True).count()
    ActiveStaff_list = staff.objects.filter(staff_status=True)
    
    assignedDevices =  Assignment.objects.filter(Q(Ast_Tag_nbr__Asset_Type__iexact="Desktop") | Q(Ast_Tag_nbr__Asset_Type__iexact="Laptop")
    ,Q(Username__in=ActiveStaff_list)).aggregate(Num=Count('Username_id__Username', distinct=True))
    print(assignedDevices)
    # for user in assignedDevices.Num:
    #     print(user.Num)

    assignedDevicesList =  Assignment.objects.filter(Q(Ast_Tag_nbr__Asset_Type__iexact="Desktop") | Q(Ast_Tag_nbr__Asset_Type__iexact="Laptop"))
    
    todays_date = datetime.date.today()
    #print(todays_date)

    qs2= AssetTb.objects.all()
    filterObj = qs2.filter(Q(PurchaseDate__gte=year_ago) & Q(PurchaseDate__lte=todays_date),Asset_Type__iexact='Laptop').aggregate(Laptops_One_Year=Count('Asset_Type'))


    filterObj = qs2.filter(Q(PurchaseDate__gte=Three_Years_ago) & Q(PurchaseDate__lte=todays_date),Asset_Type__iexact='Laptop').aggregate(Laptops_Over_Three_Years=Count('Asset_Type'))
    #data2.append(filterObj)
    filterObj = qs2.filter(Q(PurchaseDate__gte=Five_Years_ago) & Q(PurchaseDate__lte=todays_date),Asset_Type__iexact='Laptop').aggregate(Laptops_Over_Five_Years=Count('Asset_Type'))
    #data3.append(filterObj)

    equipObj = Assignment.objects.filter(Q(Ast_Tag_nbr__Asset_Type__iexact="Desktop")
     | Q(Ast_Tag_nbr__Asset_Type__iexact="Laptop")).filter(
         Q(Ast_Tag_nbr_id__PurchaseDate__lte=Five_Years_ago)
      ,Username__in=ActiveStaff_list)
   
    equipObj1 = AssetTb.objects.filter(Q(Asset_Type__iexact="Desktop")
     | Q(Asset_Type__iexact="Laptop"
     )).exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).count()
   
    equipObj2 = AssetTb.objects.filter(Q(Asset_Type__iexact="Desktop")
     | Q(Asset_Type__iexact="Laptop") ).filter(
      Q(PurchaseDate__lte=Five_Years_ago
      )).exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).count()
    
    TotalAssigned = Assignment.objects.filter(Q(Ast_Tag_nbr__Asset_Type__iexact="Desktop")
     | Q(Ast_Tag_nbr__Asset_Type__iexact="Laptop") ).filter(Username__in=ActiveStaff_list).count()
    
    myuserlist=[]
    for item in assignedDevicesList:
        myuserlist.append(item.Username)
    # print(len(myuserlist))

    UserobjFilter = staff.objects.filter(~Q(Username__in=myuserlist) & Q(Username__in=ActiveStaff_list))
    # print(assignedDevicesList.count())
    # print(UserobjFilter.count())

    defects = AssetTb.objects.filter(Q(Asset_Type__iexact="Desktop")
     | Q(Asset_Type__iexact="Laptop")).filter( 
     Q(PurchaseDate__gte=Three_Years_ago) ,Asset_Condition="Faulty" ).exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes)
    
    # print(defects.query)

    dueForDisposal = AssetTb.objects.filter(Q(Asset_Type__iexact="Desktop")
     | Q(Asset_Type__iexact="Laptop")).filter(Q(PurchaseDate__lte=Five_Years_ago)|
         Q(Availability__iexact="Due for Disposal") & Q(Asset_Condition__iexact="Faulty")).exclude(Location__icontains 
         = 'PACE').exclude(Availability__in=excludes)

    # performing =  Assignment.objects.filter(Q(Ast_Tag_nbr__Asset_Type__iexact="Desktop")
    #  | Q(Ast_Tag_nbr__Asset_Type__iexact="Laptop") 
    #  ,Ast_Tag_nbr__PurchaseDate__lte=Five_Years_ago).annotate(
    #      Models=Sum('Ast_Tag_nbr__Item_Cost_USD', distinct=True))
    performing =  Assignment.objects.filter(Q(Ast_Tag_nbr__Asset_Type__iexact="Laptop")
    & Q(Ast_Tag_nbr__PurchaseDate__lte=Five_Years_ago)).annotate(
         Models=Sum('Ast_Tag_nbr__Item_Cost_USD', distinct=True))
    #AssetTb.objects.filter(Vendor='MELLINIUM').update(Vendor='MILLENNIUM INFOSYS')
    print(performing)

    Total_Faulty = AssetTb.objects.filter(Q(Asset_Type__iexact="Desktop")
     | Q(Asset_Type__iexact="Laptop")).filter(Q(PurchaseDate__lte=Five_Years_ago)|
         Q(Asset_Condition="Faulty")| 
         Q(Asset_Condition='Bad') |
         Q(Asset_Condition__iexact="Obsolete")
         ).exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).count()

    Total_Faulty_Above_Five = AssetTb.objects.filter(Q(Asset_Type__iexact="Desktop")
     | Q(Asset_Type__iexact="Laptop")).filter(Q(PurchaseDate__lte=Five_Years_ago)
      | Q(Availability__iexact="Due for Disposal")|
         Q(Asset_Condition="Faulty")| Q(Asset_Condition='Bad') | Q(Asset_Condition__iexact="Obsolete"
         )).exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).count()

    Total_Faulty_Above_Five_Laptops = AssetTb.objects.filter(Q(Asset_Type__iexact="Laptop"
    )).filter(Q(PurchaseDate__lte=Five_Years_ago)
      | Q(Availability__iexact="Due for Disposal")|
         Q(Asset_Condition="Faulty")| Q(Asset_Condition='Bad') | 
        Q(Asset_Condition__iexact="Obsolete")).exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).count()

    Total_Faulty_Above_Five_Desktops = AssetTb.objects.filter(Q(PurchaseDate__lte=Five_Years_ago)|
    Q(Asset_Condition="Faulty")| Q(Availability__iexact="Due for Disposal")|
    Q(Asset_Condition='Bad') | 
    Q(Asset_Condition="Obsolete"),Asset_Type__iexact="Desktop").exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).count()

    

    staff_no_device = []

    for item in ActiveStaff_list:
        if Assignment.objects.filter(Username = item.Username).exists():
            continue
        else:
            staff_no_device.append(item.Username)
    print(staff_no_device)

    Assigned = Assignment.objects.filter(Q(Ast_Tag_nbr__Asset_Type__iexact='Laptop') |
                                         Q(Ast_Tag_nbr__Asset_Type__iexact='Desktop') ).count() #| Q(Ast_Tag_nbr__Asset_Type__iexact='Laptop')

    Functional = AssetTb.objects.filter(Q(Asset_Type__iexact="Desktop")
     | Q(Asset_Type__iexact="Laptop")).filter(Q(PurchaseDate__gte=Five_Years_ago)
      & ~Q(Availability__iexact="Due for Disposal")&
         ~Q(Asset_Condition="Faulty") & ~Q(Asset_Condition='Bad') & ~Q(Asset_Condition__iexact="Obsolete"
         )).exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).count()

    Gap = ActiveStaff-Functional
    if Gap<0:
        Gap=0
    else:
        Gap=Gap
    myform =  AddAssetForm(request.POST)
  
    
    if request.method == 'POST':
        AstNbr = request.POST.get('search_name')
        Asset_Type = request.POST.get('Asset_Type')
        project = request.POST.get('Project_Name')
        fromdate = request.POST.get('from_date')
        todate = request.POST.get('to_date')
        mincost = request.POST.get('minimum_cost')
        maxcost = request.POST.get('maximum_cost')
        aging = request.POST.get('age')
        Condition = request.POST.get('Asset_Condition')
        Status = request.POST.get('Asset_Status')
        #ProjectName = request.POST.get('Project_Name')
        Available = request.POST.get('Availability')
        location = request.POST.get('Location')
        vendor = request.POST.get('vendor')


        if AstNbr != "" and AstNbr is not None:
            #queryObj = Assignment.objects.select_related('Ast_Tag_nbr').filter(Ast_Tag_nbr=AstNbr)
            queryObj = queryObj.filter(Q(Ast_Tag_nbr_id__Serial_No__icontains=AstNbr)| Q(Ast_Tag_nbr=AstNbr))
            print(queryObj.query)
            print(queryObj.values())
            for i in queryObj:
               print(i.Ast_Tag_nbr)
        
        if check(Asset_Type):
            if 'findme' in request.POST: 
                queryObj = queryObj.filter(Ast_Tag_nbr_id__Asset_Type__icontains=Asset_Type)
            elif 'AllAssets' in request.POST:
                AllObjects = AllObjects.filter(Asset_Type__icontains=Asset_Type)
        
        if check(project):
           queryObj = queryObj.filter(Ast_Tag_nbr_id__Project_Name__icontains=project)
           #print(queryObj.values_list())

        if check(mincost):
            queryObj = queryObj.filter(Ast_Tag_nbr_id__Item_Cost_USD__gte = mincost)
        if check(maxcost):
            queryObj = queryObj.filter(Ast_Tag_nbr_id__Item_Cost_USD__lt = maxcost)
        if check(fromdate):
            queryObj = queryObj.filter(Ast_Tag_nbr_id__PurchaseDate__gte = fromdate)

        if check(todate):
            queryObj = queryObj.filter(Ast_Tag_nbr_id__PurchaseDate__lt = todate)
        if check(Condition):
            queryObj = queryObj.filter(Ast_Tag_nbr_id__Asset_Condition__icontains = Condition)
        if check(Status):
            queryObj = queryObj.filter(Ast_Tag_nbr_id__Asset_Status__icontains = Status)

        if check(location):
            queryObj = queryObj.filter(Ast_Tag_nbr_id__Location__icontains = location)
            print(queryObj.values_list())
        if check(vendor):
            queryObj = queryObj.filter(Ast_Tag_nbr_id__Vendor__icontains = vendor)
            print(queryObj.values_list())
        
        if check(Available):
            queryObj = queryObj.filter(Ast_Tag_nbr_id__Availability__icontains = Available)
        if 'findme' in request.POST: 
            messages.info(request,f"Your search returned {queryObj.count()} results")
        elif 'AllAssets' in request.POST:
            messages.info(request,f"Your search returned {AllObjects.count()} results")




        if 'excel' in request.POST:
            response=HttpResponse(content_type =  'application/ms-excel')
    
            response['Content-Disposition']='attachment;filename = Assets_Register_Export' + str(datetime.datetime.now())+'.xls'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('AssetsExport')
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns =  [

                    'STATUS',
                    'CO',
                    # 'PSI/W ASSET #',
                    # 'CDFA Number',
                    'AST-TAG-NBR',
                    'ASSET LOCATION', 
                    'ASSET-TYPE',
                    'AST-DESCRIPTION',
                    'Serial_No',             
                    'Model_No',
                    'ACTIVITY',
                    # 'Property Title',
                    'Asset_Condition',
                    'PurchaseDate',
                    'AST-CURRENCY',                
                    'Item_Cost_UGX',
                    'Item_Cost_USD',
                    'Project_Name',
                    
                ]

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            
            font_style = xlwt.XFStyle()

            rows = queryObj.values_list(
                    
                    'Ast_Tag_nbr__Asset_Condition',
                    'Ast_Tag_nbr__Company',
                    # '',
                    # '',
                    'Ast_Tag_nbr',
                    'Ast_Tag_nbr__Location',   
                    'Ast_Tag_nbr__Asset_Type',
                    'Ast_Tag_nbr__Ast_description',
                    'Ast_Tag_nbr__Serial_No',
                    'Ast_Tag_nbr__Model_No',
                    'Ast_Tag_nbr__Project',
                    # '',
                    'Ast_Tag_nbr__Asset_Condition',
                     'Ast_Tag_nbr__PurchaseDate',
                    'Ast_Tag_nbr__Ast_Currency',
                   'Ast_Tag_nbr__Item_Cost_UGX',
                    'Ast_Tag_nbr__Item_Cost_USD',
                    
                    'Ast_Tag_nbr__Project_Name',
                    
                   
                    )
            for row in rows:
                row_num+=1

                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            

            wb.save(response)

            return response
        

   


    paginator = Paginator(queryObj, 15)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    # Need to convert date object in returned values as a serializable value othwerwise get error Json cannot serialize date

    qs_json = json.dumps(list(AssetTb.objects.values()), default=myconverter)
    context = {'queryObj':queryObj, 'myform':myform, 
                'Desktops':Desktops,'Laptops':Laptops,
                "assignedDevices":assignedDevices,
                "ActiveStaff":ActiveStaff,
               'Unusable_Desktops':Unusable_Desktops,
               'Unusable_Laptops':Unusable_Laptops,
               'UserobjFilter':UserobjFilter.count(),'qs_json':qs_json, 'page_obj': page_obj,
               'equipObj':equipObj,
               'equipObj1':equipObj1,
               'equipObj2':equipObj2,
               'TotalAssigned':TotalAssigned,
               'defects':defects,
               'dueForDisposal':dueForDisposal,
               'dueForDisposalCount':dueForDisposal.count(),
               'todays_date':todays_date,
               'performing':performing,
               'myvalues':request.POST,
               'AllObjects':AllObjects,
               'Desktops_Above':Desktops_Above,
               'Laptops_Above':Laptops_Above,
               'Total_Faulty': Total_Faulty,
               'Total_Faulty_Above_Five':Total_Faulty_Above_Five,
               'Total_Faulty_Above_Five_Laptops':Total_Faulty_Above_Five_Laptops,
               'Total_Faulty_Above_Five_Desktops':Total_Faulty_Above_Five_Desktops,
               'Gap':Gap,
               'Assigned':Assigned,
               'Functional':Functional,

               }
    

    return render(request, 'base/reports.html', context)



def allAssetObjects(request):

    # KCCA = ['PSIU-TAB-MANE-01',
    #         'PSIU-TAB-MaNe-03',
    #         'PSIU-TAB-MaNe-06',
    #         'PSIU-TAB-MaNe-07',
    #         'PSIU-TAB-MaNe-02',
    #         'PSIU-TAB-MaNe-08',
    #         'PSIU-TAB-MaNe-09',
    #         'PSIU-TAB-MaNe-11',
    #         'PSIU-TAB-MaNe-12',
    #         ]
    # for asset in KCCA:
    # myasset=AssetTb.objects.filter(Ast_Tag_nbr__iexact="PSIU-LP-WHP-70").update(Location="FINANCIAL ANALYTICS OFFICE")
    # Assignment.objects.filter(Ast_Tag_nbr="PSIU-LP-WHP-70").delete()
    #AssetTb.objects.filter(Ast_Tag_nbr="PSIU-LP-NPI-01").update(Location="NORTH EASTERN REGION OFFICE-JINJA")
    #     myasset.update(Comments="Asset Handed Over to KCCA MaNe Project Details on MaNe File in Finance")
    #     myasset.update(Location="KCCA MANE OFFICE")
    #     myasset.update(Availability="DISPOSED-OF")
    #     myasset.update(Asset_Condition="Good")
      
    # AssetTb.objects.filter(Ast_Tag_nbr='PSIU-LP-WHP-71').update(Availability="FAULTY")
        
    EmployeeObjects = staff.objects.all()
    # Usernames = ['aayebare', 'ymugerwa', 
    #             'amagunda',
    #             'hkaula'
    #             'akalala',
    #             'dakiibua',
    #             'hmulumba',
    #             'jnsajja',
    #             'nokello',
    #             'pedhiruma',
    #             'hgutaka',
    #             'jnaggayi',
    #             'dakiibua',
    #             'dbua',
    #             'dnantongo',
    #             'jomenyuk',
    #             'sononge',
    #             'sarah1',
    #             'one',
    #             'jsmith',
    #             'akalala',
                

    
    
    # ]
#     myDevices=[
#         'UAK 457X',
#         'UAL 444N',
#         'UAS 516 Z',
#         'UAS 517 Z',
#         'UAU742S',
#         'UAU 103T',
#         'UAL 867N',
        
#         # 'PACE-COM-82',
#         # 'PACE-COM-97',
#         # 'PACE-COM-PI-06',
#         # 'PACE-COM-PI-07',
#         # 'PACE-COM-PI-10',
#         # 'PACE-COM-108',
#         # 'PACE-MBR-PTR-03',
#         # 'PACE-PROJ-WHP-04',
# ]

#     for device in myDevices:
#         AssetTb.objects.filter(Ast_Tag_nbr=device).update(Availability="DISPOSED-OF")
    
    # staff.objects.filter(Username__in=Usernames).update(staff_status="False")
    
    # Assignment.objects.filter(Username='jdoe').delete()
    
   # queryObj =  AssetTb.objects.all().order_by('-PurchaseDate', '-Ast_Tag_nbr')
    excludes = ['Lost', 'Missing', 'Disposed-of', 'Disposed-Off',"FAULTY", "DUE FOR DISPOSAL"]
    # excludes = ['Lost', 'Missing', 'Disposed-of', 'Disposed-Off',"FAULTY", "DUE FOR DISPOSAL"]
    queryObj =  AssetTb.objects.all().order_by('Ast_Tag_nbr','Location')\
    .exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes).order_by('Location')
    # queryObj =  AssetTb.objects.filter(Availability__in=excludes).order_by("Availability")
 
    
    # vehicles = AssetTb.objects.filter(Asset_Type__iexact="Vehicle").annotate(myVehicle = )

    # AssetTb.objects.filter(Ast_Tag_nbr='PSIU-LP-WHP-71').update(Location="FINANCIAL ANALYTICS OFFICE")

    myform =  AddAssetForm(request.POST)
  
    
    if request.method == 'POST':
        AstNbr = request.POST.get('search_name')
        Asset_Type = request.POST.get('Asset_Type')
        project = request.POST.get('Project_Name')
        fromdate = request.POST.get('from_date')
        todate = request.POST.get('to_date')
        mincost = request.POST.get('minimum_cost')
        maxcost = request.POST.get('maximum_cost')
        aging = request.POST.get('age')
        Condition = request.POST.get('Asset_Condition')
        Status = request.POST.get('Asset_Status')
        #ProjectName = request.POST.get('Project_Name')
        Available = request.POST.get('Availability')
        location = request.POST.get('Location')
        vendor = request.POST.get('vendor')


        if AstNbr != "" and AstNbr is not None:
            #queryObj = Assignment.objects.select_related('Ast_Tag_nbr').filter(Ast_Tag_nbr=AstNbr)
            queryObj = queryObj.filter(Q(Serial_No__icontains=AstNbr)| Q(Ast_Tag_nbr__icontains=AstNbr)|Q(AstNo__icontains=AstNbr)).exclude(Availability__in=excludes)
            print(queryObj.query)
            print(queryObj.values())
            for i in queryObj:
               print(i.Ast_Tag_nbr)
        
        if check(Asset_Type):
            queryObj = queryObj.filter(Asset_Type__icontains=Asset_Type).exclude(Availability__in=excludes)
            
        
        if check(project):
           queryObj = queryObj.filter(Project_Name__icontains=project).exclude(Availability__in=excludes)
           #print(queryObj.values_list())

        if check(mincost):
            queryObj = queryObj.filter(Item_Cost_USD__gte = mincost).exclude(Availability__in=excludes)
        if check(maxcost):
            queryObj = queryObj.filter(Item_Cost_USD__lt = maxcost).exclude(Availability__in=excludes)
        if check(fromdate):
            queryObj = queryObj.filter(PurchaseDate__gte = fromdate).exclude(Availability__in=excludes)

        if check(todate):
            queryObj = queryObj.filter(PurchaseDate__lt = todate).exclude(Availability__in=excludes)
        if check(Condition):
            queryObj = queryObj.filter(Asset_Condition__icontains = Condition).exclude(Availability__in=excludes)
        if check(Status):
            queryObj = queryObj.filter(Asset_Status__icontains = Status).exclude(Availability__in=excludes)

        if check(location):
            queryObj = queryObj.filter(Location__icontains = location).exclude(Availability__in=excludes)
            print(queryObj.values_list())
        if check(vendor):
            queryObj = queryObj.filter(Vendor__icontains = vendor)
            print(queryObj.values_list())
        
        if check(Available):
            queryObj = queryObj.filter(Availability__icontains = Available)
        
        messages.info(request,f"Your search returned {queryObj.count()} results")
        




        if 'excel' in request.POST:
            response=HttpResponse(content_type =  'application/ms-excel')
    
            response['Content-Disposition']='attachment;filename = Assets_Register_Export' + str(datetime.datetime.now())+'.xls'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('AssetsExport')
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns =  [

                    'STATUS',
                    'CO',
                    # 'PSI/W ASSET #',
                    # 'CDFA Number',
                    'AST-TAG-NBR',
                    'ASSET LOCATION', 
                    'ASSET-TYPE',
                    'AST-DESCRIPTION',
                    'Serial_No',             
                    'Model_No',
                    'ACTIVITY',
                    # 'Property Title',
                    'Asset_Condition',
                    'PurchaseDate',
                    'AST-CURRENCY',                
                    'Item_Cost_UGX',
                    'Item_Cost_USD',
                    'Project_Name',
                    
                ]

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            
            font_style = xlwt.XFStyle()

            rows = queryObj.values_list(
                    
                    'Asset_Condition',
                    'Company',
                    # '',
                    # '',
                    'Ast_Tag_nbr',
                    'Location',   
                    'Asset_Type',
                    'Ast_description',
                    'Serial_No',
                    'Model_No',
                    'Project',
                    # '',
                    'Asset_Condition',
                     'PurchaseDate',
                    'Ast_Currency',
                   'Item_Cost_UGX',
                    'Item_Cost_USD',
                    
                    'Project_Name',
                    
                   
                    )
            for row in rows:
                row_num+=1

                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            

            wb.save(response)

            return response
        

   


    paginator = Paginator(queryObj, 15)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    # Need to convert date object in returned values as a serializable value othwerwise get error Json cannot serialize date

    qs_json = json.dumps(list(AssetTb.objects.values()), default=myconverter)
    context = {'queryObj':queryObj, 'myform':myform, 'qs_json':qs_json, 'page_obj': page_obj,
               
               'myvalues':request.POST,
               

               }
    

    return render(request, 'base/reports_all.html', context)

def csvexport(request):
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment;filename = Assets_Register_Export' + str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow([
            'Asset_Type',
            'Asset_Condition ',
            'Project',
            'Project_Name',
            'Asset_Status',
            'Availability',
            'Location',   
            'Serial_No',
            'Lawson_Asset_No',
            'Ast_description',
            'Item_Cost_UGX',
            'Item_Cost_USD',
            'Model_No',
            'Ast_Tag_nbr',
            'PurchaseDate',
            ])

    assets = AssetTb.objects.all()

    for asset in assets:
        writer.writerow([
            asset.Ast_Tag_nbr,
            asset.Asset_Type,
            asset.Asset_Condition,
            asset.Serial_No,
            asset.Lawson_Asset_No,
            asset.Ast_description,
            asset.Model_No,
            asset.Asset_Status,
            asset.Availability,
            asset.Location,   
            
            asset.Project,
            asset.Project_Name,
            asset.Item_Cost_UGX,
            asset.Item_Cost_USD,
            asset.PurchaseDate,
        ])

    return response


def excelexport(request):
    
    response=HttpResponse(content_type =  'application/ms-excel')
    
    response['Content-Disposition']='attachment;filename = Assets_Register_Export' + str(datetime.datetime.now())+'.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('AssetsExport')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns =  [
            'Ast_Tag_nbr',
            'Asset_Type',
            'Asset_Condition',
            'Serial_No',
            'AstNo',
            'Ast_description',
            'Model_No',
            'Asset_Status',
            'Availability',
            'Location',   
            'Project',
            'Project_Name',
            'Item_Cost_UGX',
            'Item_Cost_USD',
            'PurchaseDate',
        ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()

    rows = AssetTb.objects.filter(Item_Cost_USD__gte = 5000).values_list('Ast_Tag_nbr',
            'Asset_Type',
            'Asset_Condition',
            'Serial_No',
            'AstNo',
            'Ast_description',
            'Model_No',
            'Asset_Status',
            'Availability',
            'Location',   
            'Project',
            'Project_Name',
            'Item_Cost_UGX',
            'Item_Cost_USD',
            'PurchaseDate',)
    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    

    wb.save(response)

    return response

    
def pdfexport(request):
    pass

def Depreciation(request):

        
    return render(request,"base/depreciation.html")

 
 
 
    # if request.method == 'POST':
    #     AstNbr = request.POST.get('search_name')
    #     Asset_Type = request.POST.get('Asset_Type')
    #     project = request.POST.get('Project_Name')
    #     fromdate = request.POST.get('from_date')
    #     todate = request.POST.get('to_date')
    #     mincost = request.POST.get('minimum_cost')
    #     maxcost = request.POST.get('maximum_cost')
    #     aging = request.POST.get('age')
    #     Condition = request.POST.get('Asset_Condition')
    #     Status = request.POST.get('Asset_Status')
    #     #ProjectName = request.POST.get('Project_Name')
    #     Available = request.POST.get('Availability')
    #     location = request.POST.get('Location')


    #     if AstNbr != "" and AstNbr is not None:
    #         queryObj = queryObj.filter(Ast_Tag_nbr__icontains=AstNbr)
        
    #     if check(Asset_Type):
    #         queryObj = queryObj.filter(Asset_Type__icontains=Asset_Type)
        
    #     if check(project):
    #         queryObj = queryObj.filter(Project_Name__icontains=project)   


    #     if check(mincost):
    #         queryObj = queryObj.filter(Item_Cost_USD__gte = mincost) 
    #     if check(maxcost):
    #         queryObj = queryObj.filter(Item_Cost_USD__lt = maxcost)
    #     if check(fromdate):
    #         queryObj = queryObj.filter(PurchaseDate__gte = fromdate)

    #     if check(todate):
    #         queryObj = queryObj.filter(PurchaseDate__lt = todate)
    #     if check(Condition):
    #         queryObj = queryObj.filter(Asset_Condition__icontains = Condition)
    #     if check(Status):
    #         queryObj = queryObj.filter(Asset_Status__icontains = Status)

    #     if check(location):
    #         #queryObj = queryObj.filter(Location__icontains = location)
    #         queryObj = queryObj.filter(Location__icontains = location)
        
    #     if check(Available):
    #         queryObj = queryObj.filter(Availability__icontains = Available)

    #     messages.info(request,f"Your search returned {queryObj.count()} results")


    # queryObj =  AssetTb.objects.filter().order_by('Ast_Tag_nbr','Location')\
    # .exclude(Location__icontains = 'PACE').exclude(Availability__in=excludes)
    # myform =  AddAssetForm(request.POST)

    
    
    # if request.method == 'POST':
    #     AstNbr = request.POST.get('search_name')
    #     Asset_Type = request.POST.get('Asset_Type')
    #     project = request.POST.get('Project_Name')
    #     fromdate = request.POST.get('from_date')
    #     todate = request.POST.get('to_date')
    #     mincost = request.POST.get('minimum_cost')
    #     maxcost = request.POST.get('maximum_cost')
    #     aging = request.POST.get('age')
    #     Condition = request.POST.get('Asset_Condition')
    #     Status = request.POST.get('Asset_Status')
    #     ProjectName = request.POST.get('Project_Name')
    #     Available = request.POST.get('Availability')
    #     location = request.POST.get('Location')


    #     if AstNbr != "" and AstNbr is not None:
    #         queryObj = queryObj.filter(Ast_Tag_nbr__icontains=AstNbr)
        
    #     if check(Asset_Type):
    #         queryObj = queryObj.filter(Asset_Type__icontains=Asset_Type)
        
    #     if check(project):
    #         queryObj = queryObj.filter(Project_Name__icontains=ProjectName)   


    #     if check(mincost):
    #         queryObj = queryObj.filter(Item_Cost_USD__gte = mincost) 
    #     if check(maxcost):
    #         queryObj = queryObj.filter(Item_Cost_USD__lt = maxcost)
    #     if check(fromdate):
    #         queryObj = queryObj.filter(PurchaseDate__gte = fromdate)

    #     if check(todate):
    #         queryObj = queryObj.filter(PurchaseDate__lt = todate)
    #     if check(Condition):
    #         queryObj = queryObj.filter(Asset_Condition__icontains = Condition)
    #     if check(Status):
    #         queryObj = queryObj.filter(Asset_Status__icontains = Status)

    #     if check(location):
    #         #queryObj = queryObj.filter(Location__icontains = location)
    #         queryObj = queryObj.filter(Location__icontains = location)
        
    #     if check(Available):
    #         queryObj = queryObj.filter(Availability__icontains = Available)

    #     messages.info(request,f"Your search returned {queryObj.count()} results")

        
    # filterObj = Assignment.objects.filter(Q(Ast_Tag_nbr__PurchaseDate__gte=year_ago) & Q(Ast_Tag_nbr__PurchaseDate__lte=todays_date),Ast_Tag_nbr__Asset_Type__iexact='Laptop').annotate(Laptops_One_Year=Count('Ast_Tag_nbr__Asset_Type'))
    # for q in filterObj:
    #     data1.append(q.Laptops_One_Year)
    #     labels.append(q.Ast_Tag_nbr.Asset_Type)
    # filterObj = Assignment.objects.filter(Q(Ast_Tag_nbr__PurchaseDate__gte=Three_Years_ago) & Q(Ast_Tag_nbr__PurchaseDate__lte=todays_date),Ast_Tag_nbr__Asset_Type__iexact='Laptop').aggregate(Laptops_Over_Three_Years=Sum('Ast_Tag_nbr__Asset_Type'))
    # for q in filterObj:
    #     data2.append(q.Laptops_Over_Three_Years)
    #     labels.append(q.Ast_Tag_nbr.Asset_Type)

    

    # if 'pdf' in request.POST:
    #     response=HttpResponse(content_type =  'application/pdf')
    
    #     response['Content-Disposition']='inline;attachment;filename = Assets_Register_Export' + str(datetime.datetime.now())+'.pdf'

    #     response['Content-Transfer-Encoding'] = 'binary'

    #     sum = queryObj.aggregate(Sum('Item_Cost_USD'))

    #     html_string = render_to_string('base/pdf_export.html',{'queryObj':queryObj,'total':sum})

    #     html = HTML(string=html_string)


    #     result = html.write_pdf()

    #     with tempfile.NamedTemporaryFile(delete=True) as output:
    #         output.write(result)
    #         output.flush()

    #         output = open(output.name,'rb')

    #         response.write(output.read())
    #     return response


         # for item in performing:
    #     print(item)
    
    # filterObj = AssetTb.objects.filter(Q(PurchaseDate__gte=Five_Years_ago) &
    #  Q(PurchaseDate__lte=todays_date)).filter(Q(Asset_Type__iexact='Laptop')
    #  |Q(Asset_Type__iexact='Desktop')).annotate(Device=(Count('Asset_Type',distinct=True)))
    # # print(filterObj.query)
    # for q in filterObj:
    #     pass

    # for item in UserobjFilter:
    #     print(item)
    # qs2 = AssetTb.objects.annotate(Desktops=Count("Asset_Type"), Laptops=Count(
    #     'Asset_Type'
    # ))
    # print(qs2.Desktops)

    #print(Unusable_Laptops.query)