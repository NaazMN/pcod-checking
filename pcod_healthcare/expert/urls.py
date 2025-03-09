from django.urls import path,include
from . import views

urlpatterns = [   

        path('expert/',views.exper_dashboard,name="expert_dashboard"),

 ]