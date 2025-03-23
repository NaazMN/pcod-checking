from django.urls import path
from . import views

urlpatterns = [
    path('admin_dash/',views.admin_dash,name="admin_dash"),
    path('permission/community/',views.permission_community,name="permission_community"),
    path('approve/<int:id>/', views.approve, name='approve'),  # Approval URL


    
    ]