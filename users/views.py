from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile # model exists in same folder
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required

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
    errors = {}
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
        
        user_exists = User.objects.filter(username = username).exists()
        email_exists = User.objects.filter(email=email).exists()
        phone_exits = Profile.objects.filter(phone=phone).exists()
        
        if user_exists:
            errors['username'] = "Username already exists."
        if phone_exits:
            errors['phone'] = "Phone number already exists."
        if len(phone) != 10:
            errors['phone'] = "Phone number should be 10 digits."
        if len(first_name)<3:
            errors['first_name'] = " Enter at least 3 characters."
        if password != confirm_password:
            errors['confirm_password'] = "Passwords do not match."
        if len(username) <3:
            errors['username'] = "Username should be at least 3 characters."
        if len(address)<3:
            errors['address'] = "Enter at least 3 characters."
        if profile_image:
            allowed_extensions = [ "jpg", "png", "jpeg"]
            if profile_image.size > 5*1024*1024:
                errors['profile_image'] = "Image size should be less than 5MB."
            image_extension = profile_image.name.split('.')[-1] # splits the data by '.' and gets the last part
            if image_extension.lower() not in allowed_extensions:
                errors['profile_image'] = f"{image_extension} is not allowed, allowed extensions are .jpg, .png, .jpeg"
        try:
            validate_password(password)
        except Exception as e:
            errors['password'] = e
            
        try:
            if email_exists:
                errors['email'] = ["Email already exists.",]
            validate_email(email)
        except Exception as e:
            errors['email'] = e
        
        if errors:
            print(errors)
            return render(request, 'pages/auth/signup.html', {'errors': errors}) # renders signup.html
        else:
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

def logoutUser(request):
    logout(request)
    messages.success(request, "User Logged out successfully!")
    return redirect('/')

@login_required(login_url="/auth/log-in")
def editUserPage(request):
    return render(request, 'pages/auth/editPage.html')
    
def updateUser(request):
    errors = {}
    if request.method == "POST":
        user = request.user
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
        
        user_exists = User.objects.filter(username = username).exists()
        email_exists = User.objects.filter(email=email).exists()
        phone_exits = Profile.objects.filter(phone=phone).exists()
        
        if user.username !=username  and user_exists:
            errors['username'] = "Username already exists."
        if user.profile.phone !=phone and phone_exits:
            errors['phone'] = "Phone number already exists."
        if len(phone) != 10:
            errors['phone'] = "Phone number should be 10 digits."
        if len(first_name)<3:
            errors['first_name'] = " Enter at least 3 characters."
        if password != confirm_password:
            errors['confirm_password'] = "Passwords do not match."
        if len(username) <3:
            errors['username'] = "Username should be at least 3 characters."
        if len(address)<3:
            errors['address'] = "Enter at least 3 characters."
        if profile_image:
            allowed_extensions = [ "jpg", "png", "jpeg"]
            if profile_image.size > 5*1024*1024:
                errors['profile_image'] = "Image size should be less than 5MB."
            image_extension = profile_image.name.split('.')[-1] # splits the data by '.' and gets the last part
            if image_extension.lower() not in allowed_extensions:
                errors['profile_image'] = f"{image_extension} is not allowed, allowed extensions are .jpg, .png, .jpeg"
                    
        try:
            if password:
                validate_password(password)
        except Exception as e:
            errors['password'] = e
            
        try:
            if user.email != email and email_exists:
                errors['email'] = ["Email already exists.",]
            validate_email(email)
        except Exception as e:
            errors['email'] = e
        
        if errors:
            print(errors)
            return render(request, 'pages/auth/editPage.html', {'errors': errors, 'image_extension':image_extension}) # renders editPage.html
        else:
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            if password:
                user.set_password(password)
                authenticate_user = authenticate(request, username=username, password=password)
                login(request, authenticate_user)
            profile = user.profile
            profile.gender = gender
            profile.nationality = nationality
            profile.dob = dob
            profile.address = address
            profile.phone = phone
            if profile_image:
                profile.profile_image = profile_image
            user.save()
            profile.save()
            messages.success(request, "User Data updated successfully.")
            return redirect('/profile')