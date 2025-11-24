from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
   
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    
  
    path('caregivers/', views.caregiver_list, name='caregiver_list'),
    path('caregivers/create/', views.caregiver_create, name='caregiver_create'),
    path('caregivers/<int:pk>/', views.caregiver_detail, name='caregiver_detail'),
    path('caregivers/<int:pk>/update/', views.caregiver_update, name='caregiver_update'),
    path('caregivers/<int:pk>/delete/', views.caregiver_delete, name='caregiver_delete'),
    
   
    path('members/', views.member_list, name='member_list'),
    path('members/create/', views.member_create, name='member_create'),
    path('members/<int:pk>/', views.member_detail, name='member_detail'),
    path('members/<int:pk>/update/', views.member_update, name='member_update'),
    path('members/<int:pk>/delete/', views.member_delete, name='member_delete'),
    

    path('jobs/', views.job_list, name='job_list'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/update/', views.job_update, name='job_update'),
    path('jobs/<int:pk>/delete/', views.job_delete, name='job_delete'),
    
  
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:pk>/update/', views.appointment_update, name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    
 
    path('job-applications/', views.job_application_list, name='job_application_list'),
    path('job-applications/create/', views.job_application_create, name='job_application_create'),
    path('job-applications/<int:caregiver_id>/<int:job_id>/', views.job_application_detail, name='job_application_detail'),
    path('job-applications/<int:caregiver_id>/<int:job_id>/delete/', views.job_application_delete, name='job_application_delete'),
    path("job-applications/<int:caregiver_id>/<int:job_id>/update/", views.job_application_update, name="job_application_update",),
  
    path("addresses/", views.address_list, name="address_list"),
    path("addresses/create/", views.address_create, name="address_create"),
    path("addresses/<int:pk>/", views.address_detail, name="address_detail"),
    path("addresses/<int:pk>/update/", views.address_update, name="address_update"),
    path("addresses/<int:pk>/delete/", views.address_delete, name="address_delete"),

]