from dataclasses import fields
from django import forms
from . import models

class User_Login(forms.ModelForm):
    class Meta:
        model = models.Applicant
        fields = '__all__'