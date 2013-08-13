from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django.template.context import RequestContext
from django.core.context_processors import csrf
from django.utils import timezone
from django.utils import simplejson
from datetime import datetime

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
            if request.POST.get('action') == 'Alpha':
                projectForm.save(commit=False, userId = i_UserId)
                return render_to_response('Masters/Project.html', {'obj_ProjectList' : obj_ProjectList, 'projectForm' : projectForm, 'userNotification' : 'Project created successfully' }, context_instance = RequestContext( request))
            elif request.POST.get('action') == 'Beta' :
                Project.objects.filter(project_id=request.POST.get('project_id')).update(name=request.POST.get('name'), description=request.POST.get('description'), 
                                                                                         start_date= datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date(), 
                                                                                         end_date=datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').date(), 
                                                                                         status=request.POST.get('status'), contact_person=request.POST.get('contact_person'))
                return render_to_response('Masters/Project.html', {'obj_ProjectList' : obj_ProjectList, 'projectForm' : projectForm, 
                                                                   'userNotification' : 'Project information updated successfully' }, context_instance = RequestContext( request))
        else:
            print "Form Invalid"
            return render_to_response('Masters/Project.html', {'obj_ProjectList' : obj_ProjectList, 'projectForm' : projectForm, 
                                                               'userNotification' : 'Project could not be created' }, context_instance = RequestContext( request))
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

def projectInfo(request):
    if request.POST:
        search_text = request.POST.get('search_txt')
        
        obj_searchResult = Project.objects.get(project_id=search_text)
        
        if obj_searchResult.start_date != None :
            startDate = str(datetime.strptime(str(obj_searchResult.start_date), '%Y-%m-%d').date())
            print "Start Date : " + startDate
        else:
            startDate = ''
       
        if obj_searchResult.end_date != None :
            endDate = str(datetime.strptime(str(obj_searchResult.end_date), '%Y-%m-%d').date()) 
        else: 
            endDate = ''
     
        initial = {     
                   'projectid': obj_searchResult.project_id,
                    'name': obj_searchResult.name, 
                    'description': obj_searchResult.description, 
                    'start_date': startDate,
                    'end_date': endDate, 
                    'status': obj_searchResult.status,
                    'contact_person' : obj_searchResult.contact_person.user_id
                    }
        print obj_searchResult.contact_person
        projectForm = Master_ProjectForm(initial)
        obj_ProjectList = Project.objects.all()
        return render_to_response('Masters/ProjectInfo.html', 
                              { 'obj_ProjectList' : obj_ProjectList, 'projectForm' : projectForm }, 
                              context_instance = RequestContext( request))
        