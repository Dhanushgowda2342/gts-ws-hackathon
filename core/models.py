from django.db import models

class TariffData(models.Model):
    """Tracks tariff rates between countries by sector"""
    country_from = models.CharField(max_length=100, help_text="Exporting country")
    country_to = models.CharField(max_length=100, help_text="Importing country")
    sector = models.CharField(max_length=100, help_text="Industry sector")
    tariff_rate = models.FloatField(help_text="Tariff percentage")
    effective_date = models.DateField(help_text="When tariff takes effect")
    
    class Meta:
        verbose_name = "Tariff Data"
        verbose_name_plural = "Tariff Data"
        ordering = ['-effective_date', '-tariff_rate']
    
    def __str__(self):
        return f"{self.country_from} → {self.country_to}: {self.tariff_rate}% ({self.sector})"

class ShippingRoute(models.Model):
    """Tracks major shipping routes and their status"""
    STATUS_CHOICES = [
        ('Normal', 'Normal'),
        ('Disrupted', 'Disrupted'),
        ('Blocked', 'Blocked'),
    ]
    
    route_name = models.CharField(max_length=200, help_text="Route description")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Normal')
    freight_cost_index = models.FloatField(default=100.0, help_text="100 = baseline")
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Shipping Route"
        verbose_name_plural = "Shipping Routes"
        ordering = ['route_name']
    
    def __str__(self):
        return f"{self.route_name} - {self.status} (Index: {self.freight_cost_index})"

class MarketData(models.Model):
    """Tracks market/stock performance by sector"""
    symbol = models.CharField(max_length=20, help_text="Stock/ETF symbol")
    sector = models.CharField(max_length=100, help_text="Market sector")
    price_change_7d = models.FloatField(help_text="7-day price change %")
    date = models.DateField(help_text="Data date")
    
    class Meta: 
        verbose_name = "Market Data"
        verbose_name_plural = "Market Data"
        ordering = ['-date', 'symbol']
    
    def __str__(self):
        return f"{self.symbol} ({self.sector}): {self.price_change_7d:+.2f}%"
