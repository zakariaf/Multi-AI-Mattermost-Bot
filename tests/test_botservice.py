# tests/test_botservice.py

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.botservice import BotService

class TestBotService(unittest.TestCase):

    @patch('src.botservice.get_plugins')
    @patch('src.botservice.CommandHandler')
    @patch('src.botservice.MattermostClient')
    def test_handle_command_with_file_id(self, mock_mm_client_cls, mock_command_handler_cls, mock_get_plugins):
        """
        Test that handling a command with a file_id appends the file_id to args and invokes CommandHandler correctly.
        """
        # Setup mocks
        mock_command_handler = MagicMock()
        mock_command_handler.execute.return_value = "Transcription result"
        mock_command_handler_cls.return_value = mock_command_handler

        mock_mm_client = MagicMock()
        mock_mm_client_cls.return_value = mock_mm_client

        # Mock plugins (excluding 'audio' since we're directly testing CommandHandler)
        mock_plugins = {}
        mock_get_plugins.return_value = mock_plugins

        # Instantiate BotService after applying patches
        bot_service = BotService()

        # Execute a command with file_id
        bot_service.handle_command('channel_id', 'user_id', '/audio', ['test_file_id_123'])

        # Assert that CommandHandler.execute was called correctly with file_id appended to args
        mock_command_handler.execute.assert_called_once_with('audio', ['test_file_id_123'], 'channel_id', 'user_id')

        # Assert that MattermostClient.post_message was called with the response
        mock_mm_client.post_message.assert_called_once_with('channel_id', 'Transcription result')

    @patch('src.botservice.get_plugins')
    @patch('src.botservice.CommandHandler')
    @patch('src.botservice.MattermostClient')
    def test_handle_command_without_file_id(self, mock_mm_client_cls, mock_command_handler_cls, mock_get_plugins):
        """
        Test that handling a command without a file_id invokes CommandHandler correctly without appending file_id.
        """
        # Setup mocks
        mock_command_handler = MagicMock()
        mock_command_handler.execute.return_value = "Command executed without file_id"
        mock_command_handler_cls.return_value = mock_command_handler

        mock_mm_client = MagicMock()
        mock_mm_client_cls.return_value = mock_mm_client

        # Mock plugins (excluding 'audio' since we're directly testing CommandHandler)
        mock_plugins = {}
        mock_get_plugins.return_value = mock_plugins

        # Instantiate BotService after applying patches
        bot_service = BotService()

        # Execute a command without file_id
        bot_service.handle_command('channel_id', 'user_id', '/test arg1 arg2', [])

        # Assert that CommandHandler.execute was called correctly without file_id
        mock_command_handler.execute.assert_called_once_with('test', ['arg1', 'arg2'], 'channel_id', 'user_id')

        # Assert that MattermostClient.post_message was called with the response
        mock_mm_client.post_message.assert_called_once_with('channel_id', 'Command executed without file_id')

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

        # Patch MattermostClient and CommandHandler
        with patch('src.botservice.MattermostClient') as mock_mm_client_cls, \
             patch('src.botservice.CommandHandler') as mock_command_handler_cls:

            # Instantiate BotService after applying patches
            bot_service = BotService()

            # Execute a chat message
            bot_service.handle_chat('channel_id', 'user_id', 'Hello, bot!')

            # Assert that chat_plugin.execute was called correctly
            mock_chat_plugin.execute.assert_called_once_with(['Hello, bot!'], 'channel_id', 'user_id')

            # Assert that post_message was called with the chat response
            mock_mm_client = mock_mm_client_cls.return_value
            mock_mm_client.post_message.assert_called_once_with('channel_id', 'Chat response')

    @patch('src.botservice.get_plugins')
    @patch('src.botservice.CommandHandler')
    @patch('src.botservice.MattermostClient')
    def test_handle_message_with_command_and_file_id(self, mock_mm_client_cls, mock_command_handler_cls, mock_get_plugins):
        """
        Test that handle_message correctly delegates command messages with file_ids to handle_command.
        """
        # Setup mocks
        mock_command_handler = MagicMock()
        mock_command_handler.execute.return_value = "Command executed with file_id"
        mock_command_handler_cls.return_value = mock_command_handler

        mock_mm_client = MagicMock()
        mock_mm_client.bot_id = 'bot_id'
        mock_mm_client_cls.return_value = mock_mm_client

        # Mock plugins (excluding 'audio' since we're directly testing CommandHandler)
        mock_plugins = {}
        mock_get_plugins.return_value = mock_plugins

        # Instantiate BotService after applying patches
        bot_service = BotService()

        # Prepare event_data for a command message with file_id
        event_data = {
            'data': {
                'post': '{"channel_id": "channel_id", "user_id": "user_id", "message": "/audio", "file_ids": ["test_file_id_123"]}'
            }
        }

        # Execute handle_message
        bot_service.handle_message(event_data)

        # Assert that CommandHandler.execute was called correctly with file_id appended to args
        mock_command_handler.execute.assert_called_once_with('audio', ['test_file_id_123'], 'channel_id', 'user_id')

        # Assert that post_message was called with the command response
        mock_mm_client.post_message.assert_called_once_with('channel_id', 'Command executed with file_id')

    @patch('src.botservice.get_plugins')
    @patch('src.botservice.CommandHandler')
    @patch('src.botservice.MattermostClient')
    def test_handle_message_with_command_and_multiple_file_ids(self, mock_mm_client_cls, mock_command_handler_cls, mock_get_plugins):
        """
        Test that handle_message appends only the first file_id when multiple file_ids are present.
        """
        # Setup mocks
        mock_command_handler = MagicMock()
        mock_command_handler.execute.return_value = "Command executed with first file_id"
        mock_command_handler_cls.return_value = mock_command_handler

        mock_mm_client = MagicMock()
        mock_mm_client.bot_id = 'bot_id'
        mock_mm_client_cls.return_value = mock_mm_client

        # Mock plugins
        mock_plugins = {}
        mock_get_plugins.return_value = mock_plugins

        # Instantiate BotService after applying patches
        bot_service = BotService()

        # Prepare event_data for a command message with multiple file_ids
        event_data = {
            'data': {
                'post': '{"channel_id": "channel_id", "user_id": "user_id", "message": "/audio", "file_ids": ["file_id_1", "file_id_2"]}'
            }
        }

        # Execute handle_message
        bot_service.handle_message(event_data)

        # Assert that CommandHandler.execute was called with only the first file_id
        mock_command_handler.execute.assert_called_once_with('audio', ['file_id_1'], 'channel_id', 'user_id')

        # Assert that post_message was called with the command response
        mock_mm_client.post_message.assert_called_once_with('channel_id', 'Command executed with first file_id')

    @patch('src.botservice.get_plugins')
    def test_handle_message_with_chat_message(self, mock_get_plugins):
        """
        Test that handle_message correctly delegates non-command messages to handle_chat.
        """
        # Create a mock chat plugin
        mock_chat_plugin = MagicMock()
        mock_chat_plugin.execute.return_value = "Chat response"

        # Setup mocked plugins
        mock_plugins = {'chat': mock_chat_plugin}
        mock_get_plugins.return_value = mock_plugins

        # Patch MattermostClient and CommandHandler
        with patch('src.botservice.MattermostClient') as mock_mm_client_cls, \
             patch('src.botservice.CommandHandler') as mock_command_handler_cls:

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
            mock_mm_client = mock_mm_client_cls.return_value
            mock_mm_client.post_message.assert_called_once_with('channel_id', 'Chat response')

    @patch('src.botservice.get_plugins')
    @patch('src.botservice.CommandHandler')
    @patch('src.botservice.MattermostClient')
    def test_handle_message_with_command_no_response(self, mock_mm_client_cls, mock_command_handler_cls, mock_get_plugins):
        """
        Test that if CommandHandler.execute returns None, no message is posted.
        """
        # Setup mocks
        mock_command_handler = MagicMock()
        mock_command_handler.execute.return_value = None
        mock_command_handler_cls.return_value = mock_command_handler

        mock_mm_client = MagicMock()
        mock_mm_client.bot_id = 'bot_id'
        mock_mm_client_cls.return_value = mock_mm_client

        # Mock plugins
        mock_plugins = {}
        mock_get_plugins.return_value = mock_plugins

        # Instantiate BotService after applying patches
        bot_service = BotService()

        # Prepare event_data for a command message
        event_data = {
            'data': {
                'post': '{"channel_id": "channel_id", "user_id": "user_id", "message": "/test arg1 arg2", "file_ids": []}'
            }
        }

        # Execute handle_message
        bot_service.handle_message(event_data)

        # Assert that CommandHandler.execute was called correctly
        mock_command_handler.execute.assert_called_once_with('test', ['arg1', 'arg2'], 'channel_id', 'user_id')

        # Assert that post_message was not called since response is None
        mock_mm_client.post_message.assert_not_called()

    @patch('src.botservice.get_plugins')
    @patch('src.botservice.CommandHandler')
    @patch('src.botservice.MattermostClient')
    def test_handle_message_with_command_and_service_flag(self, mock_mm_client_cls, mock_command_handler_cls, mock_get_plugins):
        """
        Test that handle_command correctly handles the --service flag and appends the file_id if present.
        """
        # Setup mocks
        mock_command_handler = MagicMock()
        mock_command_handler.execute.return_value = "Command with service flag executed"
        mock_command_handler_cls.return_value = mock_command_handler

        mock_mm_client = MagicMock()
        mock_mm_client_cls.return_value = mock_mm_client

        # Mock plugins (empty in this case)
        mock_plugins = {}
        mock_get_plugins.return_value = mock_plugins

        # Instantiate BotService after applying patches
        bot_service = BotService()

        # Prepare event_data for a command message with --service flag and file_id
        event_data = {
            'data': {
                'post': '{"channel_id": "channel_id", "user_id": "user_id", "message": "/audio --service openai", "file_ids": ["service_file_id_789"]}'
            }
        }

        # Execute handle_message
        bot_service.handle_message(event_data)

        # Assert that CommandHandler.execute was called correctly with file_id appended to args
        mock_command_handler.execute.assert_called_once_with(
            'audio',
            ['--service', 'openai', 'service_file_id_789'],
            'channel_id',
            'user_id'
        )

        # Assert that post_message was called with the command response
        mock_mm_client.post_message.assert_called_once_with('channel_id', 'Command with service flag executed')

    @patch('src.botservice.get_plugins')
    def test_handle_message_from_bot(self, mock_get_plugins):
        """
        Test that handle_message ignores messages sent by the bot itself.
        """
        # Patch MattermostClient and CommandHandler
        with patch('src.botservice.MattermostClient') as mock_mm_client_cls, \
             patch('src.botservice.CommandHandler') as mock_command_handler_cls:

            # Setup mocks
            mock_mm_client = MagicMock()
            mock_mm_client.bot_id = 'bot_id'
            mock_mm_client_cls.return_value = mock_mm_client

            mock_command_handler = MagicMock()
            mock_command_handler_cls.return_value = mock_command_handler

            # Mock plugins
            mock_plugins = {}
            mock_get_plugins.return_value = mock_plugins

            # Instantiate BotService after applying patches
            bot_service = BotService()

            # Prepare event_data for a message sent by the bot itself
            event_data = {
                'data': {
                    'post': '{"channel_id": "channel_id", "user_id": "bot_id", "message": "/audio"}'
                }
            }

            # Execute handle_message
            bot_service.handle_message(event_data)

            # Assert that CommandHandler.execute was not called
            mock_command_handler.execute.assert_not_called()

            # Assert that post_message was not called
            mock_mm_client.post_message.assert_not_called()

    @patch('src.botservice.get_plugins')
    def test_start_and_stop(self, mock_get_plugins):
        """
        Test that BotService starts and stops correctly, connecting to Mattermost and cleaning up plugins.
        """
        # Patch MattermostClient and CommandHandler
        with patch('src.botservice.MattermostClient') as mock_mm_client_cls, \
             patch('src.botservice.CommandHandler') as mock_command_handler_cls:

            # Setup mocks
            mock_mm_client = MagicMock()
            mock_mm_client_cls.return_value = mock_mm_client

            mock_command_handler = MagicMock()
            mock_command_handler_cls.return_value = mock_command_handler

            # Mock plugins
            mock_plugins = {'audio': MagicMock(), 'chat': MagicMock()}
            mock_get_plugins.return_value = mock_plugins

            # Instantiate BotService after applying patches
            bot_service = BotService()

            # Start the service
            bot_service.start()

            # Assert that MattermostClient.connect was called
            mock_mm_client.connect.assert_called_once()

            # Assert that handle_message was added as a message listener
            mock_mm_client.add_message_listener.assert_called_once_with(bot_service.handle_message)

            # Stop the service
            bot_service.stop()

            # Assert that MattermostClient.close was called
            mock_mm_client.close.assert_called_once()

            # Assert that cleanup was called on all plugins
            for plugin in mock_plugins.values():
                plugin.cleanup.assert_called_once()

if __name__ == '__main__':
    unittest.main()