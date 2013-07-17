'''
Created on 17-Jul-2013

@author: Nikhilesh
'''

from django import forms
from Login.models import UserDetails
from django.utils import timezone

class UserCreate(forms.ModelForm):
    usertype=(
              ('select' , 'Please select user type'),
              ('Administrator' , 'Administrator'),
              ('Employee' , 'Employee')
         )
    emailid = forms.CharField(error_messages={'required': 'Please enter email id'})
    user_level = forms.CharField()
    user_weight = forms.CharField()
    type = forms.ChoiceField(choices=usertype, error_messages={'required': 'Please select user type'})
    
    class Meta():
        model=UserDetails
        fields = ('emailid','user_level', 'user_weight', 'type',)