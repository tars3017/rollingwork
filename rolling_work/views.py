from django.shortcuts import render


def index(request):
    print("here")
    return render(request, 'rolling_work/index.html')