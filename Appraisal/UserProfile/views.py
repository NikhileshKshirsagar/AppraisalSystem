# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django.template.context import RequestContext
from django.core.context_processors import csrf 
from django.http import HttpResponseRedirect 
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.utils import timezone
from django.utils import simplejson

from UserProfile.UserProfileForms import UserCreate, userListForm
from Login.models import UserDetails, Designation

def CreateUser(request):
    #userList = UserDetails.objects.all()
        
        if request.method == 'POST':
            
            userCreateform = UserCreate(request.POST)
            print "POST request"
            if userCreateform.is_valid():
                i_UserId = UserDetails.objects.get(user_id=request.session['UserID']).user_id
                # Create user.
                if request.POST.get('action') == 'Alpha': 
                    print "Valid form"
                    userCreateform.save(commit=False, userId = i_UserId)
                    userCreateform = UserCreate()
                    # redirect to next page
                    return render_to_response('Userprofile/CreateUser.html', {'successMsg' : 'User created successfully', 'userCreateform' : userCreateform}, context_instance = RequestContext( request))
                # Update user
                elif request.POST.get('action') == 'Beta' :
                    print request.POST.get('user_id')
                    UserDetails.objects.filter(user_id=request.POST.get('user_id')).update(firstname=request.POST.get('firstname'), lastname=request.POST.get('lastname'), emailid=request.POST.get('emailid'), user_level=request.POST.get('user_level'), user_weight=request.POST.get('user_weight'), type=request.POST.get('type'))
                    userCreateform = UserCreate()
                    return render_to_response('Userprofile/CreateUser.html', {'successMsg' : 'User updated successfully', 'userCreateform' : userCreateform}, context_instance = RequestContext( request))
            else:
                print "Invalid form"
                return render_to_response('Userprofile/CreateUser.html', { 'userCreateform' : userCreateform }, context_instance = RequestContext( request))
        else:
            userCreateform = UserCreate()
            return render_to_response('Userprofile/CreateUser.html', { 'userCreateform' : userCreateform }, context_instance = RequestContext( request))
   
def UserList(request):
    if request.method == 'POST':
        userList = UserDetails.objects.all()
    else:    
        userList = UserDetails.objects.all()
        return render_to_response('Userprofile/UserList.html', { 'userList' : userList }, context_instance = RequestContext( request))
    
def userSearch(request):
    if request.POST:
        search_text = request.POST.get('search_txt')
    else:
        search_text = ''
            
    obj_searchResult = UserDetails.objects.filter(firstname__icontains=search_text).order_by('firstname')
    result = ''
    for user in obj_searchResult:
        result += '<a> <div class="userTile clickable"> <input id="id" type="hidden" value=' + str(user.user_id) + '>' +user.firstname + " " + user.lastname  +'<br> <div>' + user.emailid + ' </div></div></a>'

    return HttpResponse(content=result, content_type='text/html')

def userInfo(request):    
    print "USER INFO"
    if request.is_ajax():
        try:
            search_text = request.POST.get('search_txt')
            obj_searchResult = UserDetails.objects.get(user_id=search_text)
        
            initial = {"error" : '',
                       "firstname": obj_searchResult.firstname,
                        "lastname": obj_searchResult.lastname, 
                        "emailid": obj_searchResult.emailid, 
                        "user_level": obj_searchResult.user_level, 
                        "user_weight": obj_searchResult.user_weight, 
                        "type": obj_searchResult.type,
                        "user_id" : obj_searchResult.user_id}
            
        except:
            initial = {"error" : 'Exception occurred please report this error.'}
        
        data = simplejson.dumps(initial)
        return HttpResponse(content=data, content_type='json')    
        
    else:
        return HttpResponse(content='error occured', content_type='application/json')
    
    
def userProfile(request):
    if request.POST:
        user = UserDetails.objects.get(user_id=request.session['UserID'])
        designation = Designation.objects.filter()
        return render_to_response('Userprofile/CreateUser.html', {}, context_instance = RequestContext( request))