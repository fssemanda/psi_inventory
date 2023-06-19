# Generated by Django 3.2.6 on 2022-04-28 18:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_auto_20220428_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetrequests',
            name='Date_Requested',
            field=models.DateField(default=datetime.datetime(2022, 4, 28, 18, 31, 35, 938859, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Last_Modified',
            field=models.DateField(default=datetime.datetime(2022, 4, 28, 18, 31, 35, 938889, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Request_Modified_Date',
            field=models.DateField(default=datetime.datetime(2022, 4, 28, 18, 31, 35, 938880, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 28, 18, 31, 35, 938442, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='LogDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 28, 18, 31, 35, 941739, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 28, 18, 31, 35, 941689, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='disposal',
            name='disposalDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 28, 18, 31, 35, 942192, tzinfo=utc)),
        ),
    ]
