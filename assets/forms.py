
from django.forms import ModelForm, fields, widgets
from home.models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User



AssetType = [
    ("VEHICLE", "VEHICLE"), ("DESKTOP", "DESKTOP"),("AIR CONDITIONER", "AIR CONDITIONER"),
    ("LAPTOP", "LAPTOP"), ("MEDICAL EQUIPMENT", "MEDICAL EQUIPMENT"),
    ("TABLET", "TABLET"), ("PHONE", "PHONE"),
    ("COMPUTER ACCESSORY", "COMPUTER ACCESSORY"), ("NETWORKING EQUIPMENT", "NETWORKING EQUIPMENT"),
    ("PROJECTOR", "PROJECTOR"), ("PRINTER", "PRINTER"),
    ("PHOTOCOPIER", "PHOTOCOPIER"), ("MULTI FUNCTIONAL PRINTER", "MULTI FUNCTIONAL PRINTER"),
    ("TABLE", "TABLE"), ("CHAIR", "CHAIR"),
    ("OFFICE ACCESSORY", "OFFICE ACCESSORY"), ("FAN", "FAN"),
    ("INVERTER", "INVERTER"), ("SERVER", "SERVER"), ("FIREWALL", "FIREWALL"),
    ("SAFE", "SAFE"), ("SHREDDER", "SHREDDER"), ("SWITCH", "SWITCH"),
    ('BOOKSHELF','BOOKSHELF'),
    ("MICROWAVE", "MICROWAVE"), ("REFRIGERATOR", "REFRIGERATOR"), ("NETWORK STORAGE EQUIPMENT", "NETWORK STORAGE "
    "EQUIPMENT"),
    ("FILING CABINET", "FILING CABINET"), ("TRASHING MACHINE", "TRASHING MACHINE"), ("DRAWERS", "DRAWERS"),
    ("FIRE EXTINGUISHER", "FIRE EXTINGUISHER"), ("SHELF", "SHELF"),
    ("SOFA CHAIRS", "SOFA CHAIRS"), ("HIGH BACK ROTATING CHAIR", "HIGH BACK ROTATING CHAIR"),
    ("LOW BACK ROTATING CHAIR", "LOW BACK ROTATING CHAIR"),
    ("TELEVISION", "TELEVISION"), ("WATER DISPENSER", "WATER DISPENSER"), ("TENT", "TENT"),
    ("NOT APPLICABLE", "NOT APPLICABLE"),
("SERVER RACK","SERVER RACK")
]

Activities = [
    ("456531", "456531"),
    ("456951", "456951"),
    ("4593NPIPSIUG", "4593NPIPSIUG"),
    ("4666UG", "4666UG"),
    ("4726", "4726"),
    ("4625", "4625"),
    ("4447UG", "4447UG"),
    ("4588CVDUG", "4588CVDUG"),
    ("4677UGANDA", "4677UGANDA"),
    ("P51PPI", "P51PPI"),
    ("6002", "6002"),
    ("3901", "3901"),
    ("640051", "640051"),
    ("4499", "4499"),
    ("4562PERM", "4562PERM"),
    ("4482UG", "4482UG"),
    ("351CCP1", "351CCP1"),
    ("351ICA", "351ICA"),
    ("51CCP1", "51CCP1"),
    ("4115WSHTUNZA", "4115WSHTUNZA"),
    ("85026", "85026"),
    ("85032", "85032"),
    ("051E06", "051E06"),
    ("4562SA", "4562SA"),
    ("4562PM", "4562PM"),
    ("4520", "4520"),
    ("4336P4HVOP", "4336P4HVOP"),
    ("4519", "4519"),
    ("4548", "4548"),
    ("4385Y3", "4385Y3"),
    ("051E03", "051E03"),
    ("4560UG", "4560UG"),
    ("4605", "4605"),
    ("351E03", "351E03"),
    ("351CCP2", "351CCP2"),
    ("4565351", "4565351"),
    ("4628UG", "4628UG"),
    ("4621UG", "4621UG"),
    ("3929BNS", "3929BNS"),
    ("456951", "456951"),
    ("3646Y", "3646Y"),
    ("610051", "610051"),
    ("630051", "630051"),
    ("3526", "3526"),
    ("P3111", "P3111"),
    ("P2490", "P2490"),
    ("3706SUB", "3706SUB"),
    ("4254", "4254"), 
    ("683351", "683351"),
    ("4593NPIPS", "4593NPIPS"),
   ("4593FPPSIUGA", "4593FPPSIUGA"),
   

]

