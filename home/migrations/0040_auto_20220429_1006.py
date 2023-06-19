# Generated by Django 3.2.6 on 2022-04-29 10:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0039_auto_20220429_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetrequests',
            name='Date_Requested',
            field=models.DateField(default=datetime.datetime(2022, 4, 29, 10, 6, 34, 658336, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Last_Modified',
            field=models.DateField(default=datetime.datetime(2022, 4, 29, 10, 6, 34, 658369, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Request_Modified_Date',
            field=models.DateField(default=datetime.datetime(2022, 4, 29, 10, 6, 34, 658359, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='Company',
            field=models.CharField(blank=True, default='351', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 29, 10, 6, 34, 657855, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='LogDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 29, 10, 6, 34, 661214, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 29, 10, 6, 34, 661168, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='disposal',
            name='disposalDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 29, 10, 6, 34, 661735, tzinfo=utc)),
        ),
    ]
