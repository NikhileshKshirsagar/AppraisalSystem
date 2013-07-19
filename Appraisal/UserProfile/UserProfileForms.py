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
    firstname = forms.CharField(error_messages={'required': 'Please enter user first name'}, widget=forms.TextInput(attrs={'class':'tableRow span4 search-query'}))
    lastname = forms.CharField(error_messages={'required': 'Please enter user last name'}, widget=forms.TextInput(attrs={'class':'tableRow span4 search-query'}))
    emailid = forms.CharField(error_messages={'required': 'Please enter email id'}, widget=forms.TextInput(attrs={'class':'tableRow span4 search-query'}))
    user_level = forms.CharField()
    user_weight = forms.CharField()
    type = forms.ChoiceField(choices=usertype, error_messages={'required': 'Please select user type'},widget=forms.Select(attrs={'class':'tableRow span4 search-query', 'style': 'border-radius: 15px 15px 15px 15px;'}))
    
    class Meta():
        model=UserDetails
        fields = ('firstname','lastname','emailid','user_level', 'user_weight', 'type',)