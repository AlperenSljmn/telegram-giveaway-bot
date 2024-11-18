# Telegram Giveaway Bot

A Telegram bot that allows users to participate in giveaways, randomly selects winners, and sends promotional messages to users stored in a Google Sheet.

## Features

- **Create Giveaways**: Admin can create a giveaway for a specific chat.
- **Enter Giveaways**: Users can enter a giveaway with a `/enter` command.
- **Pick Winner**: Admin can pick a random winner using the `/pick_winner` command.
- **Send Promo Messages**: Admin can send promotional messages to all users listed in a Google Sheet.
- **User Registration**: New users are registered in the Google Sheet upon using the `/start` command.

## Prerequisites

- Python 3.x
- Telegram Bot Token (from [BotFather](https://core.telegram.org/bots#botfather))
- Google Sheets API credentials (service account JSON file)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/telegram-giveaway-bot.git
cd telegram-giveaway-bot
