# Create your views here.
from django.shortcuts import render_to_response
from Login.models import UserDetails, Designation, Project, Language, Technology,Answer,Appraisment,AppraisalContent,Option
from django.contrib.sessions.models import Session
from django.template.context import RequestContext
from django.core.context_processors import csrf 
from django.http import HttpResponseRedirect 
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.utils import timezone
from django.utils import simplejson
import json
from Login.views import sessionExpire
#{{objReport.UserCalculation}}<br/>{{objReport.TotalCalculation}}

def GenerateReports(request):
    args={}
    args.update(csrf(request))
    if request.session.get('UserID')==None:
        #sessionExpire(request)
        return HttpResponseRedirect("/expire/")
    nUserID = request.session['UserID']
    objUserId = UserDetails.objects.get(user_id=request.session['UserID'])
    args['type']=objUserId.type
    if  Appraisment.objects.filter(appraisee=nUserID,appraiser=nUserID,status="Reports").count() >=1 :
        AppCount = Appraisment.objects.filter(appraisee=nUserID,consider_appraisal=True).exclude(appraiser=nUserID).count()
        AppCompletedCount =Appraisment.objects.filter(appraisee=nUserID,status="Reports",consider_appraisal=True).exclude(appraiser=nUserID).count()
        if  AppCount>0 and AppCompletedCount>0 and AppCount == AppCompletedCount  :    
            appraisment_list = GenerateReportList(request,nUserID)
            args['reports']=appraisment_list
            calculateFinalIndex(appraisment_list)
            if nTotalCalculation>=1:
                args['othersTotal']=(nUserCalculation /nTotalCalculation)* 100
            else:
                args['othersTotal']=0
            
            if nTotalCalculationSelf>=1:
                 args['selfTotal']=(nSelfCalculation/nTotalCalculationSelf)*100
            else:
                args['selfTotal']=0

        else :
            args['error']="Reports not rolled out."
    else:
        args['error']="Reports not rolled out."
    
    args['UserID']=  request.session['UserID']
    args['username']=request.session['UserName']
    return render_to_response('Reports/ReportList.html',args)


