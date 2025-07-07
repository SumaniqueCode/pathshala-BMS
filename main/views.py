from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def landingPage(request):
    return render(request,'pages/index.html')

def aboutPage(request):
    return render(request, 'pages/aboutus/about_page.html')

def loginPage(request):
    return render (request, 'pages/auth/login.html')

def signupPage(request):
    return render(request, 'pages/auth/signup.html')

def blogPage(request):
    return render(request, 'pages/blogs/blogs.html')

@login_required(login_url='/auth/log-in/')
def profilePage(request):
    return render(request, 'pages/auth/profile.html')