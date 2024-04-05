from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from products.models import Basket
from purchases.forms import PurchaseForm
from purchases.models import Purchase
from store.common.views import TitleMixin

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'purchases/success.html'
    title = 'Successful order'


class CancelledTemplateView(TemplateView):
    template_name = 'purchases/cancelled.html'


class PurchaseListView(TitleMixin, ListView):
    template_name = 'purchases/purchases.html'
    title = 'Orders'
    queryset = Purchase.objects.all()
    ordering = ['id']

    def get_queryset(self):
        queryset = super(PurchaseListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class PurchaseDetailView(DetailView):
    template_name = 'purchases/purchase.html'
    model = Purchase

    def get_context_data(self, **kwargs):
        context = super(PurchaseDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Order # {self.object.id}'
        return context


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
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='subscription',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('purchases:order-success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('purchases:order-cancelled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(PurchaseCreateView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Purchase.objects.get(id=order_id)
    order.update_after_payment()
