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
    #userList = UserDetails.objects.all()

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
                return render_to_response('Userprofile/CreateUser.html', {'successMsg' : 'User created successfully', 'userCreateform' : userCreateform}, context_instance = RequestContext( request));
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
            
#def UserProfile(request):
    #if request.method == 'POST':
    
def userSearch(request):
    if request.POST:
        search_text = request.POST.get('search_txt')
    else:
        search_text = ''
            
    obj_searchResult = UserDetails.objects.filter(firstname__contains=search_text)
    result = ''
    for user in obj_searchResult:
        result += '<a href="" > <div class="userTile clickable"> <input id="id" type="hidden" value=' + str(user.user_id) + '>' +user.firstname + " " + user.lastname  +'<br> <div>' + user.emailid + ' </div></div></a>'

    return HttpResponse(content=result, content_type='text/html')

def userInfo(request):    
    print "USER INFO"
    if request.is_ajax():
        print "AJAX Request"
        string_search_text = request.POST.get('search_txt')
        print string_search_text
        search_text = int(string_search_text)
        print search_text 
        obj_searchResult = UserDetails.objects.get(user_id=search_text)
        print obj_searchResult.firstname 
        #initial_data =[{('firstname' : obj_searchResult.firstname),('lastname' : obj_searchResult.lastname), ('emailid' : obj_searchResult.emailid), ('user_level' : obj_searchResult.user_level), ('user_weight' : obj_searchResult.user_weight), ('type' : obj_searchResult.type)}]
        #userCreateform = UserCreate(initial={'firstname' : obj_searchResult.firstname}) 
        userList = UserDetails.objects.all()        
        return render_to_response('Userprofile/CreateUser.html', { 'userCreateform' : userList  }, context_instance = RequestContext( request))
    else:
        return HttpResponse(content='error occured', content_type='text/html')