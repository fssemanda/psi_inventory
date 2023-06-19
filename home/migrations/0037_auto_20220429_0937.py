# Generated by Django 3.2.6 on 2022-04-29 09:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_auto_20220429_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetrequests',
            name='Date_Requested',
            field=models.DateField(default=datetime.datetime(2022, 4, 29, 9, 37, 36, 34573, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Last_Modified',
            field=models.DateField(default=datetime.datetime(2022, 4, 29, 9, 37, 36, 34605, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Request_Modified_Date',
            field=models.DateField(default=datetime.datetime(2022, 4, 29, 9, 37, 36, 34595, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 29, 9, 37, 36, 34151, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='LogDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 29, 9, 37, 36, 37612, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 29, 9, 37, 36, 37563, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='disposal',
            name='disposalDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 29, 9, 37, 36, 38075, tzinfo=utc)),
        ),
    ]
