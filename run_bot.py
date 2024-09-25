import logging
from src.botservice import BotService

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Create and start the bot service
    bot_service = BotService()

    try:
        logger.info("Starting the bot service...")
        bot_service.start()

        # Keep the script running
        logger.info("Bot is now running. Press CTRL+C to stop.")
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Received interrupt. Shutting down...")
    finally:
        bot_service.stop()
        logger.info("Bot service has been stopped.")

if __name__ == "__main__":
    main()