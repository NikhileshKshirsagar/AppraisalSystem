'''
Created on 17-Jul-2013

@author: Nikhilesh
'''

from django import forms
from Login.models import UserDetails, UserAttributes, Language, UserAttributes
from django.utils import timezone
from cProfile import label

class UserCreate(forms.ModelForm):
    usertype=(
              ('select' , 'Select user type'),
              ('Administrator' , 'Administrator'),
              ('Employee' , 'Employee')
         )
    firstname = forms.CharField(label='First name', error_messages={'required': 'Please enter user first name'}, widget=forms.TextInput(attrs={'class':'tableRow span5 search-query'}))
    lastname = forms.CharField(label='Last name',error_messages={'required': 'Please enter user last name'}, widget=forms.TextInput(attrs={'class':'tableRow span5 search-query'}))
    emailid = forms.CharField(label='Email address',error_messages={'required': 'Please enter email id'}, widget=forms.TextInput(attrs={'class':'tableRow span5 search-query'}))
    user_level = forms.CharField()
    user_weight = forms.CharField()
    type = forms.ChoiceField(label='User type',choices=usertype, error_messages={'required': 'Please select user type'},widget=forms.Select(attrs={'class':'tableRow span5 search-query', 'style': 'border-radius: 15px 15px 15px 15px;'}))
    
    def save(self,  userId,commit=True):
        obj_userForm = super(UserCreate, self).save(commit=False)
        print "Form values"
        print self.data['emailid']
        obj_userForm.emailid = self.data['emailid']
        obj_userForm.user_level = self.data['user_level']
        obj_userForm.user_weight = self.data['user_weight']
        obj_userForm.type = self.data['type']
        obj_userForm.modified_by = userId
        obj_userForm.modified_on = timezone.now()
        obj_userForm.save()
    
    def clean(self):
        #data = self.cleaned_data
        print "Inside clean"
        print self.cleaned_data['type']
        if self.cleaned_data['type'] == "select":
            self.fields['type'].error_messages["errorUserType"]  = "Please select user type"
            raise forms.ValidationError(self.fields['type'].error_messages["errorUserType"])
        return self.cleaned_data
    class Meta():
        model=UserDetails
        fields = ('firstname','lastname','emailid','user_level', 'user_weight', 'type',)
        
class UserProfile_UserDetailForm(forms.ModelForm):
    class Meta():
        model=UserDetails
        fields = ('username','password',)
    
class UserProfile_LanguageForm:
    newLanguage = forms.CharField(label=("Add new language"), required=False)
    choices = [(obj_language.language_id, obj_language.language) for obj_language in Language.objects.all()]
    language = forms.ChoiceField(choices = choices)
    class Meta():
        model=UserAttributes
        fields = ('tech_working','tech_known','tech_willing','language_working','language_known','language_willing')
        
#class UserProfile_DesignationForm:
    