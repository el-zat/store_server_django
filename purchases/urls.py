from django.urls import path

from purchases.views import PurchaseCreateView, SuccessTemplateView, CancelledTemplateView, PurchaseListView

app_name = 'purchases'


urlpatterns = [
    path('place-order/', PurchaseCreateView.as_view(), name='place-order'),
    path('order-success/', SuccessTemplateView.as_view(), name='order-success'),
    path('order-cancelled/', CancelledTemplateView.as_view(), name='order-cancelled'),
    path('', PurchaseListView.as_view(), name='orders_list'),
]