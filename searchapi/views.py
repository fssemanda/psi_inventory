from django.shortcuts import render

# Create your views here.
import json

from home.models import AssetTb, Assignment
from django.http import JsonResponse
import datetime
from django.db.models import Q, Count, Avg, F,Sum,Min, Max

def search_assets(request):

    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

#        Asset_Search = AssetTb.objects.filter(Ast_Tag_nbr_starts_with=search_str, Ast_description=)

        Asset_Search  = AssetTb.objects.filter(Ast_Tag_nbr__icontains = search_str)
    
        data = Asset_Search.values()

    return JsonResponse(list(data), safe = False)


# Asset_Search  = AssetTb.objects.filter(Asset_Type__istartswith = search_str) | AssetTb.objects.filter(
#             PurchaseDate__istartswith = search_str) | AssetTb.objects.filter(
#             Availability__icontains = search_str) | AssetTb.objects.filter(Model_No__istartswith = search_str) | AssetTb.objects.filter(
#             Ast_Tag_nbr__icontains = search_str) | AssetTb.objects.filter(Project_Name__istartswith = search_str) | AssetTb.objects.filter(Ast_description__istartswith = search_str)





def graphing(request):
    AssetObj = AssetTb.objects.all()
    todays_date = datetime.date.today()
    for item in AssetObj:
       days_diff = (todays_date-item.PurchaseDate)
       #print(days_diff)

    year_ago = todays_date-datetime.timedelta(days=30*72)

    filterObj = AssetObj.filter(PurchaseDate__gte = year_ago, PurchaseDate__lte = todays_date)

    print(filterObj.count())

    #for item in filterObj:
        #print(item.Ast_Tag_nbr ,item.PurchaseDate)

    #Helper function to pick Device types

    def get_asset_type_count(assetType):
        mycount = 0
        objectcount = filterObj.filter(Asset_Type = assetType)
        for item in objectcount:
            mycount += 1
        return mycount

    def get_Asset_Type(asset):
        return asset.Asset_Type
    finalrep = {}

    assetTypeList = list(set(map(get_Asset_Type, filterObj)))

    for asset in filterObj:
        for assetType in assetTypeList:
            finalrep[assetType] = get_asset_type_count(assetType)

    return JsonResponse({'Asset_type_Data': finalrep}, safe=False)


def graphview(request):

    context={}
    return render (request, 'base/Analytics.html',context)

