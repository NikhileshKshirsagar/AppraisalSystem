from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django.template.context import RequestContext
from django.core.context_processors import csrf
from django.utils import timezone
from django.utils import simplejson

from Login.models import Project, Language, Designation, Event, UserDetails
from Masters.MasterForms import Master_DesignationForm,Master_EventForm,Master_LanguageForm,Master_ProjectForm

def MasterInput(request):
        projectForm = Master_ProjectForm()
        designationForm = Master_DesignationForm()
        languageForm = Master_LanguageForm()
        eventForm = Master_EventForm()
        
        obj_ProjectList = Project.objects.all()
        return render_to_response('Masters/InputMaster.html', 
                              { 'projectForm' : projectForm, 'designationForm' : designationForm, 'languageForm' : languageForm, 'eventForm' : eventForm, 'obj_ProjectList' : obj_ProjectList}, 
                              context_instance = RequestContext( request))
        
def ProjectMasterInput(request):
    if request.method == 'POST':
        projectForm = Master_ProjectForm(request.POST)
        i_UserId = UserDetails.objects.get(user_id=request.session['UserID'])
        if projectForm.is_valid():
            projectForm.save(commit=False, userId = i_UserId)
            return render_to_response('Masters/InputMaster.html', {'projectForm' : projectForm, 'userNotification' : 'Project created successfully' }, context_instance = RequestContext( request))
        else:
            return render_to_response('Masters/InputMaster.html', {'projectForm' : projectForm, 'userNotification' : 'Project could not be created' }, context_instance = RequestContext( request))    