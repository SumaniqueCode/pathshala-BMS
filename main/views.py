from collections import defaultdict
import json
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from blogs.models import Blog, BlogStats
from users.models import User


def landingPage(request):
    return render(request, "pages/index.html")


def aboutPage(request):
    return render(request, "pages/aboutus/about_page.html")


def loginPage(request):
    return render(request, "pages/auth/login.html")


def signupPage(request):
    return render(request, "pages/auth/signup.html")


def blogPage(request):
    blogs = Blog.objects.filter(status="Active").order_by("-created_at")
    return render(request, "pages/blogs/blogs.html", {"blogs": blogs})


@login_required(login_url="/auth/log-in/")
def profilePage(request):
    return render(request, "pages/auth/profile.html")


@login_required(login_url="/auth/log-in/")
def dashboard(request):
    if request.user.profile.role == "Admin":
        return redirect("/admin/dashboard")

    user_blogs = Blog.objects.filter(author=request.user)
    blogstats = BlogStats.objects.filter(blog__in=user_blogs).order_by("created_at")
    click_data = defaultdict(int)
    unique_data = defaultdict(int)
    for b in blogstats:
        date_str = b.created_at.strftime("%Y-%m-%d")
        click_data[date_str] += b.blog_clicks
        unique_data[date_str] += b.unique_views

    # blog stats
    blog_clicks = list(click_data.values())
    click_date = list(click_data.keys())
    unique_views = list(unique_data.values())

    context = {
        "blog_clicks": blog_clicks,
        "click_date": click_date,
        "unique_views": unique_views,
    }
    return render(request, "pages/dashboard/writer/dashboard.html", context)


def blogList(request):
    blogs = Blog.objects.filter(author=request.user).order_by("-created_at")
    return render(request, "pages/dashboard/writer/blogList.html", {"blogs": blogs})


@login_required(login_url="/auth/log-in")
def adminDashboard(request):
    if request.user.profile.role == "Admin":
        blogstats = BlogStats.objects.all().order_by("created_at")
        click_data = defaultdict(int)
        unique_data = defaultdict(int)
        
        for b in blogstats:
            date_str = b.created_at.strftime("%Y-%m-%d")
            click_data[date_str] += b.blog_clicks
            unique_data[date_str] += b.unique_views
        
        # blog stats
        blog_clicks = list(click_data.values())
        click_date = list(click_data.keys())
        unique_views = list(unique_data.values())
        
        # counting users
        users = User.objects.all()
        user_data = defaultdict(int)
        for user in users:
            date_str = user.date_joined.strftime("%Y-%m-%d")
            user_data[date_str] += 1
            # user stats
        user_date = list(user_data.keys())
        user_count = list(user_data.values())
        context = {
            "user_date": user_date,
            "user_count": user_count,
            "blog_clicks": blog_clicks,
            "click_date": click_date,
            "unique_views": unique_views,
        }
        return render(request, "pages/dashboard/admin/dashboard.html", context)
    else:
        return redirect("/writer/dashboard")
