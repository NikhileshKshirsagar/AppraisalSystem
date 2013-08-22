# Create your views here.
from django.shortcuts import render_to_response
from Login.models import UserDetails, Designation, Project, Language, Technology,Appraisment,AppraisalContent,Option
from django.contrib.sessions.models import Session
from django.template.context import RequestContext
from django.core.context_processors import csrf 
from django.http import HttpResponseRedirect 
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.utils import timezone
from django.utils import simplejson


def GenerateReports(request):
    args={}
    args.update(csrf(request))
    nUserID = request.session['UserID']
    objAppUser = Appraisment.objects.get(appraisee=nUserID,appraiser=nUserID)
    objAppOthers=None
    try:
        objAppOthers = Appraisment.objects.filter(appraiser=nUserID).exclude(appraisee=nUserID)
    except:
        objAppOthers=None
    appraisment_list = []
    objQuestionUser = AppraisalContent.objects.filter(appresment=objAppUser.appraisment_id)
    for questionUser in objQuestionUser:
        appraisment = {}
        appraisment['header']=questionUser.question.info
        appraisment['question']=questionUser.question.question
        if questionUser.answer!=None:
            if questionUser.question.type == 'Scale':
                appraisment['answerYourself']=questionUser.answer.answer
            else:
                appraisment['answerYourself']=Option.objects.get(option_id=questionUser.answer.answer).option_text
                                
        answerOther=''
        if objAppOthers!=None:
            for questionOther in objAppOthers:
                try:
                    objappContent = AppraisalContent.objects.get(appresment=questionOther.appraisment_id,question=questionUser.question)
                except:
                    objappContent=None
                if objappContent!=None:
                    if objappContent.answer!=None:
                        print '---------'
                        if objappContent.question.type == 'Scale':
                            sAnswer=sAnswer+objappContent.answer.answer
                        else:
                            sAnswer=Option.objects.get(option_id=objappContent.answer.answer).option_text
                        answerOther=sAnswer
        appraisment['answerOther']=answerOther
        appraisment_list.append(appraisment)
    
    args['UserID']=  request.session['UserID']
    args['username']=request.session['UserName']
    args['reports']=appraisment_list
    return render_to_response('Reports/ReportList.html',args)