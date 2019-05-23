from django.shortcuts import render,HttpResponse

# Create your views here.

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request,'register.html')