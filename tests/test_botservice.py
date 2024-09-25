# tests/test_botservice.py

import unittest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.botservice import BotService

class TestBotService(unittest.TestCase):

    @patch('src.botservice.get_plugins')
    @patch('src.botservice.CommandHandler')
    @patch('src.botservice.MattermostClient')
    def test_handle_command(self, mock_mm_client_cls, mock_command_handler_cls, mock_get_plugins):
        """
        Test that handling a command invokes CommandHandler and posts the response.
        """
        # Setup mocks
        mock_command_handler = MagicMock()
        mock_command_handler.execute.return_value = "Command executed"
        mock_command_handler_cls.return_value = mock_command_handler

        mock_mm_client = MagicMock()
        mock_mm_client_cls.return_value = mock_mm_client

        # Mock plugins (empty in this case)
        mock_plugins = {}
        mock_get_plugins.return_value = mock_plugins

        # Instantiate BotService after applying patches
        bot_service = BotService()

        # Execute a command
        bot_service.handle_command('channel_id', 'user_id', '/test arg1 arg2')

        # Assert that CommandHandler.execute was called correctly
        mock_command_handler.execute.assert_called_once_with('test', ['arg1', 'arg2'], 'channel_id', 'user_id')

        # Assert that MattermostClient.post_message was called with the response
        mock_mm_client.post_message.assert_called_once_with('channel_id', 'Command executed')

    @patch('src.botservice.get_plugins')
    def test_handle_chat(self, mock_get_plugins):
        """
        Test that handling a chat message invokes the ChatPlugin and posts the response.
        """
        # Create a mock chat plugin
        mock_chat_plugin = MagicMock()
        mock_chat_plugin.execute.return_value = "Chat response"

        # Setup mocked plugins
        mock_plugins = {'chat': mock_chat_plugin}
        mock_get_plugins.return_value = mock_plugins

        # Patch MattermostClient and CommandHandler if BotService depends on them during handle_chat
        with patch('src.botservice.MattermostClient') as mock_mm_client_cls, \
             patch('src.botservice.CommandHandler') as mock_command_handler_cls:

            # Instantiate BotService after applying patches
            bot_service = BotService()

            # Execute a chat message
            bot_service.handle_chat('channel_id', 'user_id', 'Hello, bot!')

            # Assert that chat_plugin.execute was called correctly
            mock_chat_plugin.execute.assert_called_once_with(['Hello, bot!'], 'channel_id', 'user_id')

            # Assert that MattermostClient.post_message was called with the response
            mock_mm_client = mock_mm_client_cls.return_value
            mock_mm_client.post_message.assert_called_once_with('channel_id', 'Chat response')

    @patch('src.botservice.MattermostClient')
    def test_handle_message_with_chat(self, mock_mm_client_cls):
        """
        Test that handle_message correctly delegates non-command messages to handle_chat.
        """
        # Setup MattermostClient mock
        mock_mm_client = MagicMock()
        mock_mm_client.bot_id = 'bot_id'
        mock_mm_client_cls.return_value = mock_mm_client

        # Mock get_plugins to include 'chat' plugin
        with patch('src.botservice.get_plugins') as mock_get_plugins, \
             patch('src.botservice.CommandHandler') as mock_command_handler_cls:

            # Create a mock chat plugin
            mock_chat_plugin = MagicMock()
            mock_chat_plugin.execute.return_value = "Chat response"
            mock_get_plugins.return_value = {'chat': mock_chat_plugin}

            # Instantiate BotService after applying patches
            bot_service = BotService()

            # Prepare event_data for a chat message
            event_data = {
                'data': {
                    'post': '{"channel_id": "channel_id", "user_id": "user_id", "message": "Hello, bot!"}'
                }
            }

            # Execute handle_message
            bot_service.handle_message(event_data)

            # Assert that chat_plugin.execute was called correctly
            mock_chat_plugin.execute.assert_called_once_with(['Hello, bot!'], 'channel_id', 'user_id')

            # Assert that post_message was called with the chat response
            mock_mm_client.post_message.assert_called_once_with('channel_id', 'Chat response')

    @patch('src.botservice.MattermostClient')
    @patch('src.botservice.CommandHandler')
    @patch('src.botservice.get_plugins')
    def test_handle_message_with_command(self, mock_get_plugins, mock_command_handler_cls, mock_mm_client_cls):
        """
        Test that handle_message correctly delegates command messages to handle_command.
        """
        # Setup mocks
        mock_command_handler = MagicMock()
        mock_command_handler.execute.return_value = "Command executed"
        mock_command_handler_cls.return_value = mock_command_handler

        mock_mm_client = MagicMock()
        mock_mm_client.bot_id = 'bot_id'
        mock_mm_client_cls.return_value = mock_mm_client

        # Mock plugins (empty in this case)
        mock_plugins = {}
        mock_get_plugins.return_value = mock_plugins

        # Instantiate BotService after applying patches
        bot_service = BotService()

        # Prepare event_data for a command message
        event_data = {
            'data': {
                'post': '{"channel_id": "channel_id", "user_id": "user_id", "message": "/test arg1 arg2"}'
            }
        }

        # Execute handle_message
        bot_service.handle_message(event_data)

        # Assert that CommandHandler.execute was called correctly
        mock_command_handler.execute.assert_called_once_with('test', ['arg1', 'arg2'], 'channel_id', 'user_id')

        # Assert that post_message was called with the command response
        mock_mm_client.post_message.assert_called_once_with('channel_id', 'Command executed')

    @patch('src.botservice.MattermostClient')
    @patch('src.botservice.CommandHandler')
    @patch('src.botservice.get_plugins')
    def test_handle_message_from_bot(self, mock_get_plugins, mock_command_handler_cls, mock_mm_client_cls):
        """
        Test that handle_message ignores messages sent by the bot itself.
        """
        # Setup mocks
        mock_command_handler = MagicMock()
        mock_command_handler_cls.return_value = mock_command_handler

        mock_mm_client = MagicMock()
        mock_mm_client.bot_id = 'bot_id'
        mock_mm_client_cls.return_value = mock_mm_client

        # Mock plugins (empty in this case)
        mock_plugins = {}
        mock_get_plugins.return_value = mock_plugins

        # Instantiate BotService after applying patches
        bot_service = BotService()

        # Prepare event_data for a message from the bot itself
        event_data = {
            'data': {
                'post': '{"channel_id": "channel_id", "user_id": "bot_id", "message": "Hello, bot!"}'
            }
        }

        # Execute handle_message
        bot_service.handle_message(event_data)

        # Assert that no actions were taken
        mock_command_handler.execute.assert_not_called()
        mock_mm_client.post_message.assert_not_called()

    @patch('src.botservice.get_plugins')
    @patch('src.botservice.CommandHandler')
    @patch('src.botservice.MattermostClient')
    def test_start_and_stop(self, mock_mm_client_cls, mock_command_handler_cls, mock_get_plugins):
        """
        Test that BotService starts and stops correctly, connecting to Mattermost and cleaning up plugins.
        """
        # Setup mocks
        mock_mm_client = MagicMock()
        mock_mm_client_cls.return_value = mock_mm_client

        mock_command_handler = MagicMock()
        mock_command_handler_cls.return_value = mock_command_handler

        # Mock plugins (empty in this case)
        mock_plugins = {}
        mock_get_plugins.return_value = mock_plugins

        # Instantiate BotService after applying patches
        bot_service = BotService()

        # Start the service
        bot_service.start()

        # Assert that MattermostClient.connect was called
        mock_mm_client.connect.assert_called_once()

        # Assert that add_message_listener was called with handle_message
        mock_mm_client.add_message_listener.assert_called_once_with(bot_service.handle_message)

        # Stop the service
        bot_service.stop()

        # Assert that MattermostClient.close was called
        mock_mm_client.close.assert_called_once()

        # Assert that plugin.cleanup was called for all plugins (none in this case)
        # If there were plugins, ensure their cleanup methods are called
        # Since mock_plugins is empty, no action is needed

if __name__ == '__main__':
    unittest.main()
