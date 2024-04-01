from django.contrib import admin

from service.models import Reason, Payment, Collect


@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'user', 'payment_date',)
    list_display_links = ('id', 'amount', 'user', 'payment_date',)
    search_fields = ('id', 'amount', 'user', 'payment_date',)


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'goal',)
    list_display_links = ('id', 'author', 'title',)
    readonly_fields = ('current_amount', 'users_count',)
    search_fields = ('id', 'author', 'title',)