Activity_Names=[

    ('WHP','WHP'),
    ('MERCK','MERCK'),
    ('MUM','MUM'),
    ('PFIZER','PFIZER'),
    ('PROGRAM INCOME','PROGRAM INCOME'),
    ('MANE','MANE'),
    ('CMS PROJECT','CMS PROJECT'),
    ('TUNZA','TUNZA'),
    ('COMMERCIAL MARKETS','COMMERCIAL MARKETS'),
    ('CM4FP','CM4FP'),
    ('BERGSTROM FOUNDATION','BERGSTROM FOUNDATION'),
    ('DISC','DISC'),
    ('COMMON COST','COMMON COST'),
    ('HIVST','HIVST'),
    ('CDC','CDC'),
    ('CSF','CSF'),
    ('WIN','WIN'),
    ('NPI','NPI'),
    ('HIVST','HIVST'),
    ('SELFCARE TBG','SELFCARE TBG'),
    ('COVID-19','COVID-19'),
    ('CITY TO CITY','CITY TO CITY'),
    ('DKT','DKT'),
    ('LEAP PROJECT','LEAP PROJECT'),
     ('REMOTE STEWARDSHIP','REMOTE STEWARDSHIP'),


]

conditions = [
    ("New", "New"),
    ("Good", "Good"),
    ("Fair", "Fair"),
    ("Bad", "Bad"),
    ("Obsolete", "Obsolete"),
    ("Faulty", "Faulty"),


]

statuses = [
    ("VERIFIED", "VERIFIED"),
    ("UNVERIFIED", "UNVERIFIED"),
    ("AUCTIONED","AUCTIONED"),
]

AvailStatus = [
    ("AVAILABLE", "AVAILABLE"),
    ("ASSIGNED", "ASSIGNED"),
    ("TO BE ASSIGNED", "TO BE ASSIGNED"),
    ("UNAVAILABLE FOR ASSIGNMENT", "UNAVAILABLE FOR ASSIGNMENT"),
    ("MISSING", "MISSING"),
    ("LOST", "LOST"),
    ("FAULTY", "FAULTY"),
    ("DUE FOR DISPOSAL", "DUE FOR DISPOSAL"),
    ("DISPOSED-OF", "DISPOSED-OF"),
    ("WRITTEN OFF", "WRITTEN OFF"),
    ("FOR INSURANCE REPLACEMENT", "FOR INSURANCE REPLACEMENT"),
    ("NOT APPLICABLE ON THIS DEVICE", "NOT APPLICABLE ON THIS DEVICE"),

]

