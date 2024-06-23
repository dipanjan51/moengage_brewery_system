from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
# from .forms import SignupForm


def signup_view(request):
    if request.method=='POST':
        username     = request.POST.get('username')
        email        = request.POST.get('email')
        password1    = request.POST.get('password1')
        password2    = request.POST.get('password2')

        if password1 != password2:
            return HttpResponse("Your password and confirm password are not Same!")
        else:
            user = User.objects.create_user(username, email, password1)
            user.save()
            messages.success(request, "Your account has been created!")

            return redirect(login_view)
    return render (request,'users/signup.html')

    # form = SignupForm()

    # if request.method == 'POST':
    #     form = SignupForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("login")
    
    # context = {'signupform': form}
    # return render(request, 'users/signup.html', context=context)


def login_view(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user     = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            # return render(request, 'breweries/home.html', {'username': username})
        else:
            messages.error(request, "Bad Credentials!")
            return redirect(login_view)

    return render(request, 'users/login.html')
    