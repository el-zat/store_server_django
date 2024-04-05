from django.contrib import admin

from purchases.models import Purchase


# Register your models here.
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    fields = (
        'id', 'created',
        ('firstname', 'lastname'),
        ('email', 'address'),
        'basket_history',
        'status', 'initiator',
    )
    readonly_fields = ('id', 'created')
