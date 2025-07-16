import telebot
import os
import csv
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

ORDER_FILE = "orders.csv"

user_states = {}

def save_order(username, service, details, video_link):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ORDER_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([time_now, username, service, details, video_link])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_states[message.chat.id] = "greeting"
    bot.reply_to(message,
        "Hey there! 👋\n"
        "Welcome to **Off Studios** 🎥\n"
        "We’re excited to help you transform your raw videos into professional content with a story-driven approach.\n\n"
        "Would you like to know about the services we offer?\n"
        "Just type **yes** to continue."
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.lower()
    username = message.from_user.username or message.from_user.first_name

    if chat_id not in user_states:
        user_states[chat_id] = "greeting"

    state = user_states[chat_id]

    if state == "greeting":
        if "yes" in text:
            user_states[chat_id] = "service_selection"
            bot.reply_to(message,
                "Awesome! Here's what we can do for you at **Off Studios**:\n\n"
                "1️⃣ **Vlog Editing** – For Instagram, Food Vlogs, and Promotion Vlogs 🍔🎥\n"
                "2️⃣ **Instagram Reels** – Trendy, viral-style edits under 30 sec 📱\n"
                "3️⃣ **Event Videos** – Weddings, Birthdays, Business Events & Stage Programs 🎉\n"
                "4️⃣ **YouTube Video Editing** – Long-form content with premium storytelling 📺\n\n"
                "Which one do you need help with?\n"
                "Please type: **vlog**, **reel**, **event**, or **youtube**"
            )
        else:
            bot.reply_to(message,
                "No worries! Whenever you're ready, just type **yes** to learn about our services."
            )

    elif state == "service_selection":
        if text == "vlog":
            user_states[chat_id] = "waiting_for_vlog_video"
            bot.reply_to(message,
                "Perfect! Our **Vlog Editing service** is specially designed for Instagram creators.\n\n"
                "**We mainly focus on:**\n"
                "🍔 **Food Vlogs** – Highlight the flavors with smooth edits\n"
                "📢 **Promotion Vlogs** – Promote your product or brand with engaging cuts\n\n"
                "Here’s what you’ll get:\n"
                "✅ Smooth Transitions\n"
                "✅ Audio Sync & Perfect Cuts\n"
                "✅ Slow Motion Highlights\n"
                "✅ Subtitles (optional)\n"
                "✅ Thumbnail Assistance\n"
                "✅ Sound Effects & Storytelling Focus\n"
                "✅ Cinematic Color Correction\n"
                "✅ 2 Free Revisions\n"
                "🚀 **Delivery: 1 Day**\n\n"
                "**Price:** ₹700–₹1000 depending on complexity.\n\n"
                "Please send your **Google Drive/Dropbox link** for best quality.\n"
                "Or send your video here as **file/document** (not as normal video)."
            )

        elif text == "reel":
            user_states[chat_id] = "waiting_for_reel_video"
            bot.reply_to(message,
                "For **Instagram Reels**, we create high-energy, trendy edits to help your content go viral! 📈\n\n"
                "🎵 **Trending Music** with **Perfect Sync**\n"
                "🌀 **Motion Blur & Speed Ramp** for cinematic flow\n"
                "🎨 **Color Correction** for an engaging look\n"
                "🖋️ **Malayalam Captions** (optional)\n"
                "⏱️ **Under 30 sec**, fully engaging\n"
                "💰 **Rate:** ₹300–₹500\n"
                "✅ **Delivery:** 1 Day\n\n"
                "Please send your **video link** or upload as **file/document**."
            )

        elif text == "event":
            user_states[chat_id] = "waiting_for_event_selection"
            bot.reply_to(message,
                "Awesome! We love creating event videos. Please choose the type of event:\n\n"
                "- **Wedding**: ₹1500–₹4000\n"
                "- **Birthday Event**: ₹1000–₹2000\n"
                "- **Business Event**: Affordable Pricing\n"
                "- **Stage Program**: Affordable Pricing\n\n"
                "After selecting the event type, please send your **Google Drive/Dropbox link** or send the video here as **file/document**."
            )

        elif text == "youtube":
            user_states[chat_id] = "waiting_for_youtube_video"
            bot.reply_to(message,
                "Our **YouTube Video Editing** service is perfect for long-form, story-driven content 📺\n\n"
                "✅ Creative Storytelling\n"
                "✅ Cinematic Color Correction\n"
                "✅ Audio Sync + Clean Cuts\n"
                "✅ Thumbnail (Optional)\n"
                "💰 **Rate:** ₹800–₹1500\n"
                "⏱️ **Delivery:** 2 Days\n\n"
                "Please send your **Google Drive/Dropbox link** or video as **file/document**."
            )

        else:
            bot.reply_to(message, 
                "Sorry, I didn’t get that. Please type: **vlog**, **reel**, **event**, or **youtube**."
            )

    elif state in ["waiting_for_vlog_video", "waiting_for_reel_video", "waiting_for_youtube_video", "waiting_for_event_selection"]:
        if "http" in text or "drive" in text or "dropbox" in text:
            service = state.replace("waiting_for_", "").replace("_video", "").replace("_selection", "")
            save_order(username, service, "Video Sent", text)
            user_states[chat_id] = "done"
            bot.reply_to(message,
                "✅ Got your video link! Thank you 🙌\n"
                "Our team will review your footage and start the editing process.\n\n"
                "For any urgent questions, feel free to contact us directly at **📞 9747184013**"
            )
        else:
            bot.reply_to(message,
                "Please send your **Google Drive/Dropbox link** or send the video here as **file/document**.\n"
                "We recommend sending **high-quality files** for the best results."
            )

    else:
        bot.reply_to(message, 
            "If you’d like to start again, type **/start**"
        )

print("🤖 Bot is running...")
bot.polling()
