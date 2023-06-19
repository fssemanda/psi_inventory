from django.shortcuts import render

# Create your views here.

import qrcode


from home.models import  staff, AssetTb,QRCodeClass
from home.logindecorators import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *


def QrGen(request):

    AssetNo = AssetTb.objects.all()

    MyQRform = QRform(request.POST)



    for Asset in AssetNo:
        print(Asset.Ast_Tag_nbr)


    context={'MyQRform': MyQRform}

    return render(request, 'base/generateqr.html' ,context)


def QrBulk(request):

    AssetNo = AssetTb.objects.all()

    for Asset in AssetNo:
        
        AssetQR = qrcode.make(Asset.AstNo)
        AssetQR.save(f'static/img/QRcodes/{Asset.AstNo}.png')
        print(AssetQR)

    context = {}

    return render(request, 'base/bulk.html', context)
