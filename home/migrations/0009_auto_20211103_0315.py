# Generated by Django 3.2.6 on 2021-11-03 03:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20211029_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetrequests',
            name='Date_Requested',
            field=models.DateField(default=datetime.datetime(2021, 11, 3, 3, 15, 59, 816835, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Last_Modified',
            field=models.DateField(default=datetime.datetime(2021, 11, 3, 3, 15, 59, 816867, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Request_Modified_Date',
            field=models.DateField(default=datetime.datetime(2021, 11, 3, 3, 15, 59, 816857, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='Asset_Condition',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('Good', 'Good'), ('Fair', 'Fair'), ('Bad', 'Bad'), ('Faulty', 'Faulty'), ('Faulty-Due For Disposal', 'Faulty-Due For Disposal'), ('Due for Disposal', 'Due for Disposal'), ('Disposed-Of', 'Disposed-Of'), ('Written Off', 'Written Off')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 11, 3, 3, 15, 59, 816401, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='AssetCondition',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('Good', 'Good'), ('Fair', 'Fair'), ('Bad', 'Bad'), ('Faulty', 'Faulty'), ('Faulty-Due For Disposal', 'Faulty-Due For Disposal'), ('Due for Disposal', 'Due for Disposal'), ('Disposed-Of', 'Disposed-Of'), ('Written Off', 'Written Off')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='LogDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 3, 3, 15, 59, 820321, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 11, 3, 3, 15, 59, 820275, tzinfo=utc)),
        ),
    ]
