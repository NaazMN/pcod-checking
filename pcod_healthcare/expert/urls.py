from django.urls import path,include
from . import views

urlpatterns = [   

        path('expert/',views.exper_dashboard,name="expert_dashboard"),

        path('expert/chat',views.message_inbox,name="message_inbox"),
        path('expert/community',views.community,name="community"),
        path('expert/list_community',views.list_community,name="list_community"),
        path('expert/list_community/mine',views.list_community_mine,name="list_community_mine"),

        path('community/<int:community_id>/members/', views.community_members, name='community_members'),
        path('community/<int:join_id>/approve/', views.approve, name='approve_member'),
        




 ]