Locations = [
("HEAD OFFICE", "HEAD OFFICE"),
("CENTRAL REGION OFFICE", "CENTRAL REGION OFFICE"),
("NORTH EASTERN REGION OFFICE", "NORTH EASTERN REGION OFFICE"), ("JINJA", "JINJA"),
("SERVER ROOM", "SERVER ROOM"), ("FINANCIAL ACCOUNTS", "FINANCIAL ACCOUNTS"), ("CR'S OFFICE", "CR'S OFFICE"),
("HR OFFICE", "HR OFFICE"),
("SIL OFFICE", "SIL OFFICE"),
("SUPPLY CHAIN OFFICE", "SUPPLY CHAIN OFFICE"),
("IT OFFICE", "IT OFFICE"), ("PROGRAMS OFFICE", "PROGRAMS OFFICE"),
("SMD OFFICE", "SMD OFFICE"),
('HQ-COMMON AREA','HQ-COMMON AREA'), 
('RECEPTION-HEAD OFFICE' ,'RECEPTION-HEAD OFFICE' ),
('CAFETERIA', 'CAFETERIA'),
('EASTERN REGION OFFICE','EASTERN REGION OFFICE'),
('NORTHERN REGION OFFICE','NORTHERN REGION OFFICE'),
('NORTH EASTERN REGION OFFICE-JINJA', 'NORTH EASTERN REGION OFFICE-JINJA'),
('NORTH EASTERN REGION OFFICE-MBALE','NORTH EASTERN REGION OFFICE-MBALE'),
('BOARDROOM','BOARDROOM'),
('FINANCIAL ANALYTICS OFFICE','FINANCIAL ANALYTICS OFFICE'),
('DIRECTOR ADMIN AND FINANCE','DIRECTOR ADMIN AND FINANCE'),
('DIRECTOR PROGRAMS', 'DIRECTOR PROGRAMS'),
('KCCA MANE OFFICE','KCCA MANE OFFICE'),
('DEPUTY COUNTRY REPS OFFICE','DEPUTY COUNTRY REPS OFFICE'),
('DISC','DISC'),
('PACE-HEAD OFFICE','PACE-HEAD-OFFICE'),
('PACE-LIRA','PACE-LIRA'),
('DIRECTOR WHP','DIRECTOR WHP'),



]
procedures = [
    ("Donated", "Donated"),("Sold","Sold"),
    ("Auctioned", "Auctioned"),("Written-Off","Written-off"),
]
options = [
    ("Pending","Pending"),
    ("Approved","Approved"),
    ("Rejected","Rejected")
           ]
modes=[
    ('Cash','Cash'),
    ('Salary Deduction','Salary Deduction'),
    ('Donated','Donation'),
]
Auction_stat =[
    ('',''),
    ('',''),
    ('',''),
]
currencies = [
    ('USD','USD'),
    ('UGX','UGX'),
]
Responses = [("Pending", "Pending"),
                 ("Approved", "Approved"),
                 ("Rejected", "Rejected"),
                 ("User Accepted", "User Accepted"),
                 ("Returned", "Returned"),
                 ]
ApprovalResponses = [
                 ("Approved", "Approved"),
                 ("Rejected", "Rejected"),
                 ]

class AssetRQForm(forms.ModelForm):
    class Meta:
        model = AssetRequests
        fields = ['Device_Type','Reason', 'Assigned_Device', ]
        widgets = {
             'Device_Type':forms.Select(attrs={'class':'form-control col-sm-6 col col-md-6', 'id':'deviceType'}),
             'Assigned_Device':forms.TextInput(attrs={'class':'form-control col-sm-6 col col-md-6', 'id':'Ast_tag_nbr_id' ,'name':'Ast_Tag_nbr'}),
             'Reason':forms.Textarea(attrs={'class':'form-control col-sm-6 col col-md-6', 'id':'reason'}),

        }


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']

class FileUploadForm(ModelForm):

    class Meta:
        model = CsvUpload
        fields = ['file_name']

class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields ='__all__'

# class AssetRQForm(forms.Form):
#     class Meta:
#         model = AssetRequests
#         fields = ['Device_Type']

