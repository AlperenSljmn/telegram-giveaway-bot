# Giveaway Telegram Bot

This is a Python-based Telegram bot that allows users to participate in giveaways, and provides administrative control for managing the giveaways and sending promotional messages. The bot integrates with Google Sheets for storing user information and logging activity.

## Features

- **Create Giveaways**: Admins can create giveaways with a title, duration, and reward.
- **Join Giveaways**: Users can enter active giveaways by using the `/enter` command.
- **Pick Winner**: Admins can randomly pick a winner from the list of participants.
- **Send Promotional Messages**: Admins can send promotional messages to all registered users.
- **User Registration**: Users are automatically registered when they use the `/start` command, and their information is logged in Google Sheets.
- **List Active Giveaways**: Users can view all active giveaways with the `/list_giveaways` command.

## Requirements

- Python 3.x
- Telegram Bot API
- Google Sheets API credentials
- `python-dotenv` for environment variable management
- Libraries:
  - `pyTelegramBotAPI` (for bot functionality)
  - `gspread` (for Google Sheets integration)
  - `oauth2client` (for Google Sheets API authentication)
  - `python-dotenv` (for loading environment variables)
  
To install the required libraries, use:
```bash
pip install telebot gspread oauth2client python-dotenv
```

## Setup

1. **Create a Telegram Bot**:
   - Start a conversation with [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
   - Use `/newbot` to create a new bot and get the **BOT_TOKEN**.
   
2. **Google Sheets Setup**:
   - Create a Google Sheets document for storing users and giveaway data.
   - Share the sheet with the service account email generated in the next step.
   - Set up Google Sheets API and create service account credentials by following [this guide](https://gspread.readthedocs.io/en/latest/oauth2.html).
   - Save the service account JSON file (this will be used for API authentication).

3. **Configure Environment Variables**:
   - Create a `.env` file in the project root and define the following variables:
     ```env
     BOT_TOKEN=your_telegram_bot_token
     YOUR_ADMIN_ID=your_telegram_admin_user_id
     GOOGLE_CREDENTIALS_PATH=path_to_your_google_credentials.json
     ```
   
4. **Run the Bot**:
   - After setting up the `.env` file and installing the dependencies, run the bot using:
     ```bash
     python bot.py
     ```

## Commands

- `/create_giveaway <title> <duration_in_minutes> <reward>`: Admin command to create a new giveaway.
- `/enter`: Allows users to enter the ongoing giveaway in the chat.
- `/pick_winner`: Admin command to pick a winner for the ongoing giveaway.
- `/send_promo`: Admin command to send a promotional message to all registered users.
- `/start`: Registers the user in the Google Sheet.
- `/list_giveaways`: Lists all active giveaways.

## Code Overview

### 1. **Bot Initialization**
- The bot is initialized using `telebot.TeleBot` with the `BOT_TOKEN` provided in the environment file.

### 2. **Google Sheets Integration**
- The bot uses `gspread` and `oauth2client` to interact with Google Sheets.
- The bot logs user registrations and tracks giveaways in Google Sheets.

### 3. **Giveaway Management**
- The bot allows admins to create giveaways, store participants, and pick winners randomly.

### 4. **User Management**
- New users are automatically registered in the Google Sheets document when they use `/start`.
  
### 5. **Admin Commands**
- Admin commands include creating giveaways, picking winners, and sending promotional messages.

### 6. **Polling**
- The bot runs using `bot.polling(none_stop=True)`, keeping it active and ready to receive commands.

## Environment Variable Details

- **BOT_TOKEN**: Your Telegram bot's API token, provided by [BotFather](https://core.telegram.org/bots#botfather).
- **YOUR_ADMIN_ID**: Your Telegram user ID, which grants admin privileges. This ensures that only authorized users can create giveaways or send promotional messages.
- **GOOGLE_CREDENTIALS_PATH**: Path to your Google Sheets API credentials JSON file. This file allows the bot to interact with Google Sheets.

## Troubleshooting

- **Bot not responding**: Ensure the bot token is correct and the bot has access to the necessary permissions.
- **Google Sheets API errors**: Verify that the credentials are correct and the bot has access to the Google Sheet.
- **Missing library errors**: Ensure all dependencies are installed using `pip install telebot gspread oauth2client python-dotenv`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

For any issues or enhancements, feel free to open an issue or pull request!
