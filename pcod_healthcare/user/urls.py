from django.urls import path
from . import views

urlpatterns = [    

    path('userdashboard/',views.user_dashboard,name="userdashboard"),
    path('userdashboard/chatapp',views.chatapp,name="chat_app"),
    path('userdashboard/list_community_user',views.list_community_user,name="list_community_user"),
    path('userdashboard/chatsystembox/<int:doctor_id>/',views.chatsystem,name="chat_system_box"),
    path('userdashboard/join/<int:id>/',views.join,name="join"),
    path('community/<int:community_id>/chat/', views.community_chat, name='community_chat'),
    path('', views.home, name='home_page'),  # Home Page
    path('userdashboard/', views.user_dashboard, name='dashboard'),
   


]