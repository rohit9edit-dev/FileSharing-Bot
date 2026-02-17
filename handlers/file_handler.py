from telegram import Update
from telegram.ext import ContextTypes
from config import Config
from database import db
from force_join import check_force_join, get_force_join_keyboard

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message

    # Check Ban
    if await db.is_banned(user_id):
        return

    # Check Force Join
    is_member = await check_force_join(context.bot, user_id)
    if not is_member:
        keyboard = await get_force_join_keyboard()
        await message.reply_text(
            "⚠️ **You must join both channels to use this bot.**",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        return

    # Identify File Type and ID
    file_id = None
    file_type = None

    if message.document:
        file_id = message.document.file_id
        file_type = 'document'
    elif message.video:
        file_id = message.video.file_id
        file_type = 'video'
    elif message.photo:
        file_id = message.photo[-1].file_id # Get highest resolution
        file_type = 'photo'
    elif message.audio:
        file_id = message.audio.file_id
        file_type = 'audio'
    
    if not file_id:
        await message.reply_text("❌ Unsupported file type.")
        return

    # Forward to Storage Channel
    try:
        await context.bot.copy_message(
            chat_id=Config.STORAGE_CHANNEL_ID,
            from_chat_id=message.chat_id,
            message_id=message.message_id
        )
    except Exception as e:
        await message.reply_text(f"❌ Storage Error: {str(e)}")
        return

    # Save to Database
    unique_id = await db.save_file(file_id, file_type, user_id)
    
    if unique_id:
        # Construct Link
        bot_info = await context.bot.get_me()
        link = f"https://t.me/{bot_info.username}?start={unique_id}"
        
        await message.reply_text(
            f"✅ **File Stored Successfully!**\n\n"
            f"🔗 **Link:** `{link}`\n\n"
            f"Click to share or download.",
            parse_mode='Markdown'
        )
    else:
        await message.reply_text("❌ Failed to save file info.")
