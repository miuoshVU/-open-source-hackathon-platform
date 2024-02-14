from django.urls import path
from django.contrib.auth import views as auther
from default import views


urlpatterns = [
     path('', views.landing, name='landing'),
     path('rules/', views.rules, name='rules'),
     path('register', views.registration, name='registration'),
     path('login', views.login_page, name='login'),
     path('logout/', views.logout_user, name='logout'),

     path('reset-password', views.password_reset_request, name="reset_password"),
     path('reset-password-sent',
          auther.PasswordResetDoneView.as_view(template_name="defaults/password_reset_sent.html"), name='password_reset_done'),
     path('reset/<uidb64>/<token>', auther.PasswordResetConfirmView.as_view(template_name="defaults/password_reset_form.html"),
         name='password_reset_confirm'),
     path('reset-password-success', auther.PasswordResetCompleteView.as_view(template_name="defaults/password_reset_success.html"),
         name='password_reset_complete'),
     path('get/json/email/verification', views.check_email, name="check_email"),
     path('get/json/password/verification', views.check_password, name="check_password"),
     
     path('profile/<int:pk>', views.profile_page, name='profile'),
     path('privacy/', views.privacy_policy_view, name='privacy'),
     path('conduct/', views.code_of_conduct_view, name='conduct'),
     path('incomingcall', views.incoming_call, name='incomingcall'),

]
