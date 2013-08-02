# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session

from forms import QuestionForm, OptionFrom
from django.http import HttpResponseRedirect 
from django.core.context_processors import csrf

from Login.models import UserDetails
def questionCreateView(request):
    
    args={}
    args.update(csrf(request))
    args['error']=''
    objQuestionForm = QuestionForm(request.POST or None)
    objOptionForm = OptionFrom(request.POST or None)
    if request.method == 'POST':
        if request.POST['type'] == '2':
            if objQuestionForm.is_valid() and objOptionForm.is_valid():
                flag=True
            else:
                flag=False
        else:
            objOptionForm = OptionFrom()
            if objQuestionForm.is_valid():
                flag=True   
            else:
                flag=False
             
        if flag == True: 
           i_UserId = UserDetails.objects.get(user_id=request.session['UserID'])
           objOptionForm.save(commit=False, userId=i_UserId)
           objQuestionForm.save(commit=False, userId = i_UserId)
           args['successMsg']="Question created successfully"
           objOptionForm = OptionFrom()
           objQuestionForm = QuestionForm()
           args['questionCreateform']=objQuestionForm
           args['optionCreateform']=objOptionForm
           return render_to_response('Questions/CreateQuestion.html',args)
        else:
           args['questionCreateform']=objQuestionForm
           args['optionCreateform']=objOptionForm
           return render_to_response('Questions/CreateQuestion.html',args)
    else:
        args['questionCreateform']=objQuestionForm
        args['optionCreateform']=objOptionForm
        return render_to_response('Questions/CreateQuestion.html',args)
