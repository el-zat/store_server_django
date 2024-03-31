from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from orders.forms import OrderForm
from store.common.views import TitleMixin


# Create your views here.
class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order-create')
    title = 'Create order'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)



