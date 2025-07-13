from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from handlers import start, button_handler, error_handler, help_command
from config import BOT_TOKEN, logger
import signal
import sys

    def __init__(self):
        self.updater = None
        self.dispatcher = None
        
    def setup_bot(self):
        """Initialize the bot and setup handlers"""
        try:
            self.updater = Updater(BOT_TOKEN, use_context=True)
            self.dispatcher = self.updater.dispatcher
            
            # Add command handlers
            self.dispatcher.add_handler(CommandHandler("start", start))
            self.dispatcher.add_handler(CommandHandler("help", help_command))
            
            # Add callback query handler
            self.dispatcher.add_handler(CallbackQueryHandler(button_handler))
            
            # Add error handler
            self.dispatcher.add_error_handler(error_handler)
            
            logger.info("Bot setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup bot: {e}")
            return False
    
    def start_bot(self):
        """Start the bot"""
        if not self.setup_bot():
            logger.error("Failed to setup bot. Exiting.")
            sys.exit(1)
            
        try:
            logger.info("Starting bot...")
            self.updater.start_polling()
            logger.info("Bot is running. Press Ctrl+C to stop.")
            self.updater.idle()
            
        except KeyboardInterrupt:
            logger.info("Received stop signal")
            self.stop_bot()
            
        except Exception as e:
            logger.error(f"Bot error: {e}")
            self.stop_bot()
            sys.exit(1)
    
    def stop_bot(self):
        """Stop the bot gracefully"""
        if self.updater:
            logger.info("Stopping bot...")
            self.updater.stop()
            logger.info("Bot stopped")

def signal_handler(signum, frame):
    """Handle system signals"""
    logger.info(f"Received signal {signum}")
    sys.exit(0)

def main():
    """Main function"""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Validate bot token
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("Bot token is not set. Please set the BOT_TOKEN environment variable.")
        sys.exit(1)
    
    # Create and start bot
    bot = TelegramBot()
    bot.start_bot()

if __name__ == '__main__':
    main()
