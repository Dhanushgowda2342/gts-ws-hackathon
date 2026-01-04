from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import models
from core.ai.summarizer import generate_executive_summary
from core.models import TariffData, ShippingRoute, MarketData


def dashboard(request):
    """Render main dashboard page"""
    return render(
        request,
        'dashboard.html',
        {
            'dashboard_url': settings.TABLEAU_DASHBOARD_URL,
        },
    )


@require_http_methods(["GET"])
def executive_summary_api(request):
    """API endpoint for AI executive summary"""
    try:
        summary = generate_executive_summary()
        return JsonResponse({
            'summary': summary,
            'status': 'success'
        })
    except Exception as e:
        return JsonResponse({
            'summary': f'Error generating summary: {str(e)}',
            'status': 'error'
        }, status=500)


@require_http_methods(["GET"])
def kpi_data_api(request):
    """API endpoint for KPI dashboard data"""
    try:
        # Calculate KPIs
        tariff_records = TariffData.objects.all()
        avg_tariff = tariff_records.aggregate(models.Avg('tariff_rate'))['tariff_rate__avg'] or 0
        
        disrupted_routes = ShippingRoute.objects.filter(status='Disrupted').count()
        
        declining_sectors = MarketData.objects.filter(price_change_7d__lt=0).values('sector').distinct().count()
        
        return JsonResponse({
            'avg_tariff': avg_tariff,
            'disrupted_routes': disrupted_routes,
            'declining_sectors': declining_sectors,
            'status': 'success'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(["GET"])
def tariff_chart_data(request):
    """Get tariff data for charting"""
    try:
        country = request.GET.get('country', '').title()
        tariffs = TariffData.objects.filter(country_from=country).values('country_to', 'tariff_rate', 'sector')
        
        data = list(tariffs)
        return JsonResponse({
            'country': country,
            'data': data,
            'status': 'success'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(["GET"])
def tariffs_api(request):
    """List all tariff records"""
    data = list(
        TariffData.objects.values(
            'country_from', 'country_to', 'sector', 'tariff_rate', 'effective_date'
        )
    )
    return JsonResponse({'results': data})


@require_http_methods(["GET"])
def shipping_api(request):
    """List all shipping routes"""
    data = list(
        ShippingRoute.objects.values(
            'route_name', 'status', 'freight_cost_index', 'last_updated'
        )
    )
    return JsonResponse({'results': data})


@require_http_methods(["GET"])
def markets_api(request):
    """List all market data rows"""
    data = list(
        MarketData.objects.values(
            'symbol', 'sector', 'price_change_7d', 'date'
        )
    )
    return JsonResponse({'results': data})


@require_http_methods(["GET"])
def dashboard_api(request):
    """Dashboard aggregate data (same KPIs + summary)"""
    avg_tariff = TariffData.objects.aggregate(models.Avg('tariff_rate'))['tariff_rate__avg'] or 0
    disrupted_routes = ShippingRoute.objects.filter(status='Disrupted').count()
    declining_sectors = MarketData.objects.filter(price_change_7d__lt=0).values('sector').distinct().count()
    summary = generate_executive_summary()
    return JsonResponse({
        'avg_tariff': avg_tariff,
        'disrupted_routes': disrupted_routes,
        'declining_sectors': declining_sectors,
        'summary': summary,
    })
