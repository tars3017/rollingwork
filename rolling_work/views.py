from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
# from .models import User
from django.urls import reverse

def index(request):
    print("here")
    return render(request, 'rolling_work/index.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "rolling_work/login.html", {
                "msg": "Invalid username and/or password.",
            })
    else:
        return render(request, "rolling_work/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        cofirm = request.POST["confirm"]
        if password != confirm:
            return render(request, "rolling_work/register.html", {
                "msg": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:
            return render(request, "rolling_work/register.html", {
                "msg": "Username already being used."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "rolling_work/register.html")