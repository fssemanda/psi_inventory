# Generated by Django 3.2.6 on 2022-07-13 15:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0050_auto_20220712_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetrequests',
            name='Date_Requested',
            field=models.DateField(default=datetime.datetime(2022, 7, 13, 15, 36, 3, 18800, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Last_Modified',
            field=models.DateField(default=datetime.datetime(2022, 7, 13, 15, 36, 3, 18832, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Request_Modified_Date',
            field=models.DateField(default=datetime.datetime(2022, 7, 13, 15, 36, 3, 18822, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 7, 13, 15, 36, 3, 18283, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='LogDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 13, 15, 36, 3, 21911, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 7, 13, 15, 36, 3, 21840, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='disposal',
            name='disposalDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 7, 13, 15, 36, 3, 22451, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staffrole',
            field=models.CharField(choices=[('User', 'User'), ('Admin', 'Admin'), ('Supervisor', 'Supervisor'), ('Warehouse', 'Warehouse'), ('Supply Chain', 'Supply Chain'), ('SalesApprover', 'SalesApprover'), ('Accountant', 'Accountant'), ('Finance', 'Finance'), ('Assistant Accountant AR', 'Assistant Accountant AR'), ('Systems Administrator', 'Systems Administrator'), ('SIL Officer', 'SIL Officer'), ('Fleet Supervisor', 'Fleet Supervisor'), ('Asset Manager', 'Asset Manager')], max_length=30, null=True),
        ),
    ]
