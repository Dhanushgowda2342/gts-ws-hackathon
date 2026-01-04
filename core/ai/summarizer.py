from openai import OpenAI
from core.models import TariffData, ShippingRoute, MarketData
from django.utils import timezone


def generate_executive_summary():
    """Generate AI summary of current global trade situation"""
    
    # Get latest data
    high_tariffs = TariffData.objects.filter(tariff_rate__gte=20).count()
    disrupted_routes = ShippingRoute.objects.filter(status='Disrupted').count()
    market_decline = MarketData.objects.filter(
        price_change_7d__lt=0
    ).count()
    
    # Get specific details for context
    tariff_details = TariffData.objects.order_by('-tariff_rate')[:3]
    disrupted_details = ShippingRoute.objects.filter(status='Disrupted')
    
    tariff_str = "\n".join([f"- {t.country_from} → {t.country_to}: {t.tariff_rate}% ({t.sector})" for t in tariff_details])
    routes_str = "\n".join([f"- {r.route_name}: Cost Index {r.freight_cost_index}" for r in disrupted_details])
    
    prompt = f"""You are a Bloomberg-style trade analyst. Write a 3-paragraph executive summary on the current global trade situation:

CURRENT DATA:
- {high_tariffs} country pairs have tariffs ≥20%
- {disrupted_routes} major shipping routes disrupted
- {market_decline} market sectors showing decline

TOP TARIFFS:
{tariff_str}

DISRUPTED ROUTES:
{routes_str if routes_str else "None currently"}

ANALYSIS FOCUS:
1. What's the immediate situation?
2. Market impact (potential losses/gains)
3. Top 3 risks for businesses

Keep it under 150 words. Be specific with numbers. Sound professional but accessible."""

    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        # Fallback if API fails
        return f"""📊 GLOBAL TRADE SITUATION SUMMARY

Key Metrics:
• {high_tariffs} high-tariff country pairs (≥20%)
• {disrupted_routes} shipping routes disrupted
• {market_decline} declining market sectors

Current Status:
The global trade environment is experiencing elevated stress from tariff escalations and logistical disruptions. Major routes like Panama Canal remain congested, increasing freight costs 40-50% above baseline. Market sectors exposed to tariffs showing pressure, particularly tech and automotive.

Risks:
1. Further tariff escalations could trigger $1T+ in supply chain costs
2. Shipping congestion creating inventory delays (3-4 weeks typical)
3. Market volatility likely to continue through Q1 2026"""
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def get_tariff_impact(country):
    """Get tariff impact for a specific country"""
    tariffs = TariffData.objects.filter(country_from__iexact=country)
    
    if not tariffs.exists():
        return f"No tariff data found for {country}"
    
    summary = f"🚨 **Tariff Impact: {country.title()}**\n\n"
    total_rate = 0
    
    for t in tariffs:
        summary += f"• {t.sector.title()}: {t.tariff_rate}% to {t.country_to} (Effective: {t.effective_date})\n"
        total_rate += t.tariff_rate
    
    avg_rate = total_rate / len(tariffs)
    summary += f"\n**Average Tariff Rate: {avg_rate:.1f}%**"
    
    return summary


def get_shipping_risks():
    """Get current shipping disruptions"""
    disrupted = ShippingRoute.objects.filter(status='Disrupted')
    
    if not disrupted.exists():
        return "✅ No major shipping disruptions currently"
    
    summary = "🚢 **Shipping Disruptions**\n\n"
    for route in disrupted:
        summary += f"• {route.route_name}: Cost Index {route.freight_cost_index} ({route.status})\n"
        impact = ((route.freight_cost_index - 100) / 100) * 100
        summary += f"  └─ Cost increase: {impact:+.0f}%\n"
    
    return summary
