from django.contrib import admin
from django.contrib.auth import get_user_model
from gas.models import Staff, Connection, Booking, GasReffiling, Stock
from gas.forms import StaffForm
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
# Register your models here.


User = get_user_model()


class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile', 'address']
    search_fields = ('mobile', 'address')
    # autocomplete_fields = ('user',)
    form = StaffForm

    # def render_change_form(self, request, context, *args, **kwargs):
    #     context['adminform'].form.fields['user'].queryset = User.objects.filter(
    #         is_staff=True)
    #     return super(StaffAdmin, self).render_change_form(request, context, *args, **kwargs)


admin.site.register(Staff, StaffAdmin)


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email', 'mobile', 'address', 'status']
    list_filter = ['status']
    search_fields = ('user__username', 'name', 'mobile')
    autocomplete_fields = ('user',)
    list_editable = ['status']


admin.site.register(Connection, ConnectionAdmin)


class GasReffilingAdmin(admin.ModelAdmin):
    list_display = ['reffiling_size', 'price']
    search_fields = ('reffiling_size', 'price',)
    list_editable = ['price']


admin.site.register(GasReffiling, GasReffilingAdmin)


class StockAdmin(admin.ModelAdmin):
    list_display = ['gas_reffiling', 'quantity']
    list_editable = ['quantity']
    list_per_page = 20


admin.site.register(Stock, StockAdmin)


def has_status_permission(request, obj=None):
    if request.user.has_perm('booking.can_change_status'):
        return True
    return False


class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'connection', 'address', 'mobile',
                    'reffiling', 'booking_number', 'status', 'staff', 'date']
    list_filter = ['status']
    search_fields = ('user__username', 'connection__name',
                     'connection__mobile')
    autocomplete_fields = ('user', 'staff', 'connection')
    list_editable = ['status', 'staff']

    def address(self, obj):
        return obj.connection.address

    def mobile(self, obj):
        return obj.connection.mobile

    @method_decorator(csrf_protect)
    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = list_display = ['user', 'connection', 'address', 'mobile',
                                                'reffiling', 'booking_number', 'status', 'staff', 'date']
            self.editable = ['status', 'staff']
            self.readonly_fields = ()
        else:
            self.list_display = ['user', 'connection', 'address', 'mobile',
                                 'reffiling', 'booking_number', 'status', 'date']
            self.editable = ['status']
            self.readonly_fields = ('user', 'connection', 'address',
                                    'mobile', 'reffiling', 'booking_number', 'staff', 'date')

        return super(BookingAdmin, self).changelist_view(request, extra_context)

    # def get_form(self, request, obj=None, **kwargs):
    #     if not request.user.is_superuser:
    #         self.fields = ['status']
    #     else:
    #         self.fields = ['user', 'connection', 'address', 'mobile',
    #                        'reffiling', 'status', 'staff']
    #     return super(BookingAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Booking, BookingAdmin)
