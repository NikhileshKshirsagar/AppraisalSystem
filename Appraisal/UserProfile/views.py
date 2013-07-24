# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django.template.context import RequestContext
from django.core.context_processors import csrf 
from django.http import HttpResponseRedirect 
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.utils import timezone

from UserProfile.UserProfileForms import UserCreate, userListForm
from Login.models import UserDetails

def CreateUser(request):
    userList = UserDetails.objects.all()
    if request.method == 'POST':
        userCreateform = UserCreate(request.POST)
        print "POST request"
        if userCreateform.is_valid():
            #userCreateform.clean_userType()
            print "Valid form"
            i_UserId = UserDetails.objects.get(user_id=request.session['UserID']).user_id
            userCreateform.save(commit=False, userId = i_UserId)
            userCreateform = UserCreate()
            # redirect to next page
            return render_to_response('Userprofile/CreateUser.html', {'successMsg' : 'User created successfully', 'userCreateform' : userCreateform, 'userList' : userList}, context_instance = RequestContext( request));
        else:
            print "Invalid form"
            return render_to_response('Userprofile/CreateUser.html', { 'userCreateform' : userCreateform ,'userList' : userList}, context_instance = RequestContext( request))
    else:
        userCreateform = UserCreate()
        return render_to_response('Userprofile/CreateUser.html', { 'userCreateform' : userCreateform, 'userList' : userList }, context_instance = RequestContext( request))
    
#def UserProfile(request):
    #if request.method == 'POST':
    
def userSearch(request):
    if request.POST:
        search_text = request.POST.get('search_txt')
    else:
        search_text = ''
        
    obj_searchResult = UserDetails.objects.filter(firstname__contains=search_text)
    return HttpResponse(content='obj_searchResult', mimetype='text/html')
    #return  render_to_response('ajax.html', {'obj_searchResult' : obj_searchResult},context_instance = RequestContext( request))