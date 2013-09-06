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

from UserProfile.UserProfileForms import UserCreate, userListForm, UserProfile_UserDetailForm, UserProfile_LanguageForm, UserProfile_DesignationForm, UserProfile_ProjectForm
from Login.models import UserDetails, Designation, Project, Language, Technology,Appraisment,AppraisalContent

#from Login.models import Appraisment,AppraisalContent

def CreateUser(request):
    if request.method == 'POST':
        print request.POST
        userCreateform = UserCreate(request.POST)
        if userCreateform.is_valid():
            i_UserId = UserDetails.objects.get(user_id=request.session['UserID']).user_id
            # Create user.
            if request.POST.get('action') == 'Alpha': 
                print "Valid form"
                userCreateform.save(commit=False, userId = i_UserId)
                userCreateform = UserCreate()
                # redirect to next page
                return render_to_response('Userprofile/CreateUser.html', {'successMsg' : 'User created successfully', 'btn' : 'Create','userCreateform' : userCreateform}, context_instance = RequestContext( request))
            # Update user
            elif request.POST.get('action') == 'Beta' :
                try:
                    UserDetails.objects.filter(user_id=request.POST.get('userid')).update(firstname=request.POST.get('firstname'), lastname=request.POST.get('lastname'), emailid=request.POST.get('emailid'), username=request.POST.get('username'), password=request.POST.get('password'), user_level=request.POST.get('user_level'), user_weight=request.POST.get('user_weight'), type=request.POST.get('type'))
                    userCreateform = UserCreate()
                    return render_to_response('Userprofile/CreateUser.html', {'successMsg' : 'User updated successfully', 'btn' : 'Create','userCreateform' : userCreateform}, context_instance = RequestContext( request))
                except:
                    userCreateform = UserCreate()
                    return render_to_response('Userprofile/CreateUser.html', {'successMsg' : 'User cannot be updated', 'btn' : 'Update','userCreateform' : userCreateform}, context_instance = RequestContext( request))
        else:
            print "Invalid form"
            if request.POST.get('action') == 'Alpha':
                return render_to_response('Userprofile/CreateUser.html', { 'userCreateform' : userCreateform, 'btn' : 'Create' }, context_instance = RequestContext( request))
            else:
                return render_to_response('Userprofile/CreateUser.html', { 'btn' : 'Update','userCreateform' : userCreateform}, context_instance = RequestContext( request))
    else:
        userCreateform = UserCreate()
        return render_to_response('Userprofile/CreateUser.html', { 'userCreateform' : userCreateform, 'btn' : 'Create' }, context_instance = RequestContext( request))

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
    if request.is_ajax():
        try:
            search_text = request.POST.get('search_txt')
            obj_searchResult = UserDetails.objects.get(user_id=search_text)
        
            initial = {"error" : '',
                       "firstname": obj_searchResult.firstname,
                        "lastname": obj_searchResult.lastname, 
                        "emailid": obj_searchResult.emailid,
                        "username":  obj_searchResult.username,
                        "password":  obj_searchResult.password,
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
        print request.POST
        #user = UserDetails.objects.get(user_id=request.session['UserID'])
        #designation = Designation.objects.filter()
        return render_to_response('Userprofile/CreateUser.html', {}, context_instance = RequestContext( request))
    else:
        UserDetailForm = UserProfile_UserDetailForm()
        LanguageForm = UserProfile_LanguageForm()
        DesignationForm = UserProfile_DesignationForm() 
        ProjectForm = UserProfile_ProjectForm()
        
        projectList = Project.objects.all()
        languageList = Language.objects.all()
        designationList = Designation.objects.all()
        technologyList = Technology.objects.all()
        
        return render_to_response('Userprofile/UserProfile.html', { 'UserDetailForm' : UserDetailForm, 'LanguageForm' : LanguageForm, 'DesignationForm' : DesignationForm, 
                                                                   'ProjectForm' : ProjectForm, 'projectList' : projectList, 'languageList' : languageList, 
                                                                   'designationList' : designationList, 'technologyList' : technologyList }, 
                                 context_instance = RequestContext( request))
        
def userWelcome(request):
    args={}
    args.update(csrf(request))
    objappraisment = Appraisment.objects.filter(appraiser=request.session['UserID'])#.exclude(appraisee=request.session['UserID'])
    appraisment_list = []
    for appraisment in objappraisment:
        appraismentlist = {}
        answeredcount=0
        totalcount=0
        status=''
        scolor=''
        appraismentlist['appraisee'] = appraisment.appraisee.user_id
        appraismentlist['appraiser'] = appraisment.appraiser.user_id
        appraismentlist['firstname'] = appraisment.appraisee.firstname
        appraismentlist['lastname'] = appraisment.appraisee.lastname
        totalcount = appraisment.appraisalcontent_set.count()
        appraismentlist['totalcount'] = totalcount
        Questions = AppraisalContent.objects.filter(appresment=appraisment).exclude(answer__isnull=True)
        
        for question in Questions:
            print "-------------------------------------------------------------------"
            print "Appraisment : " +  str(question.appresment.appraisee.firstname)
            print "Question order: " + str(question.question_order)
            print "Question type: "  + str(question.question.type) 
            print "Answer : " + str(question.answer.answer)
            if (question.question.type == 'Scale' and question.answer.answer != '0') or (question.question.type == 'Subjective' and question.answer.answer != '') or question.question.type == 'MCQ':
                answeredcount += 1
            print "Final Answer count" + str(answeredcount)
            
        appraismentlist['answeredcount'] = answeredcount
        appraismentlist['status'] = appraisment.status
        if appraisment.status=='Initial':
            status='Start appraising'
            scolor='#999333'
        else:
            print "ANSWER COUNTS........."
            print answeredcount
            print totalcount
            if appraisment.status=='Created':
                if answeredcount == totalcount:
                    status="Done appraising"
                    scolor='#cfeeb1'
                else: 
                    status='In progress'
                    scolor='#eed79f'
            elif appraisment.status=='Completed':
                status='Submitted'
                scolor='background: rgb(211,229,171); background: -moz-linear-gradient(top, rgba(211,229,171,1) 0%, rgba(78,179,73,1) 97%); /* FF3.6+ */ background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,rgba(211,229,171,1)), color-stop(97%,rgba(78,179,73,1))); /* Chrome,Safari4+ */background: -webkit-linear-gradient(top, rgba(211,229,171,1) 0%,rgba(78,179,73,1) 97%); /* Chrome10+,Safari5.1+ */background: -o-linear-gradient(top, rgba(211,229,171,1) 0%,rgba(78,179,73,1) 97%); /* Opera 11.10+ */background: -ms-linear-gradient(top, rgba(211,229,171,1) 0%,rgba(78,179,73,1) 97%); /* IE10+ */background: linear-gradient(to bottom, rgba(211,229,171,1) 0%,rgba(78,179,73,1) 97%); /* W3C */filter: progid:DXImageTransform.Microsoft.gradient( startColorstr=\'#d3e5ab\', endColorstr=\'#4eb349\',GradientType=0 ); /* IE6-9 */'      
        appraismentlist['statustext'] = status   
        appraismentlist['color'] = scolor
        appraisment_list.append(appraismentlist)
     
    args['UserID']=  request.session['UserID']
    args['username']=request.session['UserName']
    args['appraismentList']=appraisment_list
    return render_to_response('UserProfile/userWelcome.html',args)

def submitAppraisal(request):
    if request.method == 'POST' :
        answeredcount=0
        try:
            appraisee = request.POST.get('search_txt')
            print appraisee
            i_appraismentId = Appraisment.objects.get(appraiser=request.session['UserID'],appraisee=appraisee).appraisment_id
            print "i_appraismentId : "  + str(i_appraismentId)
            Questions = AppraisalContent.objects.filter(appresment=i_appraismentId).exclude(answer__isnull=True)
            
            for question in Questions:
                print "-------------------------------------------------------------------"
                print "Appraisment : " +  str(question.appresment.appraisee.firstname)
                print "Question order: " + str(question.question_order)
                print "Question type: "  + str(question.question.type) 
                print "Answer : " + str(question.answer.answer)
                if (question.question.type == 'Scale' and question.answer.answer != '0') or (question.question.type == 'Subjective' and question.answer.answer != '') or question.question.type == 'MCQ':
                    answeredcount += 1
                print "Final Answer count" + str(answeredcount)
            
            i_totalQuestionCount = AppraisalContent.objects.filter(appresment=i_appraismentId).count()
            print "Total count : " + str(i_totalQuestionCount)
            print "Answered question count : " + str(answeredcount)
            if int(i_totalQuestionCount) == int(answeredcount) :
                Appraisment.objects.filter(appraisment_id = i_appraismentId).update(status = 'Completed')
                return HttpResponse(content='Status updated', content_type='application/json')
            else:
                return HttpResponse(content='First answer all the questions', content_type='application/json')    
        except:
            return HttpResponse(content='Cannot update status.', content_type='application/json')
        print i_appraismentId
