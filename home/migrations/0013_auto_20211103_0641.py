# Generated by Django 3.2.6 on 2021-11-03 06:41

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20211103_0606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetrequests',
            name='Date_Requested',
            field=models.DateField(default=datetime.datetime(2021, 11, 3, 6, 41, 53, 357312, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Last_Modified',
            field=models.DateField(default=datetime.datetime(2021, 11, 3, 6, 41, 53, 357343, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Request_Modified_Date',
            field=models.DateField(default=datetime.datetime(2021, 11, 3, 6, 41, 53, 357333, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 11, 3, 6, 41, 53, 356939, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='LogDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 3, 6, 41, 53, 360236, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 11, 3, 6, 41, 53, 360190, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='disposal',
            name='asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.assettb'),
        ),
        migrations.AlterField(
            model_name='disposal',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='img'),
        ),
    ]
