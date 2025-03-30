📰 WhatsApp News Bot using Twilio API
This project is a WhatsApp chatbot that delivers daily news updates and allows users to request the latest news anytime. Built using Flask, Twilio API, and NewsAPI, this bot fetches top headlines based on the user's preferred country and sends them via WhatsApp.

📌 Features
✅ Daily News Updates – Sends top news headlines every day at 9 AM.
✅ On-Demand News – Users can request the latest news by sending news.
✅ Country-Specific News – Users can set their preferred country for relevant news.
✅ Subscribe/Unsubscribe – Users can opt-in or opt-out anytime.
✅ Twilio WhatsApp API – Uses Twilio to send & receive WhatsApp messages.

🛠 Tech Stack
Python (Flask) – Web framework for handling requests.

Twilio API – For sending and receiving WhatsApp messages.

NewsAPI – Fetches real-time news headlines.

APScheduler – Schedules daily news updates.

⚙️ How to Set Up
1️⃣ Install Dependencies
pip install flask twilio requests apscheduler pyngrok

2️⃣ Configure Twilio
Sign up at Twilio

Activate WhatsApp Sandbox

Get Twilio Account SID, Auth Token, and WhatsApp Number

3️⃣ Set Environment Variables
export TWILIO_ACCOUNT_SID="your_account_sid"
export TWILIO_AUTH_TOKEN="your_auth_token"
export TWILIO_WHATSAPP_NUMBER="whatsapp:+your_twilio_number"
export NEWS_API_KEY="your_newsapi_key"

4️⃣ Run the Bot
news_bot.py

5️⃣ Expose Flask Server Using ngrok
ngrok http 5000

📝 Commands Users Can Send
news – Get the latest news.

subscribe – Get daily news updates.

unsubscribe – Stop receiving daily updates.

India, USA, UK – Set news country preference.

🚀 Future Enhancements
🔹 Add AI-based news summarization.
🔹 Support for multiple languages.
🔹 Deploy on Heroku / AWS for 24/7 availability.
