from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')

#class UserSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = User
#        fields = ['id', 'password', 'is_superuser', 'username', 'first_name', 'last_name', 'email']

class ApplicantSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class CompanySerailizer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields ="__all__"

"""
class MyPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def to_representation(self, value):
       # return six.text_type(value) # returns the string(Python3)/ unicode(Python2) representation now instead of pk 
       return str(value)

class JobsSerailizer(serializers.ModelSerializer):
    company = serializers.ReadOnlyField(source = 'company.company_name')
    class Meta:
        model = Job
        fields = ('title', 'company')

class ComSerializer(serializers.ModelSerializer):
    #jobs = serializers.PrimaryKeyRelatedField(many = True, queryset = Job.objects.all())
    #jobs = serializers.SlugRelatedField("slug_field = 'title'", queryset = Job.objects.all())
    jobs = MyPrimaryKeyRelatedField(many = True, queryset = Job.objects.all())
    class Meta:
        model = Company
        fields = ('company_name','jobs')



class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
"""