from django.urls import path
from . import views

urlpatterns = [
    path('', views.records_list, name='records_list'),
    path('create/', views.create_record, name='create_record'),
    path('update/<int:record_id>/', views.update_record, name='update_record'),
    path('delete/<int:record_id>/', views.delete_record, name='delete_record'),
]
