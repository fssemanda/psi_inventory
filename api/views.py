import logging
from django.shortcuts import render

# Create your views here.

# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializer import *
from home.models import AssetTb, staff
from django.db.models import Q
from assets.views import projectMatch
from django.contrib.auth import login, logout, authenticate


logging.basicConfig(filename="ActivityLog.log",level=logging.DEBUG, format='%(levelname)s:%(lineno)d:%(asctime)s:%(message)s')

@api_view(['GET'])
def apiOverview(request):
    api_urls = {

        'Assets': '/asset-list/',
        'Assets_Search': '/asset-list/<str:str>',
        'Detail View': '/asset-detail/<str:pk>/',
        'Create': '/asset-create/',
        'Update': '/asset-update/<str:pk>',
        'Delete': '/asset-delete/<str:pk>',

        'View Verification list': '/verification/',
        'Item-detail': '/item-detail/<str:pk>/',
        'Create Item': '/item-create/',
        'Update Item': '/item-update/<str:pk>',
        'Delete Item': '/item-delete/<str:pk>',

    }

    return Response(api_urls)


@api_view(['GET'])
def assetList(request):
    Assets = AssetTb.objects.all()
    

    serializer = AssetSerializer(Assets, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def MatchAsset(request):
    Assets = AssetTb.objects.filter(Q(Ast_Tag_nbr__icontains=request.GET.get('term'))
     | Q(AstNo__icontains=request.GET.get('term')) | Q(Serial_No__icontains=request.GET.get('term')))

    serializer = AssetSerializer(Assets, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def assetdetail(request, pk):
    Assets = AssetTb.objects.filter(Q(Ast_Tag_nbr__iexact=pk) | Q(AstNo__iexact=pk)).get()
    
    # Assets = AssetTb.objects.filter(Ast_Tag_nbr__icontains=str)
    serializer = AssetSerializer(Assets, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def apiLogin(request):
    
    uname =  request.data.get('username')
    pwd = request.data.get('password')
    

    print(request.data.get('username'))
    print(request.data.get('password'))
    print(request.POST)

     
    print(f'Posted Username {uname}')
    myusername = str(uname).strip()
    password = str(pwd).strip()
    userobj = User.objects.get(username=myusername)
    #print(userobj.query)
    print(userobj)
    user = authenticate(request,username=myusername, password=password)
    print(user)
    pwdcheck = userobj.check_password(password)
    print(password)
    print(pwdcheck)
    if pwdcheck:

    # Assets = AssetTb.objects.filter(Ast_Tag_nbr__icontains=str)
        serializer = UserSerializer(instance=userobj, data=request.data)
        if serializer.is_valid():
            login(request,user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

@api_view(['POST'])
@csrf_exempt
def createAsset(request):
    # Assets = AssetTb.objects.all()

    serializer = AssetSerializer(data=request.data)

    if serializer.is_valid():
        serializer.validated_data['Project_Name']=projectMatch(serializer.validated_data['Project'])
        AstNo =  serializer.validated_data['AstNo']
        # if AssetTb.objects.filter(AstNo=AstNo).exists():
        #     print("Exists")
        #     return Response({'AstNo Error':'AstNo Already Exists'})
        # else:
        #     serializer.save()
        #     return Response(serializer.data)
        serializer.save()
        return Response(serializer.data)
        
    else:
        return Response(serializer.errors)


@api_view(['PATCH'])
@csrf_exempt
def assetUpdate(request, pk):
    MyAsset = AssetTb.objects.get(Ast_Tag_nbr=pk)

    serializer = AssetSerializer(instance=MyAsset, data=request.data)
    
    if serializer.is_valid():
        serializer.validated_data['Project_Name']=projectMatch(serializer.validated_data['Project'])
        serializer.save()
        print(serializer.data)
        # AstNo =  serializer.validated_data['AstNo']
        # if AssetTb.objects.filter(AstNo=AstNo).exists():
        #     print("Exists")
        #     return Response({'AstNo Error':'AstNo Already Exists'})
        # else:
        #     serializer.save()
        #     return Response(serializer.data)
    else:
        return Response(serializer.errors)
    return Response(serializer.data)



@api_view(['DELETE'])
def assetDelete(request,pk):
    MyAsset = AssetTb.objects.get(Ast_Tag_nbr=pk)
    MyAsset.delete()

    return Response("Item Successfully deleted")


# @api_view(['GET'])
# def verify(request):
#     Assets = Verified.objects.all()

#     serializer = VerifySerializer(Assets, many=True)

#     return Response(serializer.data)

@api_view(['PATCH'])
def verifyAsset(request,pk):

    verifyObj = AssetTb.objects.filter(Q(Ast_Tag_nbr__iexact=pk) | Q(AstNo__iexact=pk)).get()
    serializer = VerifySerializer(instance=verifyObj, data=request.data)

    if serializer.is_valid():
        serializer.validated_data['Asset_Status']="VERIFIED"
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)


# @api_view(['POST'])
# @csrf_exempt
# def vAdd(request):

#     serializer = VerifySerializer(data=request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)


# @api_view(['GET'])
# def detail(request, pk):
#     Assets = Verified.objects.get(id=pk)

#     serializer = VerifySerializer(Assets, many=False)

#     return Response(serializer.data)


# @api_view(['POST'])
# def create(request):
#     # Assets = AssetTb.objects.all()

#     serializer = VerifySerializer(data=request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)


# @api_view(['PUT'])
# @csrf_exempt
# def update(request, pk):
#     MyAsset = Verified.objects.get(id=pk)

#     serializer = VerifySerializer(instance=MyAsset, data=request.data)

#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)


# @api_view(['DELETE'])
# def delete(request,pk):

#     MyAsset = Verified.objects.get(id=pk)
#     MyAsset.delete()

#     return Response("Item Successfully deleted")

@api_view(['GET'])
def UsersListing(request):
    Users = staff.objects.all()

    serializer = UserSerializer(Users, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def UsersQuery(request):
    Users = staff.objects.filter(Q(Username__icontains=request.GET.get('term'))
     | Q(Firstname__icontains=request.GET.get('term')) | Q(Lastname__icontains=request.GET.get('term')))

    serializer = UserSerializer(Users, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def assign(request):
    serializer = AssignmentSerializer(data=request.data)

    if serializer.is_valid():
        
        serializer.save()
        
        try:
            Device = serializer.validated_data['Ast_Tag_nbr']
            AssetTb.objects.filter(Ast_Tag_nbr=Device).update(Availability="ASSIGNED")
        except Exception as e:
            print(e)
            return Response(f'{serializer.data} There was an error changing Asset status: {e}')

        return Response(serializer.data)
    else:
        return Response(serializer.errors)
