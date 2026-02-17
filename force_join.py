from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config

async def check_force_join(bot, user_id):
    """
    Returns True if user joined both channels, False otherwise.
    """
    channels = [Config.CHANNEL_1, Config.CHANNEL_2]
    
    for channel in channels:
        if not channel:
            continue
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            # Status must be member, administrator, or creator
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception:
            # Bot might not be admin in channel or channel is private/invalid
            return False
    return True

async def get_force_join_keyboard():
    """
    Generates the inline keyboard for force join.
    """
    keyboard = [
        [InlineKeyboardButton("Join Channel 1", url=f"https://t.me/{Config.CHANNEL_1.replace('@', '')}")],
        [InlineKeyboardButton("Join Channel 2", url=f"https://t.me/{Config.CHANNEL_2.replace('@', '')}")],
        [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")]
    ]
    return InlineKeyboardMarkup(keyboard)
