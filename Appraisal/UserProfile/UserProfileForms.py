'''
Created on 17-Jul-2013

@author: Nikhilesh
'''

from django import forms
from Login.models import UserDetails, UserAttributes, Language, UserAttributes, Designation
from django.utils import timezone
from cProfile import label

class UserCreate(forms.ModelForm):
    usertype=(
              ('select' , 'Select user type'),
              ('Administrator' , 'Administrator'),
              ('Employee' , 'Employee')
         )
    firstname = forms.CharField(label='First name', error_messages={'required': 'Please enter user first name.'}, widget=forms.TextInput(attrs={'class':'tableRow span5 search-query textSearch'}))
    lastname = forms.CharField(label='Last name',error_messages={'required': 'Please enter user last name.'}, widget=forms.TextInput(attrs={'class':'tableRow span5 search-query'}))
    emailid = forms.CharField(label='Email address',error_messages={'required': 'Please enter email address.'}, widget=forms.TextInput(attrs={'class':'tableRow span5 search-query'}))
    user_level = forms.CharField()
    user_weight = forms.CharField()
    type = forms.ChoiceField(label='User type',choices=usertype, widget=forms.Select(attrs={'class':'tableRow span5 search-query', 'style': 'border-radius: 15px 15px 15px 15px;'}))
    action = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden', 'value' : 'Alpha', 'id' : 'action'}))
    
    def save(self,  userId,commit=True):
        obj_userForm = super(UserCreate, self).save(commit=False)
        obj_userForm.emailid = self.data['emailid']
        obj_userForm.user_level = self.data['user_level']
        obj_userForm.user_weight = self.data['user_weight']
        obj_userForm.type = self.data['type']
        obj_userForm.modified_by = userId
        obj_userForm.modified_on = timezone.now()
        obj_userForm.save()
        
    def clean_emailid(self):
        try:
            s_existingEmail = UserDetails.objects.get(emailid=self.cleaned_data['emailid']).emailid
        except UserDetails.DoesNotExist:
            s_existingEmail = ''
               
        if s_existingEmail != '' and s_existingEmail ==  self.cleaned_data['emailid'] and self.data['action'] == "Alpha":
            raise forms.ValidationError("Email address already exists.")
        return self.cleaned_data['emailid']
    
    def clean_type(self):
        if self.cleaned_data['type'] == "select":
            raise forms.ValidationError("Please select user type.")
        return self.cleaned_data['type']
    
    def clean_user_level(self):
        if self.cleaned_data['user_level'] == '0' :
            raise forms.ValidationError("Please set the user level.")
        return self.cleaned_data['user_level']
    
    def clean_user_weight(self):
        if self.cleaned_data['user_weight'] == '0' :
            raise forms.ValidationError("Please set the user weight.")
        return self.cleaned_data['user_weight']
        
    class Meta():
        model=UserDetails
        fields = ('firstname','lastname','emailid','user_level', 'user_weight', 'type', 'action',)
        
class userListForm(forms.ModelForm):
    class Meta():
        model=UserDetails
        fields = ('firstname','lastname','emailid',)
        
class UserProfile_UserDetailForm(forms.ModelForm):
    class Meta():
        model=UserDetails
        fields = ('username','password',)
    
class UserProfile_LanguageForm(forms.ModelForm):
    newLanguage = forms.CharField(label=("Add new language"), required=False)
    choices = [(obj_language.language_id, obj_language.language) for obj_language in Language.objects.all()]
    language = forms.ChoiceField(choices = choices)
    class Meta():
        model=UserAttributes
        fields = ('tech_working','tech_known','tech_willing','language_working','language_known','language_willing', )
        
class UserProfile_DesignationForm(forms.ModelForm):
    class Meta():
        model=Designation
        
        