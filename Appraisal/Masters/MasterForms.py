from django import forms
from Login.models import Language, Designation, Project, Event, UserDetails
from django.utils import timezone

# Input Master  
        
class Master_ProjectForm(forms.ModelForm):
    cProject_status = (
                       ('Select' , 'Select project status'),
                       ('Planing' , 'Planing'),
                       ('Ongoing' , 'Ongoing'),
                       ('Finished', 'Finished'),
                       )
    choices_contactPerson = [(obj_users.user_id, obj_users.firstname) for obj_users in UserDetails.objects.all()]
    name = forms.CharField(label='Project name', error_messages={'required': 'Please enter project name.'}, widget=forms.TextInput(attrs={'class':'tableRow span5 '}))
    description = forms.CharField(label='Project description', required=False, widget=forms.Textarea(attrs={'class':'tableRow TextArea'}))
    start_date = forms.CharField(label='Project start date', widget=forms.DateInput(format=format ,attrs={'class':'tableRow span3 ', 'placeholder' : 'Click here to insert date'}))
    end_date = forms.CharField(label='Project end date', required=False , widget=forms.TextInput(attrs={'class':'tableRow span3 ', 'placeholder' : 'Click here to insert date'}))
    status = forms.ChoiceField(label='Project status',choices=cProject_status, widget=forms.Select(attrs={'class':'tableRow span5 '}))
    contact_person = forms.ChoiceField(label='Contact person', choices=choices_contactPerson, widget=forms.Select(attrs={'class':'tableRow span5 '}))
    
    def save(self,  userId,commit=True):
        obj_projectForm = super(Master_ProjectForm, self).save(commit=False)
        obj_projectForm.name = self.data['name']
        obj_projectForm.description = self.data['description']
        print self.data['start_date']
        obj_projectForm.start_date = self.data['start_date']
        obj_projectForm.end_date = self.data['end_date']
        obj_projectForm.status = self.data['status']
        obj_projectForm.contact_person = self.data['contact_person']
        obj_projectForm.modified_by = userId
        obj_projectForm.modified_on = timezone.now()
        obj_projectForm.save()
        
    def clean_name(self):    
        try:
            print self.cleaned_data['name']
            s_project = Project.objects.get(name = self.cleaned_data['name']).name
        except:
            s_project = ''
            
        if s_project != '' and s_project == self.cleaned_data['name']:
            raise forms.ValidationError("Project '" + self.cleaned_data['name'] + "' already exists.")
        
        return self.cleaned_data['name']
    
    def clean_start_date(self):
        print "Start date : "
        print self.cleaned_data['start_date']
        if self.cleaned_data['start_date'] == '' :
            raise forms.ValidationError("Please set the project start date.")
        return self.cleaned_data['start_date']
    
    def clean_status(self):
        print "Status : "
        print self.cleaned_data['status']
        if self.cleaned_data['status'] == 'Select' :
            raise forms.ValidationError("Please select the project status.")
        return self.cleaned_data['status']
    
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