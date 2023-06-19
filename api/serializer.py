from rest_framework import serializers
from home.models import AssetTb, Assignment,Verified, staff
from django.contrib.auth.models import User


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetTb

        fields = '__all__'
    # def update(self,instance, validated_data):
    #     instance.ProjectName = validated_data.get('ProjectName', instance.ProjectName)
    #     instance.save()
    #     return instance

class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetTb
        fields = ['Ast_Tag_nbr','AstNo','Asset_Status',]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = staff
        fields = ['Username', 'Firstname', 'Lastname', 'staffrole','profile_pic']
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'