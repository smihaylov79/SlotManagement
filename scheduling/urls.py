from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('book/', views.book_slot, name="book_slot"),
    path('overview/', views.schedule_overview, name="schedule_overview"),
    path('master/', views.master_data, name="master_data"),
]
