'''
Created on 17-Jul-2013

@author: Nikhilesh
'''

from django import forms
from Login.models import UserDetails, UserAttributes, Language, UserAttributes, Designation, Project, Event
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
    username = forms.CharField(label='User name',error_messages={'required': 'Please enter user name.'}, widget=forms.TextInput(attrs={'class':'tableRow span5 search-query'}))
    password = forms.CharField(label='Password', error_messages={'required': 'Please enter the password'}, widget=forms.TextInput(attrs={'class':'tableRow span5 search-query'}))
    user_level = forms.CharField()
    user_weight = forms.CharField()
    type = forms.ChoiceField(label='User type',choices=usertype, widget=forms.Select(attrs={'class':'tableRow span5 search-query', 'style': 'border-radius: 15px 15px 15px 15px;'}))
    action = forms.CharField(required=False, widget=forms.TextInput(attrs={'type':'hidden', 'value' : 'Alpha', 'id' : 'action'}))
    userid = forms.CharField(required=False, widget=forms.TextInput(attrs={ 'type':'hidden' }))
    
    def save(self,  userId,commit=True):
        obj_userForm = super(UserCreate, self).save(commit=False)
        obj_userForm.emailid = self.data['emailid']
        obj_userForm.username = self.data['username']
        obj_userForm.password = self.data['password']
        obj_userForm.user_level = self.data['user_level']
        obj_userForm.user_weight = self.data['user_weight']
        obj_userForm.type = self.data['type']
        obj_userForm.modified_by = userId
        obj_userForm.modified_on = timezone.now()
        obj_userForm.save()
        
    def clean_emailid(self):
        if self.data['action'] == "Alpha":
            print "Alpha"
            s_existingEmail = 0
            try:
                print self.cleaned_data['emailid']
                s_existingEmail = UserDetails.objects.filter(emailid=self.cleaned_data['emailid']).count()
            except UserDetails.DoesNotExist:
                s_existingEmail = 0

            if s_existingEmail > 0:
                raise forms.ValidationError("Email address '" + self.cleaned_data['emailid'] + "' already exists.")
            
        elif self.data['action'] == "Beta":
            s_existingEmail = 0
            try:
                s_existingEmail = UserDetails.objects.filter(emailid=self.cleaned_data['emailid']).exclude(user_id=self.data['userid']).count()
                
            except UserDetails.DoesNotExist:
                s_existingEmail = 1
                print s_existingEmail
           
            if s_existingEmail > 0:
                raise forms.ValidationError("Email address '" + self.cleaned_data['emailid'] + "' already exists.")
                    
        return self.cleaned_data['emailid']
    
    def clean_username(self):
        if self.data['action'] == "Alpha":
            print "Alpha"
            s_existingusername = 0
            try:
                print self.cleaned_data['username']
                s_existingusername = UserDetails.objects.filter(username=self.cleaned_data['username']).count()
            except UserDetails.DoesNotExist:
                s_existingusername = 0

            if s_existingusername > 0:
                raise forms.ValidationError("User name '" + self.cleaned_data['username'] +"' already exists.")
            
        elif self.data['action'] == "Beta":
            s_existingusername = 0
            try:
                s_existingusername = UserDetails.objects.filter(username=self.cleaned_data['username']).exclude(user_id=self.data['userid']).count()
            except UserDetails.DoesNotExist:
                s_existingusername = 1
                print s_existingusername
           
            if s_existingusername > 0:
                raise forms.ValidationError("User name '" + self.cleaned_data['username'] +"' already exists.")
        
        return self.cleaned_data['username']
        
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
        fields = ('firstname','lastname','emailid','user_level', 'user_weight', 'type', 'action', 'userid', 'password')
        
class userListForm(forms.ModelForm):
    class Meta():
        model=UserDetails
        fields = ('firstname','lastname','emailid',)

# User Profile        
class UserProfile_UserDetailForm(forms.ModelForm):
    class Meta():
        model=UserDetails
        fields = ('username','password',)
    
class UserProfile_LanguageForm(forms.ModelForm):
    #newLanguage = forms.CharField(label=("Add new language"), required=False)
    choices = [(obj_language.language_id, obj_language.language) for obj_language in Language.objects.all()]
    language = forms.MultipleChoiceField(choices = choices, label=("Languages"))
    
    class Meta():
        model=Language
        fields = ('language',)
class UserProfile_UserAttributes(forms.ModelForm):
    
    class Meta():
        model=UserAttributes
        fields = ('tech_working','tech_known','tech_willing','language_working','language_known','language_willing', )
        
class UserProfile_DesignationForm(forms.ModelForm):
    choices_desgnation = [(obj_designation.designation_id, obj_designation.designation) for obj_designation in Designation.objects.all()]
    designation = forms.MultipleChoiceField(choices=choices_desgnation, label=("Designation(s)"), required=True)
    class Meta():
        model=Designation
        fields = ('designation',)
                   
class UserProfile_ProjectForm(forms.ModelForm):
    choices_project = [(obj_project.project_id, obj_project.name) for obj_project in Project.objects.all()]
    name = forms.MultipleChoiceField(choices=choices_project, label=("Project(s)"), required=True)
    class Meta():
        model=Project
        fields = ('name',)