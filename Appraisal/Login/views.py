# Create your views here.
from django.shortcuts import render_to_response
from Login.models import  Question

#from Questionare.models import Login

def login(request):
    #Questions = Question.objects.all()
    return render_to_response('Login.html',{'Questions' : "dsdasdss"}) 

def loggedin(request):
    values = request.META.items()
    values.sort()
    path = request.path
    #Questions = request.GET.get('txt')  
    return render_to_response('Loggedin.html',{'Question' : values, 'path' : path})