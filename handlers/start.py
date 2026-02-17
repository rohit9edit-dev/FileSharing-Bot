from telegram import Update
from telegram.ext import ContextTypes
from config import Config
from database import db
from force_join import check_force_join, get_force_join_keyboard

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # Check Ban
    if await db.is_banned(user_id):
        await update.message.reply_text("🚫 You are banned from using this bot.")
        return

    # Add User to DB
    await db.add_user(user_id, user.username)

    # Check for payload (File Retrieval)
    if context.args and context.args[0]:
        unique_id = context.args[0]
        await handle_file_retrieval(update, context, unique_id, user_id)
        return

    # Normal Start
    await update.message.reply_text(
        f"👋 Hello **{user.first_name}**!\n\n"
        "Send me any file (Document, Video, Photo, Audio) to generate a shareable link.",
        parse_mode='Markdown'
    )

async def handle_file_retrieval(update: Update, context: ContextTypes.DEFAULT_TYPE, unique_id: str, user_id: int):
    # 1. Check Force Join First
    is_member = await check_force_join(context.bot, user_id)
    
    if not is_member:
        keyboard = await get_force_join_keyboard()
        await update.message.reply_text(
            "⚠️ **You must join both channels to use this bot.**",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        return

    # 2. Fetch File
    file_data = await db.get_file(unique_id)
    
    if not file_
        await update.message.reply_text("❌ **Invalid or Expired Link.**", parse_mode='Markdown')
        return

    file_id, file_type = file_data
    
    # 3. Send File
    try:
        if file_type == 'document':
            await context.bot.send_document(chat_id=user_id, document=file_id)
        elif file_type == 'video':
            await context.bot.send_video(chat_id=user_id, video=file_id)
        elif file_type == 'photo':
            await context.bot.send_photo(chat_id=user_id, photo=file_id)
        elif file_type == 'audio':
            await context.bot.send_audio(chat_id=user_id, audio=file_id)
        else:
            await context.bot.send_document(chat_id=user_id, document=file_id)
            
        await update.message.reply_text("📂 File sent successfully!")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error sending file: {str(e)}")

async def callback_check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the 'I've Joined' button click"""
    user_id = update.effective_user.id
    query = update.callback_query
    await query.answer()

    is_member = await check_force_join(context.bot, user_id)
    
    if is_member:
        await query.edit_message_text("✅ **Verification Successful!**\n\nYou can now use the bot.", parse_mode='Markdown')
    else:
        keyboard = await get_force_join_keyboard()
        await query.edit_message_text(
            "⚠️ **Membership not detected.**\nPlease join both channels and try again.",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
