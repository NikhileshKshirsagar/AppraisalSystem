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
        if UserDetails.objects.get(emailid=request.POST['emailid']).emailid ==  request.POST['emailid']:     
                print "in else"
                return render_to_response('Userprofile/CreateUser.html', {'errorEmail' : 'Email id already exists', 'userCreateform' : userCreateform});
        else:    
            if userCreateform.is_valid():
                print "Form valid"
                obj_user = userCreateform.save(commit=False)
                print "SESSION - USER ID : "
                print request.session['UserID']
                obj_user.emailid = request.POST['emailid']
                obj_user.user_level = request.POST['user_level']
                obj_user.user_weight = request.POST['user_weight']
                obj_user.type = request.POST['type']
                obj_user.modified_by = UserDetails.objects.get(user_id=request.session['UserID']).user_id
                obj_user.modified_on = timezone.now()
                obj_user.save()
                return render_to_response('Userprofile/CreateUser.html', {'successMsg' : 'User created successfully', 'userCreateform' : userCreateform});
            else:
                print UserDetails.objects.get(user_id=request.session['UserID']).firstname
                print "Invalid form"
                return render_to_response('Userprofile/CreateUser.html', { 'userCreateform' : userCreateform }, context_instance = RequestContext( request))
    else:
        userCreateform = UserCreate()
        return render_to_response('Userprofile/CreateUser.html', { 'userCreateform' : userCreateform }, context_instance = RequestContext( request))