from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    tv_shows_list={"tv_shows":{'Game of Thrones':'9.3','Blacklist': '8','Suits': '8.5','The Witcher': '8.5'}}
    return render(request,'first_app/index.html',context=tv_shows_list)

def home(request):
    return HttpResponse("Welcome to home page!")

def educative(request):
    return HttpResponse("Welcome to Educative page!")

def record(request):
    return render(request,'first_app/record.html')
