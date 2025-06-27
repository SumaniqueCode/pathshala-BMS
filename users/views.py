from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages


def loginUser(request):
    errors = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # returns boolean value if any value matching username exists in model User
        check_user = User.objects.filter(username=username).exists() 
        if check_user:
            # for authenticating user with username and password
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user:
                login(request, authenticated_user) # saves the user data in session 
                messages.success(request, "You have successfully logged in")
                return redirect("/home") # redirects to /home route
            else:
                errors['password'] = "Invalid Password!" #stores error in key 'password'
        else:
            errors['username'] = "User doesnot exist."
        
        if errors:
            return render(request, 'pages/auth/login.html', {'errors': errors}) # renders login.html with errors