# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django.template.context import RequestContext
from django.core.context_processors import csrf 
from django.http import HttpResponseRedirect 
from django.core.context_processors import csrf
from django.utils import timezone

from UserProfile.UserProfileForms import UserCreate
from Login.models import UserDetails

def CreateUser(request):
    if request.method == 'POST':
        userCreateform = UserCreate(request.POST)
        print "POST request"
        try:
            s_existingEmail = UserDetails.objects.get(emailid=request.POST['emailid']).emailid
        except UserDetails.DoesNotExist:
           s_existingEmail = ''
               
        if s_existingEmail != '' and s_existingEmail ==  request.POST['emailid']:     
                print "in else"
                return render_to_response('Userprofile/CreateUser.html', {'errorEmail' : 'Email id already exists', 'userCreateform' : userCreateform});
        else:    
            if userCreateform.is_valid():
                #userCreateform.clean_userType()
                print "Form valid"
                i_UserId = UserDetails.objects.get(user_id=request.session['UserID']).user_id
                userCreateform.save(commit=False, userId = i_UserId)
                print "SESSION - USER ID : "
                print request.session['UserID']
                
                # redirect to next page
                return render_to_response('Welcome.html', {'successMsg' : 'User created successfully', 'userCreateform' : userCreateform});
            else:
                #userCreateform.clean_type()
                print UserDetails.objects.get(user_id=request.session['UserID']).firstname
                print "Invalid form"
                return render_to_response('Userprofile/CreateUser.html', { 'userCreateform' : userCreateform }, context_instance = RequestContext( request))
    else:
        userCreateform = UserCreate()
        return render_to_response('Userprofile/CreateUser.html', { 'userCreateform' : userCreateform }, context_instance = RequestContext( request))
    
#def UserProfile(request):
    #if request.method == 'POST':
        
     