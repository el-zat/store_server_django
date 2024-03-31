from django.urls import path

from purchases.views import PurchaseCreateView, SuccessTemplateView, CancelledTemplateView

app_name = 'purchases'


urlpatterns = [
    path('place-order/', PurchaseCreateView.as_view(), name='place-order'),
    path('purchases/', PurchaseCreateView.as_view(), name='purchases'),
    path('order-success/', SuccessTemplateView.as_view(), name='order-success'),
    path('order-cancelled/', CancelledTemplateView.as_view(), name='order-cancelled'),
]