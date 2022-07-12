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
    # print("here")
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
    # print(type(request.user.username), type(record.owner.username))
    if request.user.username != record.owner.username:
        # print("Not the right user!")
        return render(request, "rolling_work/record.html", {
            "msg": "You have no permission to see this record!"
        })
    # print("Show my record", record)
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

        "time": record.timestamp.strftime("%b %d, %Y, %H:%M")
    })

def show_about(request):
    return render(request, "rolling_work/about.html")

def show_profile(request, name):
    if name != request.user.username:
        return render(request, "rolling_work/profile.html", {
            "msg": "You have no permission to see this record!"
        })
    else:
        my_records = Record.objects.filter(owner=request.user).order_by("-timestamp").all()
        LWP_avg_hr = 0
        LWP_avg_ms = 0
        LWP_avg_sc = 0
        
        WT_avg_hr = 0
        WT_avg_ms = 0
        WT_avg_sc = 0
        
        AT_avg_hr = 0
        AT_avg_ms = 0
        AT_avg_sc = 0
        count = len(my_records)
        history = []
        for my_record in my_records:
            history.append(my_record.brief_view())
            LWP_avg_sc += my_record.longest_work_period
            WT_avg_sc += my_record.work_total
            AT_avg_sc += my_record.app_total
            # print(my_record.brief_view())

        # print(WT_avg_sc, AT_avg_sc, count)
        efficiency_avg = int(WT_avg_sc / AT_avg_sc / count * 100)
        LWP_avg_sc = int(LWP_avg_sc / count)
        WT_avg_sc = int(WT_avg_sc / count)
        AT_avg_sc = int(AT_avg_sc / count)
        

        LWP_avg_ms = LWP_avg_sc // 60
        LWP_avg_sc %= 60
        LWP_avg_hr = LWP_avg_ms // 60
        LWP_avg_hr %= 60

        WT_avg_ms = LWP_avg_sc // 60
        WT_avg_sc %= 60
        WT_avg_hr = LWP_avg_ms // 60
        WT_avg_ms %= 60

        AT_avg_ms = AT_avg_sc // 60
        AT_avg_sc %= 60
        AT_avg_hr = AT_avg_ms // 60
        AT_avg_ms %= 60
        
        return render(request, "rolling_work/profile.html", {
            "LWP_hr": add_zero(LWP_avg_hr),
            "LWP_min": add_zero(LWP_avg_ms),
            "LWP_sc": add_zero(LWP_avg_sc),

            "WT_hr": add_zero(WT_avg_hr),
            "WT_min": add_zero(WT_avg_ms),
            "WT_sc": add_zero(WT_avg_sc),

            "AT_hr": add_zero(AT_avg_hr),
            "AT_min": add_zero(AT_avg_ms),
            "AT_sc": add_zero(AT_avg_sc),

            "efficiency": efficiency_avg,
            "history": history,
        })

def show_rank(request, cat = None):
    # longest_work_period work_total
    rank_by = cat
    if rank_by == None:
        rank_by = "longest_work_period"
    rank_list = Record.objects.order_by("-"+rank_by).all()
    pretty_list = []
    for i in range(min(10, len(rank_list))):
        now_item = rank_list[i].rank_view()
        now_item["rank"] = i+1
        # print(type(now_item))
        pretty_list.append(now_item)
    # print(pretty_list)
    if cat == None:
        return render(request, "rolling_work/rank.html", {
            "rank": pretty_list,
            "ctl": rank_by,
        })
    else:
        # print('return json response')
        return JsonResponse(pretty_list, safe=False)
    # rank by [x]efficiency, by LWP, WT