from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from purchases.forms import PurchaseForm
from store.common.views import TitleMixin


# Create your views here.

class PurchaseCreateView(TitleMixin, CreateView):
    template_name = 'purchases/place-order.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('purchases:place-order')
    title = 'Place order'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(PurchaseCreateView, self).form_valid(form)