def GenerateReportList(request,nUserID):
    objAppUser = Appraisment.objects.get(appraisee=nUserID,appraiser=nUserID)
    objAppOthers=None

    try:
        objAppOthers = Appraisment.objects.filter(appraisee=nUserID,consider_appraisal=True).exclude(appraiser=nUserID)
    except:
        objAppOthers=None
    appraisment_list = []
    objQuestionUser = AppraisalContent.objects.filter(appresment=objAppUser.appraisment_id).order_by('question__type').order_by('question_order')
    nOrderCount = 1
    for questionUser in objQuestionUser:
     #   print questionUser.question.type
        appraisment = {}
        appraisment['OrderNumber']=str(nOrderCount)
        nOrderCount=nOrderCount+1
        appraisment['questionID']=questionUser.question.question_id
        appraisment['header']=questionUser.question.info
        appraisment['question']=questionUser.question.question
        appraisment['status']=questionUser.question.type
        appraisment['TotalCalculation']=0
        appraisment['UserCalculation']=0
        appraisment['SelfCalculation']=0  
        appraisment['TotalCalculationSelf']=0
        appraisment['extended_answer']=""
        if questionUser.question.intent == True:
            intentValue = 1
        else:
            intentValue = -1
        nextended_answerCount = 1
        #Getting values for self appraisment
        if questionUser.answer!=None:
            print str(nextended_answerCount)
            if questionUser.answer.extended_answer != None and questionUser.answer.extended_answer != "": 
                appraisment['extended_answer'] = str(nextended_answerCount) + ") " + questionUser.answer.extended_answer + "\n"
                nextended_answerCount = nextended_answerCount + 1
            if questionUser.question.type == 'Scale' :
                if questionUser.answer_forbid_user == 0:    
                    appraisment['answerYourself']=float(questionUser.answer.answer)
		    if questionUser.question.intent == True:         
                    	appraisment['SelfCalculation']=float(int(questionUser.answer.answer)*objAppUser.appraiser.user_weight*intentValue*questionUser.question.weight)
                    	appraisment['TotalCalculationSelf']=float(10*objAppUser.appraiser.user_weight*intentValue*questionUser.question.weight)
		    else:
			appraisment['SelfCalculation']=float((int(questionUser.answer.answer)-11)*objAppUser.appraiser.user_weight*intentValue*questionUser.question.weight)
                    	appraisment['TotalCalculationSelf']=float((1-11)*objAppUser.appraiser.user_weight*intentValue*questionUser.question.weight)
                else:
                    appraisment['answerYourself']="-"
            elif questionUser.question.type == 'Subjective':
                if questionUser.answer_forbid_user == 0:
                    appraisment['answerYourself']=questionUser.answer.answer
                else:
                    appraisment['answerYourself']="-"
            else:
                
                
            
                objOption =Option.objects.filter(option_header=questionUser.question.option_header)
		if objOption:
			nOptionMaxCount=objOption[0].option_level
		for option in objOption:
			if nOptionMaxCount <= (option.option_level*intentValue):
				objOptionMax=option
				nOptionMaxCount=option.option_level*intentValue
                #objOptionMax = Option.objects.filter(option_header=questionUser.question.option_header).order_by('-order')[0]
                
                if questionUser.answer_forbid_user == 0:
                    objoptionHeader = Option.objects.get(option_id=questionUser.answer.answer)
                    appraisment['answerYourself']=objoptionHeader.option_id
                    appraisment['SelfCalculation']=float(int(objoptionHeader.option_level)*objAppUser.appraiser.user_weight*intentValue*questionUser.question.weight)
                    appraisment['TotalCalculationSelf']=int(objOptionMax.option_level)*objAppUser.appraiser.user_weight*intentValue*questionUser.question.weight
                else:
                    appraisment['answerYourself']=""
                
              #  appraisment['option']=objOption
                option_list = []
                
                
                for options in objOption:
                    option={}
                    option['option_text']=options.option_text
                    option['option_id']=options.option_id
                    option['option_level']=options.option_level
                    option['option_order']=options.order
                    option['option_count']=0
                    mcqCount=0
                    
                    #Calculating others appraisment values for MCQ (Need this because it has to be added with options list)
                    for questionOther in objAppOthers:
                         
                
                         try:
                             objappContent = AppraisalContent.objects.get(appresment=questionOther.appraisment_id,question=questionUser.question,answer_forbid_admin=1)
                         except:
                             objappContent=None
                         if objappContent!=None:
                             if objappContent.answer!=None:
                                 
                                 if objappContent.question.type == 'MCQ' :
                                     if objappContent.answer_forbid_user == 0:
                                         
                                         if str(objappContent.answer.answer) == str(options.option_id):
                                             if questionUser.answer.extended_answer != None and questionUser.answer.extended_answer !="": 
                                                appraisment['extended_answer']= appraisment['extended_answer']+str(nextended_answerCount)+") "+questionUser.answer.extended_answer+"\n"
                                                nextended_answerCount = nextended_answerCount + 1
            
                                             appraisment['UserCalculation']=float((appraisment['UserCalculation']) +(float(int(options.option_level)*questionOther.appraiser.user_weight*intentValue*questionUser.question.weight)))
                                             appraisment['TotalCalculation']=float((appraisment['TotalCalculation'])+(float(int(objOptionMax.option_level)*questionOther.appraiser.user_weight*intentValue*questionUser.question.weight)))
                                             mcqCount=mcqCount+1
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
                    objappContent = AppraisalContent.objects.get(appresment=questionOther.appraisment_id,question=questionUser.question,answer_forbid_admin=1)
                except:
                    objappContent=None
                if objappContent!=None:
                    if objappContent.answer!=None:
                        
                        if objappContent.question.type == 'Scale' :
                            sAnswer=objappContent.answer.answer
                            
                            if objappContent.answer_forbid_user == 0:
                                appraisment['answerOther']=float((appraisment['answerOther']*count+int(sAnswer))/(count+1))
				if questionUser.question.intent == True:
                                	appraisment['UserCalculation']=float((appraisment['UserCalculation']*count +float(int(sAnswer)*questionOther.appraiser.user_weight*intentValue*questionUser.question.weight))/(count+1))
                                	appraisment['TotalCalculation']=float((appraisment['TotalCalculation']*count+float(10*questionOther.appraiser.user_weight*intentValue*questionUser.question.weight))/(count+1))
				else:
					appraisment['UserCalculation']=float((appraisment['UserCalculation']*count +float((int(sAnswer)-11)*questionOther.appraiser.user_weight*intentValue*questionUser.question.weight))/(count+1))
                                	appraisment['TotalCalculation']=float((appraisment['TotalCalculation']*count+float((1-11)*questionOther.appraiser.user_weight*intentValue*questionUser.question.weight))/(count+1))
                                count = count +1
                                appraisment['count']=count
                                if questionUser.answer.extended_answer != None and questionUser.answer.extended_answer !="":
                                    appraisment['extended_answer']= appraisment['extended_answer']+str(nextended_answerCount)+") "+questionUser.answer.extended_answer+"\n"
                                    nextended_answerCount = nextended_answerCount + 1
            
                            
                        elif questionUser.question.type == 'Subjective':
                            if objappContent.answer_forbid_user == 0:
                                count = count +1
                                sAnswer=sAnswer+ str(count)+') '+objappContent.answer.answer+'\n'
                                appraisment['answerOther']=sAnswer
                            else:
                                appraisment['answerOther']="-"
                            if questionUser.answer.extended_answer != None: 
                                    appraisment['extended_answer']= appraisment['extended_answer']+str(nextended_answerCount)+") "+questionUser.answer.extended_answer+"\n"
                                    nextended_answerCount = nextended_answerCount + 1
                                
        
        
        #Calculating the total column values for scale and MCQ type question
        if questionUser.question.type == 'Scale' :
            if appraisment['answerYourself']=="-":
                nAnswerSelf = 0
            else:
                nAnswerSelf=appraisment['answerYourself']
            if questionUser.question.intent ==1:
                appraisment['total'] =   appraisment['answerOther']-nAnswerSelf
            else:
                appraisment['total'] =   nAnswerSelf-appraisment['answerOther']
        elif questionUser.question.type == 'MCQ' :
            selfCount = 0.0
            otherCount = 0.0
	    nOptionCalCount=0
            userCount=0
            for option in appraisment['options']:
                if option['option_id'] == appraisment['answerYourself']:
                    selfCount = option['option_level']
		nOptionCalCount=nOptionCalCount + option['option_count'] 
                otherCount = otherCount + float(option['option_level']*option['option_count'])
	    otherCount = otherCount/nOptionCalCount
	    appraisment['UserCalculation']=appraisment['UserCalculation']/nOptionCalCount
	    appraisment['TotalCalculation']=appraisment['TotalCalculation']/nOptionCalCount	
            appraisment['mcqSelfCount']=selfCount

            appraisment['mcqOtherCount']=otherCount
            if  questionUser.question.intent ==True:
                appraisment['total'] =  otherCount -selfCount
            else:
                appraisment['total'] =  selfCount - otherCount 
        
        appraisment_list.append(appraisment)    
    return appraisment_list

