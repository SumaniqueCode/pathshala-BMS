from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Profile # model exists in same folder


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
                return redirect("/") # redirects to /home route
            else:
                errors['password'] = "Invalid Password!" #stores error in key 'password'
        else:
            errors['username'] = "User doesnot exist."
        
        if errors:
            return render(request, 'pages/auth/login.html', {'errors': errors}) # renders login.html with errors
        
def signupUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get("email")
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        profile_image = request.FILES.get('profile_image')
        dob = request.POST.get('dob')
        nationality = request.POST.get('nationality')
        
        #creating a new user in User Model
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        
        #creating a new profile in Profile Model for user
        # Profile.objects.create(user=user, address=address, phone=phone, gender=gender, dob=dob, nationality=nationality, profile_image=profile_image)
       
        # alternative method
        # user =  User(username=username, email=email, first_name=first_name, last_name=last_name)
        # user.set_password(password)
        # user.save()
        
        profile = Profile(user=user, address=address, phone=phone, gender=gender, dob=dob, nationality=nationality)
        if profile_image:
            profile.profile_image = profile_image
        else:
           profile.profile_image = 'users/default_user.png'
        
        profile.save()
        
        messages.success(request, "You have successfully signed up")
        return redirect('/auth/log-in')