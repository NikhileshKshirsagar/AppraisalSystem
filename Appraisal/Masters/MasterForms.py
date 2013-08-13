from django import forms
from Login.models import Language, Designation, Project, Event, UserDetails
from django.utils import timezone, formats
from datetime import datetime  
    
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
    start_date = forms.DateField(label='Project start date', error_messages={'required': 'Please enter project start date.'}, widget=forms.DateInput(format=format ,attrs={'class':'tableRow span3 ', 'placeholder' : 'Click here to add start date'}))
    end_date = forms.DateField(label='Project end date', required=False , widget=forms.DateInput(attrs={'class':'tableRow span3 ', 'placeholder' : 'Click here to add end date'}))
    #start_date = forms.DateField(label='Project start date')
    #end_date = forms.DateField(label='Project end date', required=False)
    status = forms.ChoiceField(label='Project status',choices=cProject_status, widget=forms.Select(attrs={'class':'tableRow span5 '}))
    contact_person = forms.ChoiceField(label='Contact person', choices=choices_contactPerson, widget=forms.Select(attrs={'class':'tableRow span5 '}))
    action = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden', 'value' : 'Alpha', 'id' : 'action'}))
    projectid = forms.CharField(required=False, widget=forms.TextInput(attrs={ 'type':'hidden' }))
     
    def save(self,  userId,commit=True):
        obj_projectForm = super(Master_ProjectForm, self).save(commit=False)
        obj_projectForm.name = self.data['name']
        obj_projectForm.description = self.data['description']
        obj_projectForm.start_date = datetime.strptime(self.data['start_date'], '%Y-%m-%d').date()
        if(self.data['end_date'] != ''):
            print "Inside if"
            obj_projectForm.end_date = datetime.strptime( self.data['end_date'], '%Y-%m-%d')
        obj_projectForm.status = self.data['status']
        obj_ContactPerson = UserDetails.objects.get(user_id = self.data['contact_person'])
        obj_projectForm.contact_person = obj_ContactPerson
        obj_projectForm.modified_by = userId
        obj_projectForm.modified_on = timezone.now()
        obj_projectForm.save()
        
    def clean_name(self):
        s_project = 0  
        if self.data['action'] == "Alpha":  
            try:
                print self.cleaned_data['name']
                s_project = Project.objects.filter(name = self.cleaned_data['name']).count()
            except:
                print "Except.........."
                s_project = 0
                
            if s_project > 0:
                raise forms.ValidationError("Project '" + self.cleaned_data['name'] + "' already exists.")
        
        elif self.data['action'] == "Beta":
            try:
                print "Try ........" + self.cleaned_data['name']
                print "Project id" + self.data['projectid']
                s_project = Project.objects.filter(name = self.cleaned_data['name']).exclude(project_id=self.data['projectid']).count()
            except:
                print "Except..........."
                s_project = 0
                print "Project Count............."  
                print s_project
            if s_project > 0:
                raise forms.ValidationError("Project '" + self.cleaned_data['name'] + "' already exists.")

        return self.cleaned_data['name']
    
    def clean_start_date(self):
        print "Start date : ................................................."
        print self.cleaned_data['start_date']
        if self.cleaned_data['start_date'] == '' :
            raise forms.ValidationError("Please set the project start date.")
        return self.cleaned_data['start_date']
    
    def clean_status(self):
        if self.cleaned_data['status'] == 'Select' :
            raise forms.ValidationError("Please select the project status.")
        return self.cleaned_data['status']
    
    def clean_contact_person(self):
        if self.cleaned_data['contact_person'] == '' :
            raise forms.ValidationError("Please select the project contact person.")
        return UserDetails.objects.get(user_id = self.data['contact_person'])
    
    class Meta():
        model=Project
        fields = ('name','description', 'start_date', 'end_date', 'status', 'contact_person', 'projectid',)

class Master_DesignationForm(forms.ModelForm):
    designation = forms.CharField(label='Designation', error_messages={'required': 'Please enter Designation.'}, widget=forms.TextInput(attrs={'class':'tableRow span5 '}))
    
    def save(self,  userId,commit=True):
        obj_DesignationForm = super(Master_DesignationForm, self).save(commit=False)
        obj_DesignationForm.designation = self.data['designation']
        obj_DesignationForm.modified_by = userId
        obj_DesignationForm.modified_on = timezone.now()
        obj_DesignationForm.save()
        
    def clean_designation(self):
        try: 
            s_desg = Designation.objects.get(designation=self.cleaned_data['designation']).designation
        except:
            s_desg = ''
        if self.cleaned_data['designation'] != '' and self.cleaned_data['designation'] == s_desg :   
            raise forms.ValidationError("Designation '" + self.cleaned_data['designation'] + "' already exists.")    
        return self.cleaned_data['designation']
        
    class Meta():
        model=Designation          
        fields = ('designation',)
             
class Master_LanguageForm(forms.ModelForm):
    language = forms.CharField(label='Language name', error_messages={'required': 'Please enter language.'}, widget=forms.TextInput(attrs={'class':'tableRow span5 '}))
    description = forms.CharField(label='Language description', required=False, widget=forms.Textarea(attrs={'class':'tableRow TextArea '}))
    
    def save(self, userId, commit=True):
        obj_LanguageForm = super(Master_LanguageForm, self).save(commit=False)
        obj_LanguageForm.language = self.data['language']
        obj_LanguageForm.description = self.data['description']
        obj_LanguageForm.modified_by = userId
        obj_LanguageForm.modified_on = timezone.now()
        obj_LanguageForm.save()
    
    def clean_language(self):
        try:
            s_language = Language.objects.get(language=self.cleaned_data['language']).language
        except:
            print "Exception"
            s_language = 'empty'
        if self.cleaned_data['language'] != 'empty' and self.cleaned_data['language'] == s_language :   
            raise forms.ValidationError("Language '" + self.cleaned_data['language'] + "' already exists.")    
        return self.cleaned_data['language']
    
    class Meta():
        model=Language
        fields = ('language', 'description',)
             
class Master_EventForm(forms.ModelForm):
    description = forms.CharField(label='Event description', error_messages={'required': 'Please enter event description.'}, widget=forms.Textarea(attrs={'class':'tableRow TextArea '}))
    event_date = forms.DateField(label='Event date', widget=forms.DateInput(attrs={'class':'tableRow span3 '}))
    
    def save(self, userId, commit=True):
        obj_EventForm = super(Master_EventForm, self).save(commit=False)
        obj_EventForm.event_date = self.data['event_date']
        obj_EventForm.description = self.data['description']
        obj_EventForm.modified_by = userId
        obj_EventForm.modified_on = timezone.now()
        obj_EventForm.save()
    
    class Meta():
        model=Event
        fields = ('description', 'event_date',)  