
from django.forms import forms, ModelForm
from home.models import QRCodeClass

class QRform(ModelForm):

    class Meta:

        model = QRCodeClass

        fields = ['Asset']