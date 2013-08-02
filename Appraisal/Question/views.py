# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from forms import QuestionForm, OptionFrom
from Login.models import OptionHeader,Option
from django.http import HttpResponseRedirect 
from django.core.context_processors import csrf
from django.utils import simplejson

from Login.models import UserDetails
def questionCreateView(request):
    
    args={}
    args.update(csrf(request))
    args['error']=''
    objQuestionForm = QuestionForm(request.POST or None)
    objOptionForm = OptionFrom(request.POST or None)
    if request.method == 'POST':
        if request.POST['type_text'] == 'MCQ':
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
           if request.POST['type_text'] == 'MCQ':
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

def OptionList(request):
    objOptions = OptionHeader.objects.all();
    result=''
    for optionheader in objOptions:
        result += '<div class=\"accordion\" id=\"accordion_'+str(optionheader.option_header_id)+'\" ><div class=\"accordion-group\"><div class=\"accordion-heading\"><a data-toggle=\"collapse\" data-parent=\"#accordion_'+str(optionheader.option_header_id)+'\" href=\"#accordionCollapse_'+str(optionheader.option_header_id)+'\" class=\"accordion-toggle\"><i class=\"icon-minus-sign icon-white\"></i>&nbsp;'+optionheader.title+' </a><a name=\"btnUseIt\" class=\"btn btn-primary\" data=\"'+ str(optionheader.option_header_id) +'\">Use it</a></div><div class=\"accordion-body collapse\" id=\"accordionCollapse_'+str(optionheader.option_header_id)+'\"><div class=\"accordion-inner\">' 
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

