from django.contrib import admin
from gas.models import Staff, Connection
# Register your models here.


class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile', 'address']
    search_fields = ('mobile', 'address')
    autocomplete_fields = ('user',)


admin.site.register(Staff, StaffAdmin)


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email', 'mobile', 'address', 'status']
    list_filter = ['status']
    search_fields = ('user__username', 'name', 'mobile')
    autocomplete_fields = ('user',)
    list_editable = ['status']


admin.site.register(Connection, ConnectionAdmin)
