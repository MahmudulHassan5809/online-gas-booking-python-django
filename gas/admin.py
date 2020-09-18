from django.contrib import admin
from django.contrib.auth import get_user_model
from gas.models import Staff, Connection, Booking, GasReffiling
from gas.forms import StaffForm
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


class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'connection', 'address', 'mobile',
                    'reffiling', 'booking_number', 'status', 'staff', 'date']
    list_filter = ['status']
    search_fields = ('user__username', 'name', 'mobile')
    autocomplete_fields = ('user', 'staff', 'connection')
    list_editable = ['status', 'staff']

    def address(self, obj):
        return obj.connection.address

    def mobile(self, obj):
        return obj.connection.mobile


admin.site.register(Booking, BookingAdmin)
