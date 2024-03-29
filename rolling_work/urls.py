from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("save", views.save, name="save"),
    path("record/<int:num>", views.show_record, name="record"),
    path("about", views.show_about, name="about"),
    path("profile/<str:name>", views.show_profile, name="profile"),
    path("rank", views.show_rank, name="rank"),
    path("rank/<str:cat>", views.show_rank, name="rank"),
]
