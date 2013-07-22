# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session

from forms import QuestionForm
from django.http import HttpResponseRedirect 
from django.core.context_processors import csrf

def questionCreateView(request):
    
    args={}
    args.update(csrf(request))
    args['error']=''
    if request.method == 'POST':
        objQuestionForm = QuestionForm(request.POST)
        if objQuestionForm.is_valid():
                print "Form valid"
        else:
             args['questionCreateform']=objQuestionForm
             return render_to_response('Questions/CreateQuestion.html',args)
    else:
        objQuestionForm = QuestionForm()
        args['questionCreateform']=objQuestionForm
        return render_to_response('Questions/CreateQuestion.html',args)