def calculateFinalIndex(appraismentList):
    global nSelfCalculation
    global nUserCalculation
    global nTotalCalculation
    global nTotalCalculationSelf
    nSelfCalculation=0
    nUserCalculation=0
    nTotalCalculation=0
    nTotalCalculationSelf=0
    for appraisment in appraismentList:
        if appraisment['status']!="Subjective":
            nSelfCalculation = nSelfCalculation + appraisment['SelfCalculation']
            nUserCalculation = nUserCalculation + appraisment['UserCalculation']
            nTotalCalculation = nTotalCalculation + appraisment['TotalCalculation']
            nTotalCalculationSelf =nTotalCalculationSelf+ appraisment['TotalCalculationSelf']
    
            
def adminGenerateEmployeeReports(request):
    args={}
    args.update(csrf(request))
    if request.session.get('UserID')==None:
        #sessionExpire(request)
        return HttpResponseRedirect("/expire/")
    nUserID = request.session['UserID']
    objUserId = UserDetails.objects.get(user_id=request.session['UserID'])
    args['type']=objUserId.type
    if objUserId.type=="Administrator":
        objUsers = UserDetails.objects.filter(type="Employee")
        if request.POST:
            #print '--------------'
            if request.POST['drpUser']!='0':
                userID = int(request.POST['drpUser'])
             #   print Appraisment.objects.filter(appraisee=userID,appraiser=userID,status="Completed").count()
                if  Appraisment.objects.filter(appraisee=userID,appraiser=userID,status__in=["Completed","Reports"]).count() >=1 :
                    AppCount = Appraisment.objects.filter(appraisee=userID,consider_appraisal=True).exclude(appraiser=userID).count()
                    AppCompletedCount =Appraisment.objects.filter(appraisee=userID,status__in=["Completed","Reports"],consider_appraisal=True).exclude(appraiser=userID).count()
                    if AppCount == AppCompletedCount and AppCount !=0:    
                        appraisment_list=GenerateReportList(request, request.POST['drpUser'])
                        args['reports']=appraisment_list
                        calculateFinalIndex(appraisment_list)
                        if nTotalCalculation>=1:
                            args['othersTotal']=(nUserCalculation /nTotalCalculation)* 100
                        else:
                            args['othersTotal']=0
                        
                        if nTotalCalculationSelf>=1:
                             args['selfTotal']=(nSelfCalculation/nTotalCalculationSelf)*100
                        else:
                            args['selfTotal']=0

                    else :
                        args['error']="Appraisal not completed for selected user"
                else:
                    args['error']="Self appraisal not completed"
            else:
                args['error']="Please select user"
            args['UserID']=  request.session['UserID']
            args['username']=request.session['UserName']
            args['UserList']=objUsers
            args['drpUser']=int(request.POST['drpUser'])
            return render_to_response('Reports/ReportList.html',args)
        else:
            args['UserID']=  request.session['UserID']
            args['username']=request.session['UserName']
            args['UserList']=objUsers
            return render_to_response('Reports/ReportList.html',args)
    else:
        args['UserID']=  request.session['UserID']
        args['username']=request.session['UserName']
        args['error']="Not valid user"
        return render_to_response('Reports/ReportList.html',args)

    
