from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from core.ai.summarizer import generate_executive_summary, get_tariff_impact, get_shipping_risks

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def slack_events(request):
    """Handle Slack events (url_verification, messages, etc.)"""
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Slack URL verification
    if body.get('type') == 'url_verification':
        return JsonResponse({'challenge': body.get('challenge')})
    
    # Handle events
    if body.get('type') == 'event_callback':
        event = body.get('event', {})
        if event.get('type') == 'app_mention':
            handle_mention(event)
    
    return JsonResponse({'ok': True})


def handle_mention(event):
    """Handle @gts-ws mentions in Slack"""
    text = event.get('text', '').lower()
    channel = event.get('channel')
    user = event.get('user')
    
    response = None
    
    if 'summarize' in text:
        response = generate_executive_summary()
        send_slack_message(channel, f"📊 **AI Executive Summary**\n\n{response}")
    
    elif 'tariff impact' in text:
        # Extract country from message: "@gts-ws tariff impact china"
        words = text.split()
        country = None
        if 'impact' in words:
            idx = words.index('impact')
            if idx + 1 < len(words):
                country = words[idx + 1]
        
        if country:
            response = get_tariff_impact(country)
            send_slack_message(channel, response)
        else:
            send_slack_message(channel, "⚠️ Please specify a country: `@gts-ws tariff impact china`")
    
    elif 'shipping risk' in text:
        response = get_shipping_risks()
        send_slack_message(channel, response)
    
    elif 'help' in text:
        help_text = """🤖 **GTS-WS Commands**

• `@gts-ws summarize` - AI executive summary
• `@gts-ws tariff impact [country]` - Tariff details (e.g., china, mexico)
• `@gts-ws shipping risk` - Current disruptions
• `@gts-ws help` - This message"""
        send_slack_message(channel, help_text)
    
    else:
        send_slack_message(
            channel,
            "Try: `@gts-ws help` for available commands"
        )


def send_slack_message(channel, text, image_url=None):
    """Send message to Slack channel"""
    # This is a placeholder - in production, use slack_sdk
    # from slack_sdk import WebClient
    # client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
    # client.chat_postMessage(channel=channel, text=text)
    logger.info(f"Sending to Slack #{channel}: {text[:100]}...")
