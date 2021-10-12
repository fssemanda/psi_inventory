from rest_framework import serializers
from home.models import AssetTb,Verified


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetTb

        fields = '__all__'

class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Verified
        fields = '__all__'
