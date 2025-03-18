from django.urls import path
from . import views

urlpatterns = [    

    path('userdashboard/',views.user_dashboard,name="userdashboard"),
    path('userdashboard/chatapp',views.chatapp,name="chat_app"),
    path('userdashboard/chatsystembox/<int:doctor_id>/',views.chatsystem,name="chat_system_box")


]