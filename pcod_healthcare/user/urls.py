from django.urls import path
from . import views

urlpatterns = [    

    path('userdashboard/',views.user_dashboard,name="userdashboard"),
    path('userdashboard/chatapp',views.chatapp,name="chat_app")

]