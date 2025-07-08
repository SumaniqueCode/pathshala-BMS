from django.shortcuts import render, redirect
from django.contrib import messages

def addBlogPage(request):
    return render(request, 'pages/blogs/addBlogPage.html')

def createBlog(request):
    if request.method == "POST":
        messages.success(request, "Blog Created Successfully!")
        return redirect('/blogs')
