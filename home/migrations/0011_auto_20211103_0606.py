# Generated by Django 3.2.6 on 2021-11-03 06:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20211103_0521'),
    ]

    operations = [
        migrations.AddField(
            model_name='disposal',
            name='attachment',
            field=models.FileField(null=True, upload_to='img'),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Date_Requested',
            field=models.DateField(default=datetime.datetime(2021, 11, 3, 6, 6, 3, 655242, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Last_Modified',
            field=models.DateField(default=datetime.datetime(2021, 11, 3, 6, 6, 3, 655274, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Request_Modified_Date',
            field=models.DateField(default=datetime.datetime(2021, 11, 3, 6, 6, 3, 655264, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 11, 3, 6, 6, 3, 654863, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='LogDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 3, 6, 6, 3, 658191, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 11, 3, 6, 6, 3, 658146, tzinfo=utc)),
        ),
    ]
