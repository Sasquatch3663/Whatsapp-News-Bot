from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client

app = Flask(__name__)

# Twilio Credentials (Replace with your actual credentials)
TWILIO_ACCOUNT_SID = "Your TWILIO SID"
TWILIO_AUTH_TOKEN = "Your Auth_Token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:Your Whatsapp Mobile No."

# News API Key (Get from https://newsapi.org/)
NEWS_API_KEY = "Your API KEY"

# Default Country Code (INDIA)
DEFAULT_COUNTRY = "in"

# Country Preferences (Maps user phone numbers to their preferred country)
user_preferences = {}

# List of subscribers
subscribers = set()

# Country Name to Code Mapping (Expand as needed)
COUNTRY_CODES = {
    "india": "in", "usa": "us", "united states": "us",
    "uk": "gb", "united kingdom": "gb", "germany": "de",
    "france": "fr", "canada": "ca", "australia": "au"
}

def get_latest_news(country_code):
    """Fetches latest news based on the country code."""
    url = f"https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("articles", [])[:5]  # Get top 5 news articles
        news_text = f"📰 *Top News for {country_code.upper()}*\n\n"
        
        if not articles:
            return "⚠️ No news found for this country."

        for i, article in enumerate(articles, start=1):
            news_text += f"{i}. *{article['title']}*\n   {article['url']}\n\n"

        return news_text
    except Exception as e:
        return f"Error fetching news: {str(e)}"

def send_news_to_subscribers():
    """Sends daily news updates to all subscribed users based on their country preference."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    for subscriber in subscribers:
        country_code = user_preferences.get(subscriber, DEFAULT_COUNTRY)
        news_text = get_latest_news(country_code)

        client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=news_text,
            to=subscriber
        )

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """Handles incoming WhatsApp messages."""
    incoming_msg = request.values.get("Body", "").strip().lower()
    sender_number = request.values.get("From", "")

    response = MessagingResponse()
    message = response.message()

    if incoming_msg == "subscribe":
        subscribers.add(sender_number)
        message.body("✅ You have subscribed to daily news updates! Send your country name to get relevant news.")

    elif incoming_msg == "unsubscribe":
        subscribers.discard(sender_number)
        user_preferences.pop(sender_number, None)  # Remove country preference
        message.body("❌ You have unsubscribed from daily news updates.")

    elif incoming_msg == "news":
        country_code = user_preferences.get(sender_number, DEFAULT_COUNTRY)
        news_text = get_latest_news(country_code)
        message.body(news_text)

    elif incoming_msg in COUNTRY_CODES:
        user_preferences[sender_number] = COUNTRY_CODES[incoming_msg]
        message.body(f"🌍 Your preferred news country has been set to {incoming_msg.capitalize()}!")

    else:
        message.body(
            "🤖 Hello! Here’s what I can do:\n"
            "- Send 'news' to get the latest updates.\n"
            "- Send 'subscribe' to get daily news updates.\n"
            "- Send 'unsubscribe' to stop receiving updates.\n"
            "- Send your country name (e.g., 'USA', 'UK') to get relevant news."
        )

    return str(response)

# Scheduler to send daily news at 9 AM
scheduler = BackgroundScheduler()
scheduler.add_job(send_news_to_subscribers, "cron", hour=9, minute=0)
scheduler.start()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
