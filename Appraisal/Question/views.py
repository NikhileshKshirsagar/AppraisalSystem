# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from forms import QuestionForm, OptionFrom
from Login.models import OptionHeader, Option, Question
from django.http import HttpResponseRedirect 
from django.core.context_processors import csrf
from django.utils import simplejson
from django.utils import timezone


from Login.models import UserDetails
def questionCreateView(request):
    
    args={}
    args.update(csrf(request))
    args['error']=''
    objQuestionForm = QuestionForm(request.POST or None)
    objOptionForm = OptionFrom(request.POST or None)
    if request.method == 'POST':
        if request.POST['type_text'] == 'MCQ':
 #           objOptionForm.clean_optionheadertext(sOptionHeaderText=request.POST['option_header_text'],nOptionHeaderID=request.POST['option_header_id'])
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
           iOptionHeaderID = 0 
           i_UserId = UserDetails.objects.get(user_id=request.session['UserID'])
           if request.POST['type_text'] == 'MCQ':
               if request.POST['option_header_id']=='0':
                   objOptionHeader = OptionHeader.objects.create(title=request.POST['option_header_text'], modified_by=i_UserId, modified_on=timezone.now())
                   iOptionHeaderID = OptionHeader.objects.latest('option_header_id')
                   objOptionForm.save(commit=False, userId=i_UserId, optionHeaderId=iOptionHeaderID)
                   
               else:
                   iOptionHeaderID = OptionHeader.objects.get(option_header_id=request.POST['option_header_id'])
           objQuestionForm.save(commit=False, userId = i_UserId, optionHeaderId = iOptionHeaderID)
           args['successMsg']="Question created successfully"
           objOptionForm = OptionFrom()
           initial = {'type_text' : request.POST['type_text']}
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

def OptionList(request):
    objOptions = OptionHeader.objects.all();
    result=''
    for optionheader in objOptions:
        result += '<div class=\"accordion\" id=\"accordion_'+str(optionheader.option_header_id)+'\" ><div class=\"accordion-group\"><div class=\"accordion-heading\"><a data-toggle=\"collapse\" data-parent=\"#accordion_'+str(optionheader.option_header_id)+'\" href=\"#accordionCollapse_'+str(optionheader.option_header_id)+'\" class=\"accordion-toggle\"><i class=\"icon-minus-sign icon-white\"></i>&nbsp;'+optionheader.title+' </a><a name=\"btnUseIt\" class=\"btn btn-primary\" data=\"'+ str(optionheader.option_header_id) +'\">Use it</a><a name=\"btnEditIt\" class=\"btn btn-primary\" data=\"'+ str(optionheader.option_header_id) +'\">Edit</a></div><div class=\"accordion-body collapse\" id=\"accordionCollapse_'+str(optionheader.option_header_id)+'\"><div class=\"accordion-inner\">' 
        for option in optionheader.option_set.filter():
          result+= option.option_text + '<br/>'
        result+='</div></div></div></div>'
    return HttpResponse(content=result, content_type='text/html')

def OptionDetails(request):
    if request.is_ajax():
        search_text = request.POST.get('search_txt')
        objOptions = OptionHeader.objects.get(option_header_id=search_text);
        result =''
        for option in objOptions.option_set.filter():
          result+= option.option_text + ','
        objDetails = {'OptionHeaderID':objOptions.option_header_id,
                      'OptionHeader' :objOptions.title,
                      'Options' : result[:-1]
                      }
        data = simplejson.dumps(objDetails)
        return HttpResponse(content=data, content_type='json')    

def QuestionList(request):
    objQuestion = Question.objects.all();
    #for objOption in objOptions:
    #    objJsonOptions = {'option_header':objOption.option_header,
    #                      'question_id' : objOption.question_id,
    #                       'question' : objOption.question,
    #                       'level' : objOption.level,
    #                       'weight' : objOption.weight,
    #                       'type' : objOption.type,
    #                       'intent' : objOption.intent
    #                      }
    args={}
    args.update(csrf(request))
    args['error']=''
    args['QuestionList']=objQuestion
    return render_to_response('Questions/QuestionList.html',args)

def validateOptionHeader(request):
    if request.is_ajax():
        stitle = request.POST.get('stitle')
        nOptionHeaderID = request.POST.get('nOptionHeaderID')
        error_msg=''
        objOptions = OptionHeader.objects.filter(title=stitle).exclude(option_header_id=nOptionHeaderID).count()
        if objOptions> 0 :
            error_msg='Option header already exists'
        data = simplejson.dumps({'error':error_msg})
        return HttpResponse(content=data, content_type='json')      
    
def updateOption(request):
      if request.is_ajax():
            objOptionForm = OptionFrom(request.POST or None)
            iOptionHeaderID= OptionHeader.objects.get(option_header_id=request.POST.get('option_header_id'))
            OptionHeader.objects.filter(option_header_id=request.POST.get('option_header_id')).update(title=request.POST.get('option_header_text'))
            i_UserId = UserDetails.objects.get(user_id=request.session['UserID'])
            Option.objects.filter(option_header=iOptionHeaderID).delete()
            objOptionForm.save(commit=False, userId=i_UserId, optionHeaderId=iOptionHeaderID)
      success_msg='Record updated successfully'
      data = simplejson.dumps({'success':success_msg})
      return HttpResponse(content=data, content_type='json')   
  
  
def deleteQuestion(request):
      if request.is_ajax():
          Question.objects.filter(question_id=request.POST.get('QuestionID')).delete()
      success_msg='Record deleted successfully'    
      data = simplejson.dumps({'success':success_msg})
      return HttpResponse(content=data, content_type='json')   
      
      
def editQuestion(request, questionId):
    args={}
    args.update(csrf(request))
    objQuestionForm = QuestionForm(request.POST or None)
    objOptionForm = OptionFrom(request.POST or None)
    if request.method == 'POST':
        
        if objQuestionForm.is_valid():
            print '--------------------'
            print request.POST['questionID']
            print request.POST['question']
            Question.objects.filter(question_id=request.POST['questionID']).update(question=request.POST['question'],level=request.POST['level'],weight=request.POST['weight'],info=request.POST['info'],intent=request.POST['intent'],type=request.POST['type_text'],option_header=None)
            return HttpResponseRedirect("/question/QuestionList")
        else:
            args['optionCreateform']=objOptionForm
            print '--------------------'
            args['questionCreateform']=objQuestionForm
    else:    
        objQuestion=Question.objects.get(question_id=int(questionId))
        
        if objQuestion.type=='MCQ':
            objOptionHeader=OptionHeader.objects.get(option_header_id=objQuestion.option_header_id)
            objOption=Option.objects.filter(option_header=objOptionHeader.option_header_id)
            optionText=''
            for option in objOption:
                optionText+=option.option_text + ','
            optionText=optionText[:-1]
            objOptionForm = OptionFrom(initial={'option_text':optionText,'option_header_text':objOptionHeader.title})
            
        args['optionCreateform']=objOptionForm
        
        objQuestionForm = QuestionForm(initial={'questionID':questionId,'question':objQuestion.question,'level':objQuestion.level,'weight':objQuestion.weight,'info':objQuestion.info,'intent':objQuestion.intent,'type_text':objQuestion.type})
        args['questionCreateform']=objQuestionForm
    
    return render_to_response('Questions/CreateQuestion.html',args)

    