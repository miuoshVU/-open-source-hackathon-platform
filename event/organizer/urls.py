from django.urls import path, re_path
from organizer import views

urlpatterns = [
     path('odash', views.dash, name='organizer-dash'),
     path('hackers', views.display_hackers, name='display-hackers'),
     path('form/<int:pk>', views.generate_pdf, name='generate_pdf'),
     path('download/hackers/', views.export_hacker_csv, name='export-hackers'),
     path('stats/', views.stats_page, name='statistics'),
]
