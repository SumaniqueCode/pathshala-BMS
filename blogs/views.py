from django.shortcuts import render

def addBlogPage(request):
    return render(request, 'pages/blogs/addBlogPage.html')
