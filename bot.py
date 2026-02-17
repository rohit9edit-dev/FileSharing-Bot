import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import Config
from handlers import start, file_handler, admin

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    if not Config.BOT_TOKEN:
        raise ValueError("No BOT_TOKEN set in .env")

    # Build Application
    application = ApplicationBuilder().token(Config.BOT_TOKEN).build()

    # --- Handlers ---

    # Start Command (Handles /start and /start payload)
    application.add_handler(CommandHandler("start", start.start_command))
    
    # Callback Query (Force Join Check)
    application.add_handler(CallbackQueryHandler(start.callback_check_join, pattern="^check_join$"))

    # File Handler (Documents, Photos, Videos, Audio)
    # Excludes commands to prevent loops
    application.add_handler(MessageHandler(
        filters.ALL & ~filters.COMMAND & (
            filters.Document.ALL | 
            filters.VIDEO | 
            filters.PHOTO | 
            filters.AUDIO
        ), 
        file_handler.handle_media
    ))

    # Admin Commands
    application.add_handler(CommandHandler("stats", admin.stats_command))
    application.add_handler(CommandHandler("ban", admin.ban_command))
    application.add_handler(CommandHandler("unban", admin.unban_command))
    application.add_handler(CommandHandler("broadcast", admin.broadcast_command))

    # Run Bot
    print("🤖 Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
