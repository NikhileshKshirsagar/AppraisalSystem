from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django.template.context import RequestContext
from django.core.context_processors import csrf
from django.utils import timezone
from django.utils import simplejson

from Login.models import Project, Language, Designation, Event, UserDetails
from Masters.MasterForms import Master_DesignationForm,Master_EventForm,Master_LanguageForm,Master_ProjectForm

def MasterInput(request):
        return render_to_response('Masters/InputMaster.html', context_instance = RequestContext( request))
        
def ProjectMasterInput(request):
    obj_ProjectList = Project.objects.all()
    if request.method == 'POST':
        projectForm = Master_ProjectForm(request.POST)
        i_UserId = UserDetails.objects.get(user_id=request.session['UserID'])
        if projectForm.is_valid():
            print "Form Valid"
            projectForm.save(commit=False, userId = i_UserId)
            return render_to_response('Masters/Project.html', {'obj_ProjectList' : obj_ProjectList, 'projectForm' : projectForm, 'userNotification' : 'Project created successfully' }, context_instance = RequestContext( request))
        else:
            print "Form Invalid"
            return render_to_response('Masters/Project.html', {'obj_ProjectList' : obj_ProjectList, 'projectForm' : projectForm, 'userNotification' : 'Project could not be created' }, context_instance = RequestContext( request))
    else:
        print "not post"
        projectForm = Master_ProjectForm()
        return render_to_response('Masters/Project.html', 
                              { 'obj_ProjectList' : obj_ProjectList, 'projectForm' : projectForm }, 
                              context_instance = RequestContext( request))
        
def DesignationMasterInput(request):
    obj_DesignationList = Designation.objects.all()
    if request.method == 'POST':
        designationForm = Master_DesignationForm(request.POST)
        i_UserId = UserDetails.objects.get(user_id=request.session['UserID'])
        if designationForm.is_valid():
            print "Form valid"
            designationForm.save(commit=False, userId = i_UserId)
            return render_to_response('Masters/Designation.html', { 'obj_DesignationList' : obj_DesignationList, 'userNotification' : 'Designation added successfully', 'designationForm' : designationForm }, 
                                      context_instance = RequestContext( request))
        else:
            return render_to_response('Masters/Designation.html', { 'obj_DesignationList' : obj_DesignationList, 'userNotification' : 'Designation could not be added', 'designationForm' : designationForm }, 
                                      context_instance = RequestContext( request))
    else:
        designationForm = Master_DesignationForm()
        return render_to_response('Masters/Designation.html', 
                              { 'obj_DesignationList' : obj_DesignationList, 'designationForm' : designationForm }, 
                              context_instance = RequestContext( request))

def LanguageMasterInput(request):
    obj_LanguageList = Language.objects.all()
    if request.method == 'POST':
        languageForm = Master_LanguageForm(request.POST)
        i_UserId = UserDetails.objects.get(user_id=request.session['UserID'])
        if languageForm.is_valid():
            languageForm.save(commit=False, userId = i_UserId)
            return render_to_response('Masters/Language.html', { 'obj_LanguageList' : obj_LanguageList, 'userNotification' : 'Language added successfully', 'languageForm' : languageForm }, 
                                      context_instance = RequestContext( request))
        else:
            return render_to_response('Masters/Language.html', { 'obj_LanguageList' : obj_LanguageList, 'userNotification' : 'Language could not be added', 'languageForm' : languageForm }, 
                                      context_instance = RequestContext( request))

    else:
        languageForm = Master_LanguageForm()
        return render_to_response('Masters/Language.html', 
                              { 'obj_LanguageList' : obj_LanguageList, 'languageForm' : languageForm }, 
                              context_instance = RequestContext( request))

def EventMasterInput(request):
    obj_EventList = Event.objects.all()
    if request.method == 'POST':
        eventForm = Master_EventForm(request.POST)
        i_UserId = UserDetails.objects.get(user_id=request.session['UserID'])
        if eventForm.is_valid():
            eventForm.save(commit=False, userId = i_UserId)
            return render_to_response('Masters/Event.html', { 'obj_EventList' : obj_EventList, 'userNotification' : 'Event added successfully', 'eventForm' : eventForm }, 
                                      context_instance = RequestContext( request))
        else:
            return render_to_response( 'Masters/Event.html', { 'obj_EventList' : obj_EventList, 'userNotification' : 'Event could not be added', 'eventForm' : eventForm }, 
                                      context_instance = RequestContext( request))

    else:
        eventForm = Master_EventForm()
        return render_to_response('Masters/Event.html', 
                              { 'obj_EventList' : obj_EventList, 'eventForm' : eventForm }, 
                              context_instance = RequestContext( request))