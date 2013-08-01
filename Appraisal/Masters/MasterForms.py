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
    
    name = forms.CharField(label='Project name', error_messages={'required': 'Please enter user first name.'}, widget=forms.TextInput(attrs={'class':'tableRow span5 '}))
    description = forms.CharField(label='Project description', widget=forms.Textarea(attrs={'class':'tableRow TextArea'}))
    start_date = forms.CharField(label='Project start date', widget=forms.TextInput(attrs={'class':'tableRow span3 ', 'placeholder' : 'Click here to insert date'}))
    end_date = forms.CharField(label='Project end date', widget=forms.TextInput(attrs={'class':'tableRow span3 ', 'placeholder' : 'Click here to insert date'}))
    status = forms.ChoiceField(label='Project status',choices=cProject_status, widget=forms.Select(attrs={'class':'tableRow span5 '}))
    contact_person = forms.CharField(label='Contact person', widget=forms.TextInput(attrs={'class':'tableRow span5 '}))
    
    class Meta():
        model=Project
        fields = ('name','description', 'start_date', 'end_date', 'status', 'contact_person',)

class Master_DesignationForm(forms.ModelForm):
    designation = forms.CharField(label='Designation', error_messages={'required': 'Please enter Designation.'}, widget=forms.TextInput(attrs={'class':'tableRow span5 '}))
    class Meta():
        model=Designation          
        fields = ('designation',)
             
class Master_LanguageForm(forms.ModelForm):
    language = forms.CharField(label='Language name', error_messages={'required': 'Please enter language.'}, widget=forms.TextInput(attrs={'class':'tableRow span5 '}))
    description = forms.CharField(label='Language description', widget=forms.Textarea(attrs={'class':'tableRow TextArea '}))
    class Meta():
        model=Language
        fields = ('language', 'description',)
             
class Master_EventForm(forms.ModelForm):
    description = forms.CharField(label='Event description', error_messages={'required': 'Please enter event description.'}, widget=forms.Textarea(attrs={'class':'tableRow TextArea '}))
    event_date = forms.CharField(label='Event date', widget=forms.TextInput(attrs={'class':'tableRow span3 '}))
    class Meta():
        model=Event
        fields = ('description', 'event_date',)  