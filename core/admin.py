from django.contrib import admin
from .models import TariffData, ShippingRoute, MarketData

@admin.register(TariffData)
class TariffDataAdmin(admin.ModelAdmin):
    list_display = ['country_from', 'country_to', 'sector', 'tariff_rate', 'effective_date']
    list_filter = ['sector', 'country_from', 'country_to']
    search_fields = ['country_from', 'country_to', 'sector']

@admin.register(ShippingRoute)
class ShippingRouteAdmin(admin.ModelAdmin):
    list_display = ['route_name', 'status', 'freight_cost_index', 'last_updated']
    list_filter = ['status']
    search_fields = ['route_name']

@admin.register(MarketData)
class MarketDataAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'sector', 'price_change_7d', 'date']
    list_filter = ['sector', 'date']
    search_fields = ['symbol', 'sector']
