

# Register your models here.
from django.contrib import admin

from .models import GatewayRoute,GatewayEndpoint,TargetURL



class GatewayRouteAdmin(admin.ModelAdmin):
    readonly_fields=('added_date',)
class GatewayEndpointAdmin(admin.ModelAdmin):
    readonly_fields=('added_date','updated_date')
class TargetURLAdmin(admin.ModelAdmin):
    readonly_fields=('added_date','updated_date')

admin.site.register(GatewayRoute,GatewayRouteAdmin)
admin.site.register(GatewayEndpoint,GatewayEndpointAdmin)
admin.site.register(TargetURL,TargetURLAdmin)