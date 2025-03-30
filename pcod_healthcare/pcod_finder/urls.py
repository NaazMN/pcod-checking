from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.print_hello, name="home"),
    path('register/', views.register, name="register_page"),
    path('register/login/', views.login, name="register_login"),  # Fixed login inside register
    path('login/', views.login, name="login"),
    path('predict/', views.predict, name="predict"),
    path('learmore/', views.learmore, name="learmore"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    
    # Ensure 'user/' and 'expert/' prefixes avoid conflicts
    path('user/', include('user.urls')),
    path('expert/', include('expert.urls')),

    path('expert/registeration/', views.healthcareexpert_reg, name="expert_registeration"),
]
