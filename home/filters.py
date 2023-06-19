
import django_filters
from django import forms
from django_filters import filters, ChoiceFilter

from .models import *

AssetType = [
        ("Vehicle", "Vehicle"), ("Computer-Desktop", "Computer-Desktop"),
        ("Computer-Laptop", "Computer-Laptop"), ("Medical Equipment", "Medical Equipment"),
        ("Tablet", "Tablet"), ("Phone", "Phone"),
        ("Computer Accessory", "Computer Accessory"), ("Networking Equipment", "Networking Equipment"),
        ("Projector", "Projector"), ("Printer", "Printer"),
        ("PhotoCopier", "PhotoCopier"), ("Multi Functional Printer", "Multi Functional Printer"),
        ("Table", "Table"), ("Chair", "Chair"),
        ("Office Accessory", "Office Accessory"), ("Not Applicable", "Not Applicable"),

    ]

class AssetFilter(django_filters.FilterSet):
    class Meta:
        model = AssetTb
        fields = ['Ast_Tag_nbr','Serial_No', 'Asset_Type',
                  'PurchaseDate',
                  ]

        widgets = {'Device_Type': forms.Select(attrs={}, choices=AssetType)}
