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
        confirm = request.POST["confirm"]
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

def add_zero(num):
    if num < 10:
        return '0'+str(num)
    return str(num)
@login_required
def show_record(request, num):
    record = Record.objects.get(id=num)
    print(type(request.user.username), type(record.owner.username))
    if request.user.username != record.owner.username:
        print("Not the right user!")
        return render(request, "rolling_work/record.html", {
            "msg": "You have no permission to see this record!"
        })
    print("Show my record", record)
    LWP_sc = record.longest_work_period
    LWP_min = LWP_sc // 60
    LWP_sc %= 60
    LWP_hr = LWP_min // 60
    LWP_min %= 60

    LRP_sc = record.longest_rest_period
    LRP_min = LRP_sc // 60
    LRP_sc %= 60
    LRP_hr = LRP_min // 60
    LRP_min %= 60

    SWP_sc = record.shortest_work_period
    SWP_min = SWP_sc // 60
    SWP_sc %= 60
    SWP_hr = SWP_min // 60
    SWP_min %= 60

    SRP_sc = record.shortest_rest_period
    SRP_min = SRP_sc // 60
    SRP_sc %= 60
    SRP_hr = SRP_min // 60
    SRP_min %= 60

    WT_sc = record.work_total
    WT_min = WT_sc // 60
    WT_sc %= 60
    WT_hr = WT_min // 60
    WT_min %= 60

    AT_sc = record.app_total
    AT_min = AT_sc // 60
    AT_sc %= 60
    AT_hr = AT_min // 60
    AT_min %= 60
    return render(request, "rolling_work/record.html", {
        "LWP_hr": add_zero(LWP_hr),
        "LWP_min": add_zero(LWP_min),
        "LWP_sc": add_zero(LWP_sc),

        "LRP_hr": add_zero(LRP_hr),
        "LRP_min": add_zero(LRP_min),
        "LRP_sc": add_zero(LRP_sc),

        "SWP_hr": add_zero(SWP_hr),
        "SWP_min": add_zero(SWP_min),
        "SWP_sc": add_zero(SWP_sc),

        "SRP_hr": add_zero(SRP_hr),
        "SRP_min": add_zero(SRP_min),
        "SRP_sc": add_zero(SRP_sc),

        "WT_hr": add_zero(WT_hr),
        "WT_min": add_zero(WT_min),
        "WT_sc": add_zero(WT_sc),

        "AT_hr": add_zero(AT_hr),
        "AT_min": add_zero(AT_min),
        "AT_sc": add_zero(AT_sc),

        "RC": record.roll_count,
        "efficiency": int(record.work_total / record.app_total * 100),
    })

def show_about(request):
    return render(request, "rolling_work/about.html")