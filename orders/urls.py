
from django.urls import path

from orders.views import OrderCreateView, SuccessTemplateView, CancelledTemplateView

app_name = 'orders'


urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order-create'),
    path('order-success/', SuccessTemplateView.as_view(), name='order-success'),
    path('order-cancelled/', CancelledTemplateView.as_view(), name='order-cancelled'),
]
