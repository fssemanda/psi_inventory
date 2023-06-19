# Generated by Django 3.2.6 on 2022-07-12 11:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0049_auto_20220712_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='disposal',
            name='BuyerType',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Date_Requested',
            field=models.DateField(default=datetime.datetime(2022, 7, 12, 11, 54, 17, 951853, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Last_Modified',
            field=models.DateField(default=datetime.datetime(2022, 7, 12, 11, 54, 17, 951887, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Request_Modified_Date',
            field=models.DateField(default=datetime.datetime(2022, 7, 12, 11, 54, 17, 951876, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 7, 12, 11, 54, 17, 951452, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='LogDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 12, 11, 54, 17, 954654, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 7, 12, 11, 54, 17, 954610, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='disposal',
            name='disposalDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 7, 12, 11, 54, 17, 955099, tzinfo=utc)),
        ),
    ]