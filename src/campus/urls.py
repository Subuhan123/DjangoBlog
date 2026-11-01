from django.urls import path
from . import views

app_name = 'campus'

urlpatterns = [
    path('clubs/', views.club_list, name='club_list'),
    path('activities/', views.activity_list, name='activity_list'),
    path('activity/<int:pk>/', views.activity_detail, name='activity_detail'),
    path('activity/<int:pk>/signup/', views.activity_signup, name='activity_signup'),

]
