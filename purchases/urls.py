from django.urls import path

from purchases.views import PurchaseCreateView

app_name = 'orders'


urlpatterns = [
    path('place-order/', PurchaseCreateView.as_view(), name='place-order'),

]