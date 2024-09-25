import logging
import json
from src.mattermost_client import MattermostClient
from src.command_handler import CommandHandler
from src.plugins import get_plugins

logger = logging.getLogger(__name__)

class BotService:
    def __init__(self):
        self.mm_client = MattermostClient()
        self.command_handler = CommandHandler()
        self.plugins = get_plugins()

    def start(self):
        logger.info("Starting BotService...")
        self.mm_client.connect()
        self.mm_client.add_message_listener(self.handle_message)
        logger.info("BotService started successfully.")

    def handle_message(self, event_data):
        post = event_data.get('data', {}).get('post')
        if post:
            post_data = json.loads(post)
            channel_id = post_data.get('channel_id')
            user_id = post_data.get('user_id')
            message = post_data.get('message', '').strip()
            file_ids = post_data.get('file_ids', [])

            # Ignore messages from the bot itself
            if user_id == self.mm_client.bot_id:
                return

            # Check if the message is a command
            if message.startswith('/'):
                self.handle_command(channel_id, user_id, message, file_ids)
            else:
                self.handle_chat(channel_id, user_id, message)

    def handle_command(self, channel_id, user_id, message, file_ids):
        command, *args = message[1:].split()

        # If there are file_ids, append the first one to args
        if file_ids:
            args.append(file_ids[0])

        response = self.command_handler.execute(command, args, channel_id, user_id)
        if response:
            self.mm_client.post_message(channel_id, response)

    def handle_chat(self, channel_id, user_id, message):
        chat_plugin = self.plugins.get('chat')
        if chat_plugin:
            response = chat_plugin.execute([message], channel_id, user_id)
            if response:
                self.mm_client.post_message(channel_id, response)
        else:
            logger.warning("Chat plugin not found. Unable to process chat message.")

    def stop(self):
        logger.info("Stopping BotService...")
        self.mm_client.close()
        for plugin in self.plugins.values():
            plugin.cleanup()
        logger.info("BotService stopped successfully.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot_service = BotService()
    bot_service.start()

    # Keep the service running
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        bot_service.stop()