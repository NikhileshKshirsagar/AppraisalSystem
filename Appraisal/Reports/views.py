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
        #Getting values for self appraisment
        if questionUser.answer!=None:
            if questionUser.question.type == 'Scale' :
                appraisment['answerYourself']=float(questionUser.answer.answer)
            elif questionUser.question.type == 'Subjective':
                appraisment['answerYourself']=questionUser.answer.answer
            else:
                
                objoptionHeader = Option.objects.get(option_id=questionUser.answer.answer)
                
                appraisment['answerYourself']=objoptionHeader.option_id
                
                objOption =Option.objects.filter(option_header=questionUser.question.option_header)
              #  appraisment['option']=objOption
                option_list = []
                for options in objOption:
                    option={}
                    option['option_text']=options.option_text
                    option['option_id']=options.option_id
                    option['option_level']=options.option_level
                    option['option_count']=0
                    
                    #Calculating others appraisment values for MCQ (Need this because it has to be added with options list)
                    for questionOther in objAppOthers:
                         try:
                             objappContent = AppraisalContent.objects.get(appresment=questionOther.appraisment_id,question=questionUser.question)
                         except:
                             objappContent=None
                         if objappContent!=None:
                             if objappContent.answer!=None:
                                 if objappContent.question.type == 'MCQ' :
                                     if str(objappContent.answer.answer) == str(options.option_id):
                                         option['option_count']=option['option_count']+1
                    option_list.append(option)
                appraisment['options']=option_list
        count=0                        
        answerOther=''
        
        #Calculating others appraisment values for scale and subjective
        if objAppOthers!=None:
            sAnswer=''
            arrAnswerUserList=[]
            
            appraisment['answerOther']=0
            for questionOther in objAppOthers:
                
                try:
                    #data = AppraisalContent.objects.filter(appresment=objAppOthers.appraisment_id,question=questionUser.question).count()
                   # print data
                    objappContent = AppraisalContent.objects.get(appresment=questionOther.appraisment_id,question=questionUser.question)
                except:
                    objappContent=None
                if objappContent!=None:
                    if objappContent.answer!=None:
                        if objappContent.question.type == 'Scale' :
                            sAnswer=objappContent.answer.answer
                            appraisment['answerOther']=float((appraisment['answerOther']*count+int(sAnswer))/(count+1))
                            count = count +1
                            appraisment['count']=count
                        elif questionUser.question.type == 'Subjective':
                            count = count +1
                            sAnswer=sAnswer+ str(count)+') '+objappContent.answer.answer+'\n'
                            appraisment['answerOther']=sAnswer
        
        
        #Calculating the total column values for scale and MCQ type question
        if questionUser.question.type == 'Scale' :
            appraisment['total'] =   appraisment['answerOther']-appraisment['answerYourself']
        elif questionUser.question.type == 'MCQ' :
            selfCount = 0.0
            otherCount = 0.0
            userCount=0
            for option in appraisment['options']:
                if option['option_id'] == appraisment['answerYourself']:
                    selfCount = option['option_level']
                otherCount = otherCount + float(option['option_level']*option['option_count'])
                userCount=userCount + option['option_count']
            appraisment['mcqSelfCount']=selfCount
            appraisment['mcqOtherCount']=float(otherCount/userCount)
            appraisment['total'] =  float(otherCount/userCount) -selfCount
        
        appraisment_list.append(appraisment)
    
    args['UserID']=  request.session['UserID']
    args['username']=request.session['UserName']
    args['reports']=appraisment_list
    return render_to_response('Reports/ReportList.html',args)