from django.urls import path
from . import views

urlpatterns = [
    path('', views.billing_list, name='billing_list'),
    path('create/', views.create_billing, name='create_billing'),
    path('update/<int:billing_id>/', views.update_billing, name='update_billing'),
    path('delete/<int:billing_id>/', views.delete_billing, name='delete_billing'),
]
