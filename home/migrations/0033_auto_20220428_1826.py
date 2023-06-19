# Generated by Django 3.2.6 on 2022-04-28 18:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_auto_20220428_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verified',
            name='Ast_Tag_nbr',
        ),
        migrations.RemoveField(
            model_name='verified',
            name='Comments',
        ),
        migrations.RemoveField(
            model_name='verified',
            name='Location',
        ),
        migrations.RemoveField(
            model_name='verified',
            name='Status',
        ),
        migrations.RemoveField(
            model_name='verified',
            name='Username',
        ),
        migrations.AddField(
            model_name='verified',
            name='Device',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='verified',
            name='Name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Date_Requested',
            field=models.DateField(default=datetime.datetime(2022, 4, 28, 18, 26, 2, 505760, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Last_Modified',
            field=models.DateField(default=datetime.datetime(2022, 4, 28, 18, 26, 2, 505794, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Request_Modified_Date',
            field=models.DateField(default=datetime.datetime(2022, 4, 28, 18, 26, 2, 505784, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 28, 18, 26, 2, 505278, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='LogDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 28, 18, 26, 2, 511591, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 28, 18, 26, 2, 511541, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='disposal',
            name='disposalDate',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 28, 18, 26, 2, 512057, tzinfo=utc)),
        ),
    ]