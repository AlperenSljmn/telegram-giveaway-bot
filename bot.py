import telebot
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Initialize your bot with the token from BotFather
BOT_TOKEN = '7867045562:AAHdirpHihP_Juuk9RssYQe1FYZfw2Hmzm8'
bot = telebot.TeleBot(BOT_TOKEN)
YOUR_ADMIN_ID = 1931616426
# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\alper\\Desktop\\deneme1-440820-d48c8f300450.json", scope)

client = gspread.authorize(creds)

# Access your Google Sheet
sheet = client.open("denemem").sheet1

# Dictionary to store ongoing giveaways
giveaways = {}

# Command to create a giveaway (admin-only)
@bot.message_handler(commands=['create_giveaway'])
def create_giveaway(message):
    # Check if user is admin
    admin_id = message.from_user.id
    if admin_id != YOUR_ADMIN_ID:
        bot.reply_to(message, "You are not authorized to create giveaways.")
        return
    
    # Create a new giveaway entry
    giveaways[message.chat.id] = {
        "title": "Sample Giveaway",
        "duration": 10, # Duration in minutes
        "participants": []
    }
    bot.reply_to(message, "Giveaway created! Use /enter to participate.")

# Command to join a giveaway
@bot.message_handler(commands=['enter'])
def enter_giveaway(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # Check if a giveaway exists
    if chat_id not in giveaways:
        bot.reply_to(message, "No active giveaway.")
        return
    
    # Register the participant
    if user_id not in giveaways[chat_id]["participants"]:
        giveaways[chat_id]["participants"].append((user_id, username))
        bot.reply_to(message, f"{username}, you are now entered in the giveaway!")
    else:
        bot.reply_to(message, "You have already entered the giveaway.")

# Command to randomly choose a winner
@bot.message_handler(commands=['pick_winner'])
def pick_winner(message):
    chat_id = message.chat.id
    
    # Check if giveaway exists and if there are participants
    if chat_id not in giveaways or not giveaways[chat_id]["participants"]:
        bot.reply_to(message, "No active giveaway or no participants.")
        return

    # Select a random winner
    winner = random.choice(giveaways[chat_id]["participants"])
    bot.send_message(chat_id, f"🎉 Congratulations {winner[1]}! You won the giveaway!")

    # Reset giveaway after winner is chosen
    del giveaways[chat_id]

# Command to send promotional message
@bot.message_handler(commands=['send_promo'])
def send_promo(message):
    # Check if user is admin
    if message.from_user.id != YOUR_ADMIN_ID:
        bot.reply_to(message, "You are not authorized to send promotional messages.")
        return
    
    promo_message = "Check out our latest updates!"
    user_ids = sheet.col_values(1)  # Assuming the user IDs are stored in the first column
    successful, failed = 0, 0

    for user_id in user_ids:
        try:
            bot.send_message(user_id, promo_message)
            successful += 1
        except Exception:
            failed += 1
    
    # Log results in a new sub-sheet
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_sheet = client.open("GiveawayBot").add_worksheet(title=f"Promo_Log_{now}", rows="100", cols="3")
    log_sheet.append_row(["Timestamp", "Successful", "Failed"])
    log_sheet.append_row([now, successful, failed])

    bot.reply_to(message, f"Promotional message sent. Success: {successful}, Failed: {failed}.")

# Command to register users on start
@bot.message_handler(commands=['start'])
def start_bot(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    # Log user in Google Sheets if they haven't started before
    existing_users = sheet.col_values(1)
    if str(user_id) not in existing_users:
        sheet.append_row([user_id, username])
        bot.reply_to(message, "Welcome! You've been added to the list.")
    else:
        bot.reply_to(message, "You're already registered!")

# Polling to keep the bot running
bot.polling(none_stop=True)
