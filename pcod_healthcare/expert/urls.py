from django.urls import path,include
from . import views

urlpatterns = [   

        path('expert/',views.exper_dashboard,name="expert_dashboard"),

        path('expert/chat',views.message_inbox,name="message_inbox"),
        path('expert/community',views.community,name="community"),



 ]