from django.contrib import admin
from django.urls import path
from first_app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("create/", views.create, name="create"),
    path("jobshow/", views.jobshow, name="jobshow"),

]
