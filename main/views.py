import json
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from blogs.models import Blog, BlogStats

def landingPage(request):
    return render(request,'pages/index.html')

def aboutPage(request):
    return render(request, 'pages/aboutus/about_page.html')

def loginPage(request):
    return render (request, 'pages/auth/login.html')

def signupPage(request):
    return render(request, 'pages/auth/signup.html')

def blogPage(request):
    blogs  =  Blog.objects.filter(status='Active').order_by('-created_at')
    return render(request, 'pages/blogs/blogs.html', {'blogs':blogs})

@login_required(login_url='/auth/log-in/')
def profilePage(request):
    return render(request, 'pages/auth/profile.html')

@login_required(login_url='/auth/log-in/')
def dashboard(request):
    blogstats = BlogStats.objects.all()
    blog_clicks = [b.blog_clicks for b in blogstats]
    click_date = [b.created_at.strftime('%Y-%m-%d') for b in blogstats]
    return render(request, 'pages/dashboard/writer/dashboard.html', {"blog_clicks":blog_clicks, "click_date":click_date})

def blogList(request):
    blogs = Blog.objects.filter( author = request.user).order_by('-created_at')
    return render(request, 'pages/dashboard/writer/blogList.html', {'blogs':blogs})

@login_required(login_url="/auth/log-in")
def adminDashboard(request):
    if request.user.profile.role=="Admin":
        return render(request, 'pages/dashboard/admin/dashboard.html')
    else:
        return redirect('/writer/dashboard')

