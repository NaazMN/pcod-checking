from django.urls import path
from . import views

urlpatterns = [
    path('admin_dash/',views.admin_dash,name="admin_dash"),
    path('permission/community/',views.permission_community,name="permission_community"),
    path('approve/<int:id>/', views.approve, name='approve'),  # Approval URL
    path('list_users/', views.list_users, name='list_users'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),


    
    ]