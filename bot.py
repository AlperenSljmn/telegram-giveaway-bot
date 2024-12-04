import telebot
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Your bot token from .env
YOUR_ADMIN_ID = int(os.getenv("YOUR_ADMIN_ID"))  # Admin ID from .env
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")  # Path to Google credentials file from .env

# Initialize your bot
bot = telebot.TeleBot(BOT_TOKEN)

# Google Sheets setup
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_PATH, scope)  # Path from .env
client = gspread.authorize(creds)

# Access the Google Sheet
sheet = client.open("GiveAway").sheet1

# Dictionary to store ongoing giveaways
giveaways = {}

# Command: Create a giveaway (admin-only)
@bot.message_handler(commands=['create_giveaway'])
def create_giveaway(message):
    if message.from_user.id != YOUR_ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to create giveaways.")
        return
    
    # Parse the command: /create_giveaway <title> <duration_in_minutes> <reward>
    args = message.text.split(maxsplit=3)
    if len(args) < 4:
        bot.reply_to(message, "Usage: /create_giveaway <title> <duration_in_minutes> <reward>")
        return

    title = args[1]
    duration = int(args[2])
    reward = args[3]
    end_time = datetime.now().timestamp() + duration * 60  # Convert minutes to seconds

    giveaways[message.chat.id] = {
        "title": title,
        "end_time": end_time,
        "reward": reward,
        "participants": []
    }
    bot.reply_to(message, f"🎉 Giveaway '{title}' created! Reward: {reward}. Ends in {duration} minutes.\nUse /enter to participate.")

# Command: Join a giveaway
@bot.message_handler(commands=['enter'])
def enter_giveaway(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    if chat_id not in giveaways:
        bot.reply_to(message, "❌ No active giveaway in this chat.")
        return

    if user_id not in [p[0] for p in giveaways[chat_id]["participants"]]:
        giveaways[chat_id]["participants"].append((user_id, username))
        bot.reply_to(message, f"✅ {username}, you have successfully entered the giveaway!")
    else:
        bot.reply_to(message, "⚠️ You are already registered in this giveaway.")

# Command: Pick a winner
@bot.message_handler(commands=['pick_winner'])
def pick_winner(message):
    if message.from_user.id != YOUR_ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to pick winners.")
        return

    chat_id = message.chat.id

    if chat_id not in giveaways or not giveaways[chat_id]["participants"]:
        bot.reply_to(message, "❌ No active giveaway or no participants in this chat.")
        return

    winner = random.choice(giveaways[chat_id]["participants"])
    bot.send_message(chat_id, f"🎉 Congratulations {winner[1]}! You won the giveaway! Reward: {giveaways[chat_id]['reward']}")
    del giveaways[chat_id]  # Remove the giveaway after picking the winner

# Command: Send promotional messages
@bot.message_handler(commands=['send_promo'])
def send_promo(message):
    if message.from_user.id != YOUR_ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to send promotional messages.")
        return

    promo_message = "📢 Don't miss our latest updates and offers!"
    user_ids = sheet.col_values(1)  # Assuming user IDs are stored in the first column
    successful, failed = 0, 0

    for user_id in user_ids:
        try:
            bot.send_message(user_id, promo_message)
            successful += 1
        except Exception:
            failed += 1

    # Log the results in Google Sheets
    log_sheet = client.open("GiveAway").add_worksheet(title=f"Promo_Log_{datetime.now().strftime('%Y%m%d_%H%M%S')}", rows="100", cols="3")
    log_sheet.append_row(["Timestamp", "Successful", "Failed"])
    log_sheet.append_row([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), successful, failed])

    bot.reply_to(message, f"✅ Promotional message sent successfully.\nSuccess: {successful}, Failed: {failed}.")

# Command: Register user on /start
@bot.message_handler(commands=['start'])
def start_bot(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.first_name

    # Log user in Google Sheets if they aren't already registered
    existing_users = sheet.col_values(1)
    if user_id not in existing_users:
        sheet.append_row([user_id, username])
        bot.reply_to(message, "✅ Welcome! You have been registered.")
    else:
        bot.reply_to(message, "⚠️ You are already registered.")

# Command: List active giveaways
@bot.message_handler(commands=['list_giveaways'])
def list_giveaways(message):
    active_giveaways = []
    for chat_id, giveaway in giveaways.items():
        time_left = (giveaway["end_time"] - datetime.now().timestamp()) / 60
        if time_left > 0:
            active_giveaways.append(f"🎁 {giveaway['title']} - Reward: {giveaway['reward']} (Ends in {int(time_left)} minutes)")

    if active_giveaways:
        bot.reply_to(message, "\n".join(active_giveaways))
    else:
        bot.reply_to(message, "⚠️ No active giveaways right now.")

# Polling to keep the bot running
bot.polling(none_stop=True)
