from queue import Empty
from django.shortcuts import render,redirect
from assets.forms import FileUploadForm
from home.logindecorators import allowed_users
from home.models import CsvUpload, AssetTb,User,Assignment, staff,Disposal
import csv
import logging
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Finance', 'IT'])
def UserUpload(request):

    # Assetsobj = AssetTb.objects.filter(Project="4562PM")
    # for asset in Assetsobj:
    #     assetobj = AssetTb.objects.get(Ast_Tag_nbr=asset.Ast_Tag_nbr)
    #     assetobj.Project_Name = "BERGSTROM FOUNDATION"
    #     assetobj.save()

    if request.method == 'POST':
        if 'Confirm' in request.POST:
            form = FileUploadForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                obj = CsvUpload.objects.get(Parsed=False)
                with open(obj.file_name.path, 'r') as f:
                    reader = csv.reader(f)
                    try:
                        next(reader)
                        for row in reader:
                            
                            if User.objects.filter(username=row[2]).exists():
                                print("User Exists")
                                continue
                            else:
                                try:
                                    print('Trying to create user')
                                    myuser=User.objects.create(
                                    first_name=row[0],
                                    last_name=row[1],
                                    username=row[2],
                                    email=row[9],
                                    password="Uganda@123",

                                    )
                                    myuser.set_password("Uganda@123")
                                    myuser.save()
                                except:
                                    ValueError("Error Occured")
                                    obj.Parsed = True

                            # print(row[4])
                            # print(type(row[4]))

                            # print(type(value))
                        obj.Parsed = True
                        obj.save()
                    except Exception as e:
                        "Failed first Test"
                        obj.Parsed = True
                        obj.save()
                        return e
        else:
            form = FileUploadForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                obj = CsvUpload.objects.get(Parsed=False)
                with open(obj.file_name.path, 'r') as f:
                    reader = csv.reader(f)
                    
                    logging.info("Reading File") 
                    

                    for row in reader:
                        logging.debug(f"Reading File")
                        FMV = row[2]
                        FMV = FMV.replace(",", "")
                        FMV = float(FMV)

                        DI= row[3]
                        DI = DI.replace(",", "")
                        DI = float(DI)


                        # The date split it via / then tuple unpack it and compose a new string i required structure.

                        DateFormat = row[1]
    
                        DateFormat1 = DateFormat.split('/')
                        print(DateFormat1)
                        NewDate = "-".join([DateFormat1[2], DateFormat1[0],
                                            DateFormat1[1]])

                        print(NewDate)  
                        try:
                            if Disposal.objects.filter(Ast_Tag_nbr=row[0]).exists():
                                obj.Parsed = True
                                obj.save()
                                Ast_Tag_number = Disposal.objects.get(Ast_Tag_nbr=row[0])
                                messages.warning(request, f"This Asset {Ast_Tag_number.Ast_Tag_nbr} has already been Auctioned/Disposed-Of")
                                # return redirect('auction')
                            else:    
                                Disposal.objects.create(
                                Ast_Tag_nbr = AssetTb.objects.get(Ast_Tag_nbr=row[0]),
                                disposalDate = NewDate,
                                disposalIncome =DI,
                                fairMarketValue = FMV,
                                disposalProcedure = "Auctioned",
                                disposalExplanation = row[6],
                                CR_Approval = "Approved"
                                )
                                obj.Parsed = True
                                obj.save()
                        except ValueError as e:
                            logging.debug('Asset not added')
                            obj.Parsed = True
                            obj.save()
                            print(row[0])
                            print(row[1])
                            print(row[2])
                            print(row[3])
                            print(row[4])
                            print(row[5])
                            

                            
                    obj.Parsed = True
                    obj.save()

    else:
        form = FileUploadForm()

    context = {'form': form}

    return render(request, 'base/usersbulkupload.html', context)


def AssetAssignment(request):



        if request.method == 'POST':
            form = FileUploadForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                obj = CsvUpload.objects.get(Parsed=False)
                with open(obj.file_name.path, 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        Staffinstance = staff.objects.get(Username=row[0])
                        Asset_Instance = AssetTb.objects.get(Ast_Tag_nbr=row[1])
                        print(Asset_Instance)
                        print(Staffinstance)

                                        # print(Asset_Instance)

                        if Assignment.objects.all().filter(Ast_Tag_nbr=row[1]).exists():
                            
                            print("Assignment Exists")

                        else:
                            print("saving object")
                            Assignment.objects.create(
                                    Username = Staffinstance,
                                    Ast_Tag_nbr=Asset_Instance,
                                
                                )

                        
                    obj.Parsed = True
                    obj.save()
        else:
            form = FileUploadForm()
        
        

        context = {'form': form}

        return render(request, 'base/bulkassignment.html', context)
    
    