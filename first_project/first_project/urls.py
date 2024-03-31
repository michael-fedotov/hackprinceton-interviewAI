from django.contrib import admin
from django.urls import path
from first_app import views

urlpatterns = [
    path('',views.index,name="index"),
    path('home/',views.home,name="home"),
    path('educative/',views.educative,name="educative"),
    path('admin/', admin.site.urls),
    path('record/', views.record,name="record"),
    path('upload_video/', views.upload_video, name='upload_video'),
    path('review_video/', views.review_video, name='review_video')
]
