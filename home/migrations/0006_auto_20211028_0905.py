# Generated by Django 3.2.6 on 2021-10-28 09:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20211028_0324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='EventDate',
        ),
        migrations.RemoveField(
            model_name='events',
            name='EventObject',
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Date_Requested',
            field=models.DateField(default=datetime.datetime(2021, 10, 28, 9, 5, 1, 542450, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Last_Modified',
            field=models.DateField(default=datetime.datetime(2021, 10, 28, 9, 5, 1, 542518, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Request_Modified_Date',
            field=models.DateField(default=datetime.datetime(2021, 10, 28, 9, 5, 1, 542508, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 10, 28, 9, 5, 1, 542055, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='LogDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 28, 9, 5, 1, 545651, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 10, 28, 9, 5, 1, 545598, tzinfo=utc)),
        ),
    ]
