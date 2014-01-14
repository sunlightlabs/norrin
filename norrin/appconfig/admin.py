from django.contrib import admin
from norrin.appconfig.models import Client, Configuration, Load


class ClientAdmin(admin.ModelAdmin):
    list_display = ('key', 'name', 'email')
    readonly_fields = ('key',)


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('key', 'description', 'enabled')
    readonly_fields = ('key',)


class LoadAdmin(admin.ModelAdmin):
    list_display = ('configuration', 'client', 'user_agent', 'timestamp')
    readonly_fields = ('timestamp',)


admin.site.register(Client, ClientAdmin)
admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Load, LoadAdmin)