def agingGraph(request):

    qs2= AssetTb.objects.all()
    # qs2= AssetTb.objects.filter(Asset_Type='Desktop').update(Asset_Type='DESKTOP')
    data2 = []
    data1 = []
    data3 =[]
    labels = []
    todays_date = datetime.date.today()
    year_ago = todays_date - datetime.timedelta(days=365)
    Three_Years_ago = todays_date - datetime.timedelta(days=365 * 3)
    Five_Years_ago = todays_date - datetime.timedelta(days=365 * 5)

    # filterObj = qs2.filter(Q(PurchaseDate__gte=year_ago) & Q(PurchaseDate__lte=todays_date),Asset_Type__iexact='Laptop').annotate(Laptops_One_Year=Count('Asset_Type'))
    # for item in filterObj:
    #     data1.append(item.Laptops_One_Year)
    # filterObj = Assignment.objects.filter(Q(Ast_Tag_nbr__PurchaseDate__gte=Five_Years_ago) &
    #  Q(Ast_Tag_nbr__PurchaseDate__lte=todays_date)).filter(Q(Ast_Tag_nbr__Asset_Type__iexact='Laptop')
    #  |Q(Ast_Tag_nbr__Asset_Type__iexact='Desktop')).annotate(Device=Count('Ast_Tag_nbr__Model_No',distinct=True))
     
    # for q in filterObj:
    #     data1.append(q.Device)
    #     labels.append(q.Ast_Tag_nbr.Model_No)
    # filterObj = AssetTb.objects.filter(Q(PurchaseDate__gte=Five_Years_ago) &
    #  Q(PurchaseDate__lte=todays_date)).filter(Q(Asset_Type__iexact='Laptop')
    #  |Q(Asset_Type__iexact='Desktop')).annotate(Device=(Count('Model_No',distinct=True)))
    # print(filterObj.query)
    # for q in filterObj:
    #     data1.append(q.Device)
    #     labels.append(q.Ast_Currency)
    # filterObj = Assignment.objects.filter(Q(Ast_Tag_nbr__PurchaseDate__gte=Three_Years_ago) & Q(Ast_Tag_nbr__PurchaseDate__lte=todays_date),Ast_Tag_nbr__Asset_Type__iexact='Laptop').aggregate(Laptops_Over_Three_Years=Sum('Ast_Tag_nbr__Asset_Type'))
    # for q in filterObj:
    #     data2.append(q.Laptops_Over_Three_Years)
    #     labels.append(q.Ast_Tag_nbr.Asset_Type)

    filterObj=AssetTb.objects.filter(Q(Asset_Type__iexact="Desktop")
    & Q(PurchaseDate__lte=Five_Years_ago)).annotate(
         Models=Sum('Item_Cost_USD', distinct=True), DeviceTypes=Count('Model_No', distinct=True))


    # filterObj = qs2.filter(Q(PurchaseDate__gte=Three_Years_ago) & Q(PurchaseDate__lte=todays_date),Asset_Type__iexact='Laptop').aggregate(Laptops_Over_Three_Years=Count('Asset_Type'))
    # data2.append(filterObj.Laptops_Over_Three_Years)
    # filterObj = qs2.filter(Q(PurchaseDate__gte=Five_Years_ago) & Q(PurchaseDate__lte=todays_date),Asset_Type__iexact='Laptop').aggregate(Laptops_Over_Five_Years=Count('Asset_Type'))
    # data3.append(filterObj.Laptops_Over_Five_Years)

    # filterObj = qs2.filter(Q(PurchaseDate__gte=Three_Years_ago) & Q(PurchaseDate__lte=todays_date),Asset_Type__iexact='Desktop').aggregate(One_Year=Count('Asset_Type'))
    # filterObj = qs2.filter(Q(PurchaseDate__gte=Three_Years_ago) & Q(PurchaseDate__lte=todays_date),Asset_Type__iexact='Desktop').aggregate(One_Year=Count('Asset_Type'))
    # filterObj = qs2.filter(Q(PurchaseDate__gte=Three_Years_ago) & Q(PurchaseDate__lte=todays_date),Asset_Type__iexact='Desktop').aggregate(One_Year=Count('Asset_Type'))
    # filterObj = qs2.filter(Q(PurchaseDate__gte=Three_Years_ago) & Q(PurchaseDate__lte=todays_date),Asset_Type__iexact='Laptop').aggregate(One_Year=Count('Asset_Type'))
    # filterObj = qs2.filter(Q(PurchaseDate__gte=Three_Years_ago) & Q(PurchaseDate__lte=todays_date),Asset_Type__iexact='Laptop').aggregate(One_Year=Count('Asset_Type'))
    # filterObj = qs2.filter(Q(PurchaseDate__gte=Three_Years_ago) & Q(PurchaseDate__lte=todays_date),Asset_Type__iexact='Laptop').aggregate(One_Year=Count('Asset_Type'))
    # for q in filterObj:
    #     print(f"{q}:{q.One_Year}")
    # print(filterObj.keys())
    # for item in filterObj:
    #     print(item)

    finalrep={}
    for q in filterObj:
       queryset = AssetTb.objects.get(Ast_Tag_nbr=q.Ast_Tag_nbr)

        # for item in filterObj:
        #     days_diff = (todays_date - item.PurchaseDate)
        #     days_diff = days_diff.days/365
        #     if days_diff < 3 and days_diff > 0:
        #         finalrep[item.Asset_Type]=days_diff
        #     # elif days_diff > 3 and days_diff < 5:
        #     #     data2.append(item)

        # data2.append(q.Desktops)
       data1.append(q.Models)
       labels.append(q.Asset_Type)
    #    labels.append(queryset.Asset_Type)
    myDict = { 'labels':labels,'data1': data1}

    return JsonResponse(myDict, safe=False)


def Dep(request):
    '''Get All Asset Objects
    
    '''
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
    
    Dimes = AssetObj.all().aggregate(Dime=Sum('Item_Cost_USD'))
    print(Dimes)
    Money=Dimes.values
    print(Money)
    for value in Dimes:
        print(f'The Key is {value}')
    # print(Date.values)
    items = AssetTb.objects.filter(PurchaseDate__lte= "2006-09-24")
    # print(items)
    # print(items.count())
    
    # for item in Date:
    #     print(item.MinimumDate)
    ItemsList = []
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
      
        
        
        for k in range (0, Life):
            Dep = ((BookValue-Salvage)*k)/Life 
            Actual_Dep_Per_year = ((BookValue-Salvage)* (Life-k))/Life
            
            
            if Life-k == 1:
                Total_Depreciation +=  Actual_Dep_Per_year
                # ItemsList.append({
                # f'{asset}':[Dep,Actual_Dep_Per_year]
            # })
            
            # print (f'{asset}------{k}---------{Dep:,.2f}--------{Actual_Dep_Per_year:,.2f}')
    print(Total_Depreciation)
    ItemsList.append(
        {
            'Total_Depreciation':Total_Depreciation,
            'Dimes':20000
        })
    myDict = {'Book_Value':list(Dimes.values()),'Current Asset Salvage Value':Total_Depreciation,}
    # myDict = {'Current Asset Salvage Value':f'{Total_Depreciation:,.2f}','Book_Value':list(Dimes.values())}
    
            
    return JsonResponse({"myDict":myDict},safe=False)
            
    # return HttpResponse(f'{asset} {k}---------{Dep}--------{Actual_Dep_Per_year}') 
    # return HttpResponse(f'{Total_Depreciation:,.2f}') 