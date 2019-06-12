from django.shortcuts import render,HttpResponse

# Create your views here.

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request,'register.html')

def homepage(request):
    return render(request,'homepage.html')

def vocabubook(request):
    return render(request,'vocabubook.html')

def vocabunote(request):
    return render(request,'vocabunote.html')