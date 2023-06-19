from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
#from datetime import datetime

AssetType = [
    ("VEHICLE", "VEHICLE"), ("DESKTOP", "DESKTOP"),
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
    ("AIR CONDITIONER", "AIR CONDITIONER"),("SERVER RACK","SERVER RACK")

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
    ("81001UG", "81001UG"),
    ("87001UG", "87001UG"),
   

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
    ('VIYA','VIYA'),
    ('BABYCHECKER','BABYCHECKER'),
    ('MAVERICK','MAVERICK'),


]

conditions = [
     ("New", "New"),
    ("Good", "Good"),
    ("Fair", "Fair"),
    ("Bad", "Bad"),
    ("Obsolete", "Obsolete"),
    ("Faulty", "Faulty"),


]
Responses = [("Pending", "Pending"),
                 ("Approved", "Approved"),
                 ("Rejected", "Rejected"),
                 ("User Accepted", "User Accepted"),
                 ("Returned", "Returned"),
                     ("In process","In Process"),
    ("Fully Approved","Fully Approved"),
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
('DISPOSED-OF','DISPOSED-OF'),



]
procedures = [
    ("Donated", "Donated"),("Sold","Sold"),
    ("Auctioned", "Auctioned"),("Written-Off","Written-off"),
]
options = [
    ("Pending","Pending"),
    ("Approved","Approved"),
    ("Rejected","Rejected"),
    ("In Process","In Process"),
    ("Fully Approved","Fully Approved"),
    
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
roles = [
        ("User", "User"),
        ("Admin", "Admin"),
        ("Supervisor", "Supervisor"),

        ("Warehouse", "Warehouse"),
        ("Supply Chain", "Supply Chain"),
        ("SalesApprover", "SalesApprover"),
        ("Accountant-AP", "Accountant-AP"),
        ("Finance", "Finance"),
        ("Assistant Accountant AR", "Assistant Accountant AR"),
        ("Systems Administrator", "Systems Administrator"),
        ("SIL Officer", "SIL Officer"),
        ("Fleet Supervisor", "Fleet Supervisor"),
        ("Asset Manager", "Asset Manager"),
        ('IT Support Assistant','IT Support Assistant'),
('Accountant - Accounts Payables','Accountant - Accounts Payables'),
('Advocacy and Communications Officer','Advocacy and Communications Officer'),
('Advocacy and Partnerships Coordinator','Advocacy and Partnerships Coordinator'),
('Assistant Accountant - Accounts Receivables','Assistant Accountant - Accounts Receivables'),
('Assistant Accountant-Treasury','Assistant Accountant-Treasury'),
('Country Digital Manager','Country Digital Manager'),
('Country Representative','Country Representative'),
('CYBER INTER-PERSONAL COMMUNICATION COORDINATOR','CYBER INTER-PERSONAL COMMUNICATION COORDINATOR'),
('Deputy Country Representative','Deputy Country Representative'),

('Director Programs','Director Programs'),
('Director of Finance and Administration','Director of Finance and Administration'),

('Digital Community Engagement Officer','Digital Community Engagement Officer'),
('Brand Manager','Brand Manager'),
('DISC Project Coordinator','DISC Project Coordinator'),
('DISC Project Lead','DISC Project Lead'),
('District Mobilization Officer - Bergstrom','District Mobilization Officer - Bergstrom'),
('District Mobilization Officer- SBC','District Mobilization Officer- SBC'),
('Driver','Driver'),
('Driver/Logistics Assistant - Bergstrom','Driver/Logistics Assistant - Bergstrom'),
('Emergency Medical Services Coordinator','Emergency Medical Services Coordinator'),
('Finance and Administration Director','Finance and Administration Director'),
('Financial Accounts Manager','Financial Accounts Manager'),
('Financial Analytics Manager','Financial Analytics Manager'),
('Fleet Supervisor','Fleet Supervisor'),
('Head of Regional Operations','Head of Regional Operations'),
('Head of Finance','Head of Finance'),
('Accounts Assistant','Accounts Assistant'),
('Financial Analyst','Financial Analyst'),

('Head of Strategic Information and Learning','Head of Strategic Information and Learning'),
('Head -Social Behavioral Change','Head -Social Behavioral Change'),
('Health Services Coordinator','Health Services Coordinator'),
('Human Resources and Administration Assistant','Human Resources and Administration Assistant'),
('Human Resources and Administration Coordinator','Human Resources and Administration Coordinator'),
('Human Resources and Administration Manager','Human Resources and Administration Manager'),
('"Implementation Learning and Adaptation Lead','Implementation Learning and Adaptation Lead'),
('Internal Auditor Manager','Internal Auditor Manager'),
('Knowledge Management Coordinator','Knowledge Management Coordinator'),
('Medical Detailer','Medical Detailer'),
('Medical Detailer','Medical Detailer'),
('Medical Detailer Supervisor','Medical Detailer Supervisor'),
('Monitoring and Evaluation Officer','Monitoring and Evaluation Officer'),
('Payroll & Management Accountant','Payroll & Management Accountant'),
('Policy and Adaptive Supervisor','Policy and Adaptive Supervisor'),
('Procurement Officer','Procurement Officer'),
('Project Director - MaNe Kampala Slum project','Project Director - MaNe Kampala Slum project'),
('Project Manager-SHIPS','Project Manager-SHIPS'),
('Quality Assurance Officer-Bergstrom','Quality Assurance Officer-Bergstrom'),
('Research Manager','Research Manager'),
('Revolving/Surgical Team Lead','Revolving/Surgical Team Lead'),
('Sales and Marketing Manager','Sales and Marketing Manager'),
('Sales Coordinator','Sales Coordinator'),
('Sales Representative','Sales Representative'),
('Sales Representative','Sales Representative'),
('SBC Coordinator','SBC Coordinator'),
('Senior Technical Advisor','Senior Technical Advisor'),
('"Senior Technical Advisor HIV','Senior Technical Advisor HIV'),
('"Senior Technical Advisor I,SRH','Senior Technical Advisor SRH'),
('Sexual Reproductive Health Officer -Bergstrom','Sexual Reproductive Health Officer -Bergstrom'),
('Social Behavioral Change Coordinator','Social Behavioral Change Coordinator'),
('Social Behavioral Change Officer','Social Behavioral Change Officer'),
('Social Entreprise Lead East Africa','Social Entreprise Lead East Africa'),
('Strategic Communications Manager','Strategic Communications Manager'),
('Strategic Information and Learning Coordinator','Strategic Information and Learning Coordinator'),
('Supply Chain Manager','Supply Chain Manager'),
('Systems Administrator','Systems Administrator'),
('Team Lead-Bergstrom','Team Lead-Bergstrom'),
('Technical Learning and Innovations Manager','Technical Learning and Innovations Manager'),
('Temporary Below the Line Activation Assistant','Temporary Below the Line Activation Assistant'),
('Temporary Procurement Assistant','Temporary Procurement Assistant'),
('Temporary Quality Assurance Officer','Temporary Quality Assurance Officer'),
('Temporary Social Behavioral Change Officer','Temporary Social Behavioral Change Officer'),
('Assistant Quality Assurance Officer','Assistant Quality Assurance Officer'),
('Quality Assurance Officer','Quality Assurance Officer'),

('Youth Friendly Services Officer','Youth Friendly Services Officer'),


    ]    
class Staff_Emails(models.Model):
    Email =  models.CharField(unique = True, max_length=50)
    
    def __str__(self):
        return self.Email
    
class staff(models.Model):

    Username = models.CharField(max_length=50, primary_key=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=30)
    Lastname = models.CharField(max_length=30)
    email = models.EmailField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    profile_pic = models.ImageField(default=("profile1.png"), null=True, blank=True)
    staffrole = models.CharField(max_length=60, null=True, choices=roles)
    staff_status = models.BooleanField(default=True)
    Manager = models.ForeignKey('self', on_delete=models.CASCADE,null=True, blank=True)
    
   

    def __str__(self):
        return f'{self.Username}'

blanks =[
    ('None','None'),
    ('Blank',''),
]

class AssetTb(models.Model):

    Company = models.CharField(max_length=10, default='351', blank =True, null=True)
    #Blank_Column = models.CharField(max_length=100, choices = blanks, default='0', blank =True,null=True)
    Ast_Tag_nbr = models.CharField(max_length=100, null=False, primary_key=True)
    Serial_No = models.CharField(max_length=100, null=True, blank=True)
    AstNo = models.CharField(max_length=50, null=True, blank=True)
    Vendor = models.CharField(max_length=100, blank=True, null=True)
    Ast_description = models.CharField(max_length=100, null=True,blank =True,)
    Item_Cost_UGX = models.FloatField(blank=True)
    Item_Cost_USD = models.FloatField(blank = True)
    Asset_Type = models.CharField(max_length=50, null=True, choices=AssetType, blank=True)
    Model_No = models.CharField(max_length=50, null=True, blank=True)
    Project = models.CharField(max_length=100, null=True,blank =True, choices=Activities)
    Asset_Condition = models.CharField(max_length=100, null=True, choices=conditions, blank=True)
    Asset_Status = models.CharField(max_length=100, null=True, choices=statuses,blank =True, default="UNVERIFIED")
    Project_Name = models.CharField(max_length=100, null=True, blank =True,choices=Activity_Names)
    Availability = models.CharField(max_length=40, choices=AvailStatus, blank=True, null=True)
    Location = models.CharField(max_length=40, choices=Locations, blank=True, null=True)
    PurchaseDate = models.DateField(default=now(), blank = True)
    Ast_Currency = models.CharField(max_length=100, choices = currencies, default='UGX',blank =True,)
    Comments = models.CharField(max_length=1000, blank=True,default='', null=True)

    def __str__(self):
        return f'{self.Ast_Tag_nbr}'



class AssetRequests(models.Model):

    Device_Type = models.CharField(max_length=50, null=True, choices=AssetType, blank=True)
    Assigned_Device = models.ForeignKey(AssetTb, on_delete=models.CASCADE, null=True, blank=True)
    Status = models.CharField(max_length=50, null=True, choices=Responses, default="Pending")
    Username = models.ForeignKey(staff, on_delete=models.CASCADE)
    Date_Requested = models.DateField(default=now())
    Reason = models.TextField(blank=True, max_length=1500, null=True)
    Request_Modified_Date = models.DateField(default=now())
    Last_Modified = models.DateField(default=now())
    Last_Modified_by = models.CharField(max_length=500, blank=True)

    SupervisorApproval = models.CharField(max_length=15, null=True, choices=Responses, blank=True, default='Pending')
    SupervisorApprovalComments = models.CharField(max_length=1000, blank=True, null=True)

    AssetManagerApproval = models.CharField(max_length=15, null=True, blank=True, choices=Responses, default='Pending')
    AssetMangerApprovalComments = models.CharField(max_length=1000, blank=True, null=True)

    FinanceManagerApproval = models.CharField(max_length=15, blank=True, null=True, choices=Responses,
                                           default='Pending')
    FinanceManagerApprovalComments = models.CharField(max_length=1000, blank=True, null=True)

    UserAcceptance = models.CharField(max_length=15, blank=True, null=True, choices=Responses,
                                           default='Pending')
    #Postsave signal for this model will include that if a user has accepted the request the Asset Assignments table is
    #Automatically updated with the user details and asset assignment details. Log file should then be updated that the user has accepted the device they requested for

    def __str__(self):
        return f'{self.id} {self.Assigned_Device} {self.Username}'

class PoolRequests(models.Model):
    pass


class CsvUpload(models.Model):
    file_name = models.FileField(upload_to='img')
    Date_uploaded = models.DateTimeField(auto_now_add=True)
    Parsed = models.BooleanField(default=False)

    def __str__(self):
        return f'File ID: {self.id}'


class QRCodeClass(models.Model):
    QRimage = models.ImageField(default=("profile1.png"), null=True, blank=True)
    Asset = models.ForeignKey(AssetTb, on_delete=models.SET_NULL, null=True)
    path = models.CharField(max_length=100)

    def __str__(self):
        return f'Image ID:{self.id}'


class UserAsset(models.Model):
    staff = models.ForeignKey(staff, on_delete=models.CASCADE, null=True, blank=True)
    AssignedAsset = models.ForeignKey(AssetTb, on_delete=models.CASCADE, null=True)


class Verified(models.Model):

    # Ast_Tag_nbr = models.ForeignKey(AssetTb,on_delete=models.SET_NULL, null=True, blank=True)
    # Username = models.ForeignKey(staff, on_delete=models.CASCADE, null=True, blank=True)
    # Status = models.CharField(max_length=30, blank=True, default="Unverified")
    # Location = models.CharField(max_length=40, choices=Locations, blank=True, null=True)
    # Comments = models.CharField(max_length=1000, blank=True)
    # def __str__(self):
    #     return f'{self.id}'
    Name = models.CharField(max_length=100, blank=True)
    Device = models.ForeignKey(AssetTb, on_delete=models.CASCADE, null=True)

class Assignment(models.Model):

    Username = models.ForeignKey(staff, on_delete=models.CASCADE, null=True, blank=True)
    Ast_Tag_nbr = models.ForeignKey(AssetTb, on_delete=models.CASCADE, null=True, blank=True, unique=True)

    def __str__(self):
        return f'{self.id}{self.Username}'


class Ajaxsend(models.Model):
    name = models.CharField(max_length=100)
    result = models.CharField(max_length=200)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name
ApprovalResponses = [
                 ("Approved", "Approved"),
                 ("Rejected", "Rejected"),
                 ]

class ChangeLog(models.Model):

    Requester = models.ForeignKey(User, on_delete=models.CASCADE)
    AstTagnbr = models.CharField(max_length=100, null=True)
    SerialNo = models.CharField(max_length=100, null=True, blank=True)
    AstNo = models.CharField(max_length=50, null=True, blank=True)
    Vendor = models.CharField(max_length=100, blank=True, null=True)
    AstDescription = models.CharField(max_length=100, null=True)
    ItemCostUGX = models.FloatField(null=True, default=0.0)
    ItemCostUSD = models.FloatField(null=True, default=0.0)
    AssetType = models.CharField(max_length=50, null=True, choices=AssetType, blank=True)
    ModelNo = models.CharField(max_length=50, null=True, blank=True)
    Project = models.CharField(max_length=100, null=True, choices=Activities, blank=True)
    AssetCondition = models.CharField(max_length=100, null=True, choices=conditions, blank=True)
    AssetStatus = models.CharField(max_length=100, null=True, choices=statuses, blank=True)
    ProjectName = models.CharField(max_length=100, null=True, choices=Activity_Names, blank=True)
    Availability = models.CharField(max_length=40, choices=AvailStatus, blank=True, null=True)
    Location = models.CharField(max_length=40, choices=Locations, blank=True, null=True)
    PurchaseDate = models.DateField(default=now(), blank=True)
    Modifications = models.CharField(max_length=2000, blank=True, null=True)
    RequesterComments = models.CharField(max_length=1000, null=True, blank=True)
    FAMApproval = models.CharField(max_length=15, null=True, blank=True, choices=ApprovalResponses, default='Pending')
    FAMApprovalComments =models.CharField(max_length=100,null=True,blank=True)
    LogDate = models.DateTimeField(default=now(), blank=True)

    def __str__(self):
        return self.AstTagnbr




class Disposal(models.Model):
    '''Checked Out option tells if as asset is has been disposed off already'''
    Ast_Tag_nbr = models.ForeignKey(AssetTb, on_delete=models.CASCADE, unique=True)
    disposalDate = models.DateField(default='2022-11-11', blank = True)
    disposalIncome = models.FloatField(null=True, blank=True, default=0.0)
    fairMarketValue = models.FloatField(null=True, blank=True)
    disposalProcedure = models.CharField(max_length=30, choices=procedures, blank=True)
    disposalExplanation = models.CharField(max_length=100, null=True, blank=True)
    CR_Approval = models.CharField(max_length=30, choices=options,default='Pending', blank=True)
    comments = models.CharField(max_length=1000, null=True, blank=True)
    attachment = models.FileField(upload_to='documents',null=True,blank=True)
    Paymentmode = models.CharField(max_length=20, blank=True, null=True, choices=modes)
    
    CheckedOut =  models.BooleanField(default=False)
    Buyer = models.CharField(max_length=50, null=True, blank=True)
    BuyerType = models.CharField(max_length=50, null=True, blank=True)
    

    def __str__(self):
        return f'{self.Ast_Tag_nbr}'
        
eventTypes=[
    ('Asset Addition','Asset Addition'),
    ('Asset Modification','Asset Modification'),
    ('Asset Deletion','Asset Deletion'),
    ('Asset Request','Asset Request'),
    ('Asset Assignment','Asset Assignment'),
    ('Account Created','Account Created'),
    ('Login Event','Login Event'),
    ('Failed Login Event','Failed Login Event'),
    ('Login Event','Login Event'),
    ('Logout Event','Logout Event'),
    ('Asset Withdrawal','Asset Withdrawal'),
]
class Events(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    #EventDate = models.DateTimeField(default=datetime.now, blank=True)
    #EventObject = models.CharField(max_length=100, blank=True, null=True)
    EventType = models.CharField(max_length=30, choices=eventTypes)
    EventSummary = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.EventType


class DeleteAssignment(models.Model):
    AssignmentID = models.ForeignKey(Assignment,blank=False, on_delete=models.CASCADE)
    Response =  models.CharField(max_length=20, choices=options, default="Pending")
    Comments =  models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.AssignmentID}'
    
class FileUploads(models.Model):
    file_name = models.FileField(upload_to='documents')
    Date_uploaded = models.DateTimeField(auto_now_add=True)
    Parsed = models.BooleanField(default=False)
    
    def __str__(self):
        return f'File Name:{self.file_name}'

    
