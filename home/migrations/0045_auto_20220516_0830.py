# Generated by Django 3.2.6 on 2022-05-16 08:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0044_auto_20220511_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetrequests',
            name='Date_Requested',
            field=models.DateField(default=datetime.datetime(2022, 5, 16, 8, 30, 0, 329349, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Last_Modified',
            field=models.DateField(default=datetime.datetime(2022, 5, 16, 8, 30, 0, 329381, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Request_Modified_Date',
            field=models.DateField(default=datetime.datetime(2022, 5, 16, 8, 30, 0, 329371, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='Asset_Condition',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('Good', 'Good'), ('Fair', 'Fair'), ('Bad', 'Bad'), ('Obsolete', 'Obsolete'), ('Faulty', 'Faulty')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='Availability',
            field=models.CharField(blank=True, choices=[('AVAILABLE', 'AVAILABLE'), ('ASSIGNED', 'ASSIGNED'), ('TO BE ASSIGNED', 'TO BE ASSIGNED'), ('UNAVAILABLE FOR ASSIGNMENT', 'UNAVAILABLE FOR ASSIGNMENT'), ('MISSING', 'MISSING'), ('LOST', 'LOST'), ('FAULTY', 'FAULTY'), ('DUE FOR DISPOSAL', 'DUE FOR DISPOSAL'), ('DISPOSED-OF', 'DISPOSED-OF'), ('WRITTEN OFF', 'WRITTEN OFF'), ('FOR INSURANCE REPLACEMENT', 'FOR INSURANCE REPLACEMENT'), ('NOT APPLICABLE ON THIS DEVICE', 'NOT APPLICABLE ON THIS DEVICE')], max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='Project_Name',
            field=models.CharField(blank=True, choices=[('WHP', 'WHP'), ('MERCK', 'MERCK'), ('MUM', 'MUM'), ('PFIZER', 'PFIZER'), ('PROGRAM INCOME', 'PROGRAM INCOME'), ('MANE', 'MANE'), ('CMS PROJECT', 'CMS PROJECT'), ('TUNZA', 'TUNZA'), ('COMMERCIAL MARKETS', 'COMMERCIAL MARKETS'), ('CM4FP', 'CM4FP'), ('BERGSTROM FOUNDATION', 'BERGSTROM FOUNDATION'), ('DISC', 'DISC'), ('COMMON COST', 'COMMON COST'), ('HIVST', 'HIVST'), ('CDC', 'CDC'), ('CSF', 'CSF'), ('WIN', 'WIN'), ('NPI', 'NPI'), ('HIVST', 'HIVST'), ('SELFCARE TBG', 'SELFCARE TBG'), ('COVID-19', 'COVID-19'), ('CITY TO CITY', 'CITY TO CITY'), ('DKT', 'DKT'), ('LEAP PROJECT', 'LEAP PROJECT')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 5, 16, 8, 30, 0, 328913, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='AssetCondition',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('Good', 'Good'), ('Fair', 'Fair'), ('Bad', 'Bad'), ('Obsolete', 'Obsolete'), ('Faulty', 'Faulty')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='Availability',
            field=models.CharField(blank=True, choices=[('AVAILABLE', 'AVAILABLE'), ('ASSIGNED', 'ASSIGNED'), ('TO BE ASSIGNED', 'TO BE ASSIGNED'), ('UNAVAILABLE FOR ASSIGNMENT', 'UNAVAILABLE FOR ASSIGNMENT'), ('MISSING', 'MISSING'), ('LOST', 'LOST'), ('FAULTY', 'FAULTY'), ('DUE FOR DISPOSAL', 'DUE FOR DISPOSAL'), ('DISPOSED-OF', 'DISPOSED-OF'), ('WRITTEN OFF', 'WRITTEN OFF'), ('FOR INSURANCE REPLACEMENT', 'FOR INSURANCE REPLACEMENT'), ('NOT APPLICABLE ON THIS DEVICE', 'NOT APPLICABLE ON THIS DEVICE')], max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='LogDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 5, 16, 8, 30, 0, 332361, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='ProjectName',
            field=models.CharField(blank=True, choices=[('WHP', 'WHP'), ('MERCK', 'MERCK'), ('MUM', 'MUM'), ('PFIZER', 'PFIZER'), ('PROGRAM INCOME', 'PROGRAM INCOME'), ('MANE', 'MANE'), ('CMS PROJECT', 'CMS PROJECT'), ('TUNZA', 'TUNZA'), ('COMMERCIAL MARKETS', 'COMMERCIAL MARKETS'), ('CM4FP', 'CM4FP'), ('BERGSTROM FOUNDATION', 'BERGSTROM FOUNDATION'), ('DISC', 'DISC'), ('COMMON COST', 'COMMON COST'), ('HIVST', 'HIVST'), ('CDC', 'CDC'), ('CSF', 'CSF'), ('WIN', 'WIN'), ('NPI', 'NPI'), ('HIVST', 'HIVST'), ('SELFCARE TBG', 'SELFCARE TBG'), ('COVID-19', 'COVID-19'), ('CITY TO CITY', 'CITY TO CITY'), ('DKT', 'DKT'), ('LEAP PROJECT', 'LEAP PROJECT')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 5, 16, 8, 30, 0, 332310, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='disposal',
            name='disposalDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 5, 16, 8, 30, 0, 332845, tzinfo=utc)),
        ),
    ]