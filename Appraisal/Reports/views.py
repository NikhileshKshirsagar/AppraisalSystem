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
    index=0
    arrAnswerUserList=[]
    try:
        objAppOthers = Appraisment.objects.filter(appraisee=nUserID).exclude(appraiser=nUserID)
    except:
        objAppOthers=None
    appraisment_list = []
    objQuestionUser = AppraisalContent.objects.filter(appresment=objAppUser.appraisment_id)
    for questionUser in objQuestionUser:
        appraisment = {}
        appraisment['header']=questionUser.question.info
        appraisment['question']=questionUser.question.question
        appraisment['status']=questionUser.question.type
        if questionUser.answer!=None:
            if questionUser.question.type == 'Scale' or questionUser.question.type == 'Subjective':
                appraisment['answerYourself']=questionUser.answer.answer
            else:
                objoptionHeader = Option.objects.get(option_id=questionUser.answer.answer)
                appraisment['answerYourself']=objoptionHeader.option_id
                
                objOption =Option.objects.filter(option_header=questionUser.question.option_header)
                appraisment['option']=objOption
              #  option_list = []
              #  for options in objOption:
              #      option={}
              #      option['text']=options.option_text
              #      option['ID']=options.option_id
              #      option_list.append(option)
               # appraisment['option']=option_list
                                
        answerOther=''
        if objAppOthers!=None:
            sAnswer=None
            for questionOther in objAppOthers:
                try:
                    objappContent = AppraisalContent.objects.get(appresment=questionOther.appraisment_id,question=questionUser.question)
                except:
                    objappContent=None
                if objappContent!=None:
                    if objappContent.answer!=None:
                        if objappContent.question.type == 'Scale' or questionUser.question.type == 'Subjective':
                            sAnswer=sAnswer+objappContent.answer.answer
                            appraisment['answerOther']=sAnswer
                        else:
                            arrAnswerUser={}
                            #sAnswer=Option.objects.get(option_id=objappContent.answer.answer).option_id
                            arrAnswerUser['ID']=Option.objects.get(option_id=questionUser.answer.answer).option_id
                            arrAnswerUserList.append(arrAnswerUser)
                            sAnswer=arrAnswerUserList
                            appraisment['answerOther']=arrAnswerUserList
     
        appraisment_list.append(appraisment)
    
    args['UserID']=  request.session['UserID']
    args['username']=request.session['UserName']
    args['reports']=appraisment_list
    return render_to_response('Reports/ReportList.html',args)