class AddAssetForm(ModelForm):
    
    class Meta:
        model = AssetTb
        fields = '__all__'
        #exclude = ['Project_Name',]
        widgets =  {
            'Asset_Type':forms.Select(attrs={'class':'form-control col col-sm-6 col col-md-6', 'id':'assetType', 'readonly':'readonly'}, choices=AssetType),
            'AstNo':forms.TextInput(attrs={'class':'form-control col col-sm-6 col col-md-6', 'id':'astno'}),
            'Asset_Condition ':forms.Select(attrs={'class':'form-control col-sm-6 col col-md-6'}, choices=conditions),
            'Project':forms.Select(attrs={'class':'form-control col-sm-6 col col-md-6'}, choices=Activities),
            'Project_Name':forms.Select(attrs={'class':'form-control'}, choices=Activity_Names),
            'Asset_Status':forms.Select(attrs={'class':'form-control col-sm-6 col col-md-6'}, choices=statuses),
            'Availability':forms.Select(attrs={'class':'form-control col-sm-6 col col-md-6'}, choices=AvailStatus),
            'Location':forms.Select(attrs={'class':'form-control col-sm-6 col col-md-6'}, choices=Locations),   
            'Serial_No': forms.TextInput(attrs={'class':'form-control col-sm-6 col col-md-6','id':'serial_id'}),
            'AstNo': forms.TextInput(attrs={'class':'form-control col-sm-6 col col-md-6','id':'ast_no_id'}),
            'Ast_description': forms.TextInput(attrs={'class':'form-control col-sm-6 col col-md-6','id':'description_id'}),
            'Item_Cost_UGX': forms.NumberInput (attrs={'class':'form-control col-sm-6 col col-md-6','id':'ugx_id'}),
            'Item_Cost_USD': forms.NumberInput(attrs={'class':'form-control col-sm-6 col col-md-6','id':'usd_id'}),
            'Model_No': forms.TextInput(attrs={'class':'form-control col-sm-6 col col-md-6','id':'model_id'}),
            'Ast_Tag_nbr': forms.TextInput(attrs={'class':'form-control col-sm-6 col col-md-6','id':'ast_tag_id'}),
            'Vendor': forms.TextInput(attrs={'class':'form-control col-sm-6 col col-md-6','id':'vendor_id'}),
            'PurchaseDate': forms.DateInput(attrs={'class':'form-control col-sm-6 col col-md-6', 'type':'date'}),
            'Comments': forms.TextInput(attrs={'class':'form-control col-sm-6 col col-md-6','id':'ReqComments_id'}),

            
            }

class SupervisorApprovalForm(ModelForm):

    class Meta:
        model = AssetRequests
        fields = ['id', 'Username','SupervisorApproval', 'SupervisorApprovalComments',]

class AccountantApprovalform(forms.ModelForm):

    class Meta:
        model = AssetRequests
        fields = ['id', 'AssetManagerApproval', 'AssetMangerApprovalComments',]


class ChangeLogForm(forms.ModelForm):

    class Meta: 
        model = ChangeLog
        fields = '__all__'
        widgets =  {
            'AssetType':forms.Select(attrs={'class':'form-control col col-sm-6 col-md-6 ', 'id':'assetType','readonly':'readonly'}, choices=AssetType),
            'AssetCondition ':forms.Select(attrs={'class':'form-control ','readonly':'readonly'}, choices=conditions),
            'Project':forms.Select(attrs={'class':'form-control ','readonly':'readonly'}, choices=Activities),
            'ProjectName':forms.Select(attrs={'class':'form-control','readonly':'readonly'}, choices=Activity_Names),
            'AssetStatus':forms.Select(attrs={'class':'form-control ','readonly':'readonly'}, choices=statuses),
            'Availability':forms.Select(attrs={'class':'form-control ','readonly':'readonly'}, choices=AvailStatus),
            'Location':forms.Select(attrs={'class':'form-control col col-sm-6 col-md-6 ','readonly':'readonly'}, choices=Locations),   
            'FAMApproval':forms.Select(attrs={'class':'form-control '}, choices=ApprovalResponses),   
            'SerialNo': forms.TextInput(attrs={'class':'form-control ','id':'serial_id','readonly':'readonly'}),
            'AstNo': forms.TextInput(attrs={'class':'form-control ','id':'ast_no_id','readonly':'readonly'}),
            'AstDescription': forms.TextInput(attrs={'class':'form-control ','id':'description_id','readonly':'readonly'}),
            'FAMApprovalComments': forms.Textarea(attrs={'class':'form-control ','id':'FAMComments_id'}),
            'RequesterComments': forms.Textarea(attrs={'class':'form-control ','id':'ReqComments_id','readonly':'readonly','readonly':'readonly'}),
            'ItemCostUGX': forms.NumberInput (attrs={'class':'form-control ','id':'ugx_id','readonly':'readonly'}),
            'ItemCostUSD': forms.NumberInput(attrs={'class':'form-control ','id':'usd_id','readonly':'readonly'}),
            'ModelNo': forms.TextInput(attrs={'class':'form-control ','id':'model_id','readonly':'readonly'}),
            'AstTagnbr': forms.TextInput(attrs={'class':'form-control ','id':'ast_tag_id','readonly':'readonly'}),
            'Vendor': forms.TextInput(attrs={'class':'form-control ','id':'vendor_id','readonly':'readonly'}),
            'Requester': forms.TextInput(attrs={'class':'form-control d-none','id':'Requester_id','readonly':'readonly'}),
            'PurchaseDate': forms.DateInput(attrs={'class':'form-control ', 'type':'date','readonly':'readonly'}),
            
            'logDate': forms.DateInput(attrs={'class':'form-control ', 'type':'date','readonly':'readonly'}),

            
        }

class Assetwithdrawform(forms.ModelForm):

    class Meta:
        model = DeleteAssignment
        fields = '__all__'

        widgets =  {
                
                    'AssignmentID': forms.TextInput(attrs={'class':'form-control ','id':'Deletion_id','readonly':'readonly','value':'{AssignmentObj.id}'}),
                    'Response': forms.Select(attrs={'class':'form-control ', 'id':'Response'}, choices=options),
                    'Comments': forms.Textarea(attrs={'class':'form-control ','id':'Comments_id','rows':'4'}),
        }

class disposalCommentsForm(forms.ModelForm):

    class Meta:
        model = Disposal
        fields = '__all__'

        widgets = {
                    'Ast_Tag_nbr': forms.TextInput(attrs={'class':'form-control col-sm-6 col col-md-6','readonly':'readonly'}),
                    'comments':forms.Textarea(attrs={'class':'form-control'}),
                    #'attachment': forms.FileField(),
                    'disposalExplanation': forms.Textarea(attrs={'class':'form-control'}),
                    'fairMarketValue': forms.NumberInput(attrs={'class':'form-control'}),
                    'disposalDate' : forms.DateInput(attrs={'class':'form-control col-sm-6 col col-md-6', 'type':'date'}),
                    'disposalIncome' : forms.NumberInput(attrs={'class':'form-control'}),
                    'disposalProcedure' : forms.Select(attrs={'class':'form-control '}, choices=procedures),
                    'CR_Approval' : forms.Select(attrs={'class':'form-control '}, choices= options ),
                    'Paymentmode' : forms.Select(attrs={'class':'form-control '}, choices=modes),
                    #'CheckedOut' : forms.BooleanField(),
                    'Buyer' : forms.TextInput(attrs={'class':'form-control'}), 

        }
class auctionForm(forms.ModelForm):

    class Meta:
        model = Disposal
        fields = '__all__'

        widgets = {
                    'Ast_Tag_nbr': forms.TextInput(attrs={'class':'form-control col-sm-6 col col-md-6','readonly':'readonly'}),
                    'comments':forms.Textarea(attrs={'class':'form-control'}),
                    # 'attachment': forms.FileField(),
                    'disposalExplanation': forms.Textarea(attrs={'class':'form-control', 'readonly':'readonly'}),
                    'fairMarketValue': forms.NumberInput(attrs={'class':'form-control'}),
                    'disposalDate' : forms.DateInput(attrs={'class':'form-control col-sm-6 col col-md-6', 'type':'date'}),
                    'disposalIncome' : forms.NumberInput(attrs={'class':'form-control'}),
                    'disposalProcedure' : forms.Select(attrs={'class':'form-control'}, choices=procedures),
                    'CR_Approval' : forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
                    'Paymentmode' : forms.Select(attrs={'class':'form-control '}, choices=modes),
                    #'CheckedOut' : forms.BooleanField(),
                    'Buyer' : forms.TextInput(attrs={'class':'form-control'}), 

        }
