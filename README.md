# Telegram File Sharing Bot

A professional, modular Telegram bot for storing and sharing files with a Force Join subscription system.

## Features
- ✅ **Force Join System**: Users must join 2 channels to use the bot.
- ✅ **Private Storage**: Files are forwarded to a private channel.
- ✅ **Shareable Links**: Generates short links (`t.me/bot?start=id`).
- ✅ **Admin Panel**: Stats, Broadcast, Ban/Unban users.
- ✅ **Database**: SQLite for persistent storage.
- ✅ **Security**: Banned user check, Admin validation.

## Prerequisites
- Python 3.10 or higher
- Telegram Bot Token (from BotFather)
- 2 Public Channels (for Force Join)
- 1 Private Channel (for Storage)

## Setup Guide

### 1. Create Bot (BotFather)
1. Open Telegram and search for **@BotFather**.
2. Send `/newbot`.
3. Name your bot (e.g., `MyFileBot`).
4. Set username (must end in `bot`, e.g., `my_share_bot`).
5. Copy the **API Token**.

### 2. Setup Channels
1. **Channel 1 & 2 (Force Join)**:
   - Create two public channels.
   - Add your bot as an **Administrator** (to verify membership).
   - Copy their usernames (e.g., `@ChannelOne`).
2. **Storage Channel**:
   - Create a **Private** channel.
   - Add your bot as an **Administrator**.
   - Forward a message from this channel to **@JsonDumpBot** or similar to get the `ID` (e.g., `-100123456789`).

### 3. Installation
```bash
# Clone or download files
cd telegram_file_bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure .env
# Edit .env file and add your Token, Admin ID, and Channel IDs
