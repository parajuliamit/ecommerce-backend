from django.urls import path
from base.views import order_views as views

urlpatterns = [
    path('confirm/', views.addOrderItems, name='new-order'),
    path('history/', views.getOrders, name='get-orders'),
    path('<str:pk>/', views.getOrderDetail, name='order-details'),
]
