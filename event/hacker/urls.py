from django.urls import path
from hacker import views 

urlpatterns = [

    path('hdash', views.dash, name='hacker-dash'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('verifyphone', views.verify_by_otp, name='verify-by-otp'),
    path('verifybycall', views.verify_by_call, name='verify-by-call'),
    path('discord', views.update_checkbox, name='discord'),
    path('guide', views.guide, name="guide"),
]