def IndividualQuestionDetails(request):
      if request.is_ajax():
        
        nQuestionID = request.POST.get('QuestionID')
        nUserID = request.POST.get('UserID')
        objAppOthers = Appraisment.objects.filter(appraisee=nUserID,consider_appraisal=True).exclude(appraiser=nUserID)
        arrQuestionList=[]
        for appOther in objAppOthers:
           try:
               objappContent = AppraisalContent.objects.get(appresment=appOther.appraisment_id,question=nQuestionID)
           except:
               objappContent=None
           if objappContent:
               lstQuestionList={}
               lstQuestionList['AppraisalContentID']=objappContent.appraisal_content_id
               lstQuestionList['appresmentID']=appOther.appraisment_id
               lstQuestionList['UserName']=appOther.appraiser.firstname
               lstQuestionList['answer_forbid_admin']=objappContent.answer_forbid_admin
               lstQuestionList['answer_forbid_user'] = objappContent.answer_forbid_user
               lstQuestionList['question_type'] = objappContent.question.type
               if objappContent.answer != None:
                   if objappContent.question.type != 'MCQ':
                       lstQuestionList['answer']=objappContent.answer.answer
                   else:
                       lstQuestionList['answer']=Option.objects.get(option_id=objappContent.answer.answer).option_text
               else:
                    lstQuestionList['answer']="-"
               arrQuestionList.append(lstQuestionList)
        data= json.dumps(arrQuestionList) 
        return HttpResponse(content=data, content_type='json')
        #//objOptions = OptionHeader.objects.get(option_header_id=search_text);
        #//result =''
        #//for option in objOptions.option_set.filter():
       # //    result+= option.option_text + '|'+ str(option.option_level) +','
       
        #data = simplejson.dumps(arrQuestionList)
        #data =json.dumps(arrQuestionList)
        #return HttpResponse(content=data, content_type='json')
        
        
def AnswerForbidUpdate(request):
    flag=False
    if request.is_ajax():
        try:
            sAnswerForbid = request.POST.get('AnswerForbid')
            arrAnswerForbid = sAnswerForbid.split("|,|")
            if '|~|' in sAnswerForbid:
                
                for index, sAnswer in enumerate(arrAnswerForbid):
                     arrSplitForbidNID = sAnswer.split("|#|")
                     arrSplitTextForbid = arrSplitForbidNID[1].split("|~|")
                     AppraisalContent.objects.filter(appraisal_content_id=arrSplitForbidNID[0]).update(answer_forbid_admin=arrSplitTextForbid[0],modified_on=timezone.now())
                     
                     objAppraisalContent = AppraisalContent.objects.get(appraisal_content_id=arrSplitForbidNID[0])
                     
                     Answer.objects.filter(answer_id = objAppraisalContent.answer.answer_id).update(answer=arrSplitTextForbid[1],modified_on=timezone.now())
                flag=True
            else:
                for index, sAnswer in enumerate(arrAnswerForbid):
                     arrSplitForbidNID = sAnswer.split("|#|")
                     AppraisalContent.objects.filter(appraisal_content_id=arrSplitForbidNID[0]).update(answer_forbid_admin=arrSplitForbidNID[1],modified_on=timezone.now())
                flag=True
        except:
            flag=False     
    if flag:
        objResponse = {'success':'Records updated'}
    else:
        objResponse = {'error':'Error occurred while updating'}
    
    data = simplejson.dumps(objResponse)
         
    return HttpResponse(content=data, content_type='json')

def ReportsRolledOut(request):
    flag=False
    if request.is_ajax():
        try:
            nUserID = request.POST.get('UserID')
            nAdminUserID = request.session['UserID']
            Appraisment.objects.filter(appraisee=nUserID).update(status="Reports",modified_by=nAdminUserID,modified_on=timezone.now())
            flag=True
        except Exception, e:
            print e.message
            flag=False     
    if flag:
        objResponse = {'success':'Records updated'}
    else:
        objResponse = {'error':'Error occurred while updating'}
    
    data = simplejson.dumps(objResponse)
         
    return HttpResponse(content=data, content_type='json')
                
