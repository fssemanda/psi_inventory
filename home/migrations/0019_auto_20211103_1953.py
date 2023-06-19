# Generated by Django 3.2.6 on 2021-11-03 19:53

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20211103_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetrequests',
            name='Date_Requested',
            field=models.DateField(default=datetime.datetime(2021, 11, 3, 19, 53, 46, 567951, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Last_Modified',
            field=models.DateField(default=datetime.datetime(2021, 11, 3, 19, 53, 46, 567984, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assetrequests',
            name='Request_Modified_Date',
            field=models.DateField(default=datetime.datetime(2021, 11, 3, 19, 53, 46, 567973, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assettb',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 11, 3, 19, 53, 46, 567539, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='LogDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 3, 19, 53, 46, 570934, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='PurchaseDate',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 11, 3, 19, 53, 46, 570889, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='disposal',
            name='Ast_Tag_nbr',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.assettb'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='disposal',
            name='CR_Approval',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=30),
        ),
        migrations.AlterField(
            model_name='disposal',
            name='disposalDate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='disposal',
            name='disposalIncome',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='disposal',
            name='disposalProcedure',
            field=models.CharField(blank=True, choices=[('Donated', 'Donated'), ('Sold', 'Sold'), ('Auctioned', 'Auctioned'), ('Written-Off', 'Written-off')], max_length=30),
        ),
        migrations.AlterField(
            model_name='disposal',
            name='fairMarketValue',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
