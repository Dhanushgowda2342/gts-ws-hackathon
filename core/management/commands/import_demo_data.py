import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import TariffData, ShippingRoute, MarketData

class Command(BaseCommand):
    help = 'Import demo data from CSV files for GTS-WS'

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        data_dir = os.path.join(base_dir, 'data')
        
        self.stdout.write(self.style.WARNING('🗑️  Clearing existing data...'))
        TariffData.objects.all().delete()
        ShippingRoute.objects.all().delete()
        MarketData.objects.all().delete()
        
        # Import Tariffs
        self.stdout.write(self.style.SUCCESS('\n📊 Importing Tariff Data...'))
        tariff_file = os.path.join(data_dir, 'tariffs.csv')
        with open(tariff_file, 'r') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                TariffData.objects.create(
                    country_from=row['country_from'],
                    country_to=row['country_to'],
                    sector=row['sector'],
                    tariff_rate=float(row['tariff_rate']),
                    effective_date=datetime.strptime(row['effective_date'], '%Y-%m-%d').date()
                )
                count += 1
            self.stdout.write(f'   ✅ Imported {count} tariff records')
        
        # Import Shipping Routes
        self.stdout.write(self.style.SUCCESS('\n🚢 Importing Shipping Routes...'))
        shipping_file = os.path.join(data_dir, 'shipping_routes.csv')
        with open(shipping_file, 'r') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                ShippingRoute.objects.create(
                    route_name=row['route_name'],
                    status=row['status'],
                    freight_cost_index=float(row['freight_cost_index'])
                )
                count += 1
            self.stdout.write(f'   ✅ Imported {count} shipping routes')
        
        # Import Market Data
        self.stdout.write(self.style.SUCCESS('\n📈 Importing Market Data...'))
        market_file = os.path.join(data_dir, 'market_data.csv')
        with open(market_file, 'r') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                MarketData.objects.create(
                    symbol=row['symbol'],
                    sector=row['sector'],
                    price_change_7d=float(row['price_change_7d']),
                    date=datetime.strptime(row['date'], '%Y-%m-%d').date()
                )
                count += 1
            self.stdout.write(f'   ✅ Imported {count} market data records')
        
        self.stdout.write(self.style.SUCCESS('\n✨ Demo data import complete!'))

