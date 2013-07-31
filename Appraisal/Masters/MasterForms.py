from django import forms
from Login.models import Language, Designation, Project, Event
from django.utils import timezone

# Input Master  
        
class Master_ProjectForm(forms.ModelForm):
    cProject_status = (
                       ('PL' , 'Planing'),
                       ('OG' , 'Ongoing'),
                       ('FN', 'Finished'),
                       )
    
    name = forms.CharField(label='Project name', error_messages={'required': 'Please enter user first name.'})
    description = forms.CharField(label='Project description')
    start_date = forms.CharField(label='Project start date')
    end_date = forms.CharField(label='Project end date')
    status = forms.ChoiceField(label='Project status',choices=cProject_status)
    contact_person = forms.CharField(label='Contact person')
    
    class Meta():
        model=Project
    fields = ('name','description', 'start_date', 'end_date', 'status', 'contact_person',)

class Master_DesignationForm(forms.ModelForm):
    class Meta():
        model=Designation          
    fields = ('designation',)
             
class Master_LanguageForm(forms.ModelForm):
    class Meta():
        model=Language
    fields = ('language', 'description',)
             
class Master_EventForm(forms.ModelForm):
    class Meta():
        model=Event
    fields = ('description', 'event_date',)  