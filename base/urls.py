from django.urls import path
from base import views


urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('learn/<int:course_id>/', views.learn, name='learn'),
    path('lesson/<int:lesson_id>/', views.lesson, name='lesson'),
]