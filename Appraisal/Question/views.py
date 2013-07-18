# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session

from forms import QuestionForm
from django.http import HttpResponseRedirect 
from django.core.context_processors import csrf

def questionCreateView(request):
    objQuestionForm = QuestionForm()
    args={}
    args.update(csrf(request))
    args['error']=''
    args['form']=objQuestionForm
    return render_to_response('Questions/question.html',args)
