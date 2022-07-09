from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from .models import User, Record
from django.urls import reverse
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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

@login_required
def save(request):
    data = json.loads(request.body)
    new_record = Record(
        owner = request.user,
        longest_work_period = data["nLWP"],
        shortest_work_period = data["nSWP"],
        longest_rest_period = data["nLRP"],
        shortest_rest_period = data["nSRP"],
        work_total = data["nWT"],
        app_total = data["nAT"],
        roll_count = data["nRC"],
    )
    new_record.save()
    return JsonResponse({"record_id": new_record.id})

@login_required
def show_record(request, num):
    record = Record.objects.get(id=num)
    print(type(request.user.username), type(record.owner.username))
    if request.user.username != record.owner.username:
        print("Not the right user!")
        return render(request, "rolling_work/record.html", {
            "msg": "You have no permission to see this record!"
        })
    print("Show my record")
    return render(request, "rolling_work/record.html", {
        "my_record": record
    })