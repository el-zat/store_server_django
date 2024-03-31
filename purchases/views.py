from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from purchases.forms import PurchaseForm
from store.common.views import TitleMixin
import stripe
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from http import HTTPStatus

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'purchases/success.html'
    title = 'Successful order'


class CancelledTemplateView(TemplateView):
    template_name = 'purchases/cancelled.html'


class PurchaseCreateView(TitleMixin, CreateView):
    template_name = 'purchases/place-order.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('purchases:place-order')
    title = 'Place order'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(PurchaseCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        super(PurchaseCreateView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1Oz0v3EZ0aTg4ftyXktQSIXU',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('purchases:order-success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('purchases:order-cancelled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)