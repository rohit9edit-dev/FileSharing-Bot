from telegram import Update
from telegram.ext import ContextTypes
from config import Config
from database import db

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.ADMIN_ID:
        return
    
    users, files = await db.get_stats()
    await update.message.reply_text(
        f"📊 **Bot Statistics**\n\n"
        f"👥 Total Users: `{users}`\n"
        f"📁 Total Files: `{files}`",
        parse_mode='Markdown'
    )

async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.ADMIN_ID:
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /ban <user_id>")
        return
    
    try:
        target_id = int(context.args[0])
        await db.ban_user(target_id)
        await update.message.reply_text(f"✅ User `{target_id}` has been banned.", parse_mode='Markdown')
    except ValueError:
        await update.message.reply_text("❌ Invalid User ID.")

async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.ADMIN_ID:
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /unban <user_id>")
        return
    
    try:
        target_id = int(context.args[0])
        await db.unban_user(target_id)
        await update.message.reply_text(f"✅ User `{target_id}` has been unbanned.", parse_mode='Markdown')
    except ValueError:
        await update.message.reply_text("❌ Invalid User ID.")

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.ADMIN_ID:
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
    
    message_text = " ".join(context.args)
    users = await db.get_all_users()
    
    success = 0
    failed = 0
    
    status_msg = await update.message.reply_text(f"📢 Broadcasting to {len(users)} users...")
    
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=message_text)
            success += 1
        except Exception:
            failed += 1
        
        # Avoid FloodWait (Simple delay)
        import asyncio
        await asyncio.sleep(0.1)
        
    await status_msg.edit_text(
        f"✅ Broadcast Complete.\n"
        f"Sent: `{success}`\n"
        f"Failed: `{failed}`",
        parse_mode='Markdown'
    )
