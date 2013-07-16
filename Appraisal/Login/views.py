# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session

from forms import LoginForm
from django.http import HttpResponseRedirect 
from django.core.context_processors import csrf
#from Questionare.models import Login


def login(request):
    args={}
    args.update(csrf(request))
    if request.POST:
        form = LoginForm(request.POST)
        args['form']=form
        if form.is_valid():
            #flag=UserDetails.objects.filter(firstname=request.POST['txtUserName'],password=request.POST['txtPassword']).exists()
            sUserID = form.Authenticate()
            if sUserID != 0:
                args['username']= request.POST['txtUserName']
                request.session['UserID']=sUserID
                return render_to_response('Welcome.html',args)
            else :
               args['error']='Not Valid user'
               return render_to_response('Login.html',args)    
        else:
            return render_to_response('Login.html',args)
            
    else:  
        objLoginForm = LoginForm()
        args['form']=objLoginForm
        return render_to_response('Login.html', args)
         
def logout(request):
    del request.session['UserID']
  # del request.session['Password']
    args={}
    args.update(csrf(request))
    objLoginForm = LoginForm()
    args['form']=objLoginForm
    args['error']='Logout Successfully'
    return render_to_response('Login.html',args)
     