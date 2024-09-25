import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.plugins.chat_plugin import ChatPlugin
import src.plugins.chat_plugin as chat_plugin_module

class TestChatPlugin(unittest.TestCase):

    @patch('src.plugins.chat_plugin.openai_chat')
    def test_execute_default_service(self, mock_openai_chat):
        # Configure the mock to return a specific response
        mock_openai_chat.return_value = "AI response"

        # Patch CHAT_SERVICE before initializing the plugin
        with patch.object(chat_plugin_module, 'CHAT_SERVICE', 'openai'):
            # Initialize the plugin **after** patching
            plugin = ChatPlugin()

            # Execute the plugin with default service
            result = plugin.execute(["Hello"], "channel_id", "user_id")

        # Assertions to ensure the mock was called correctly
        mock_openai_chat.assert_called_once()
        expected_messages = [
            {"role": "system", "content": chat_plugin_module.BOT_INSTRUCTION},
            {"role": "user", "content": "Hello"}
        ]
        mock_openai_chat.assert_called_with(expected_messages)
        self.assertEqual(result, "[openai] AI response")

    @patch('src.plugins.chat_plugin.openai_chat')
    def test_execute_specific_service(self, mock_openai_chat):
        # Configure the mock to return a specific response
        mock_openai_chat.return_value = "AI response"

        # Patch CHAT_SERVICE before initializing the plugin
        with patch.object(chat_plugin_module, 'CHAT_SERVICE', 'openai'):
            # Initialize the plugin **after** patching
            plugin = ChatPlugin()

            # Execute the plugin with specific service
            result = plugin.execute(["--service", "openai", "Hello"], "channel_id", "user_id")

        # Assertions to ensure the mock was called correctly
        mock_openai_chat.assert_called_once()
        expected_messages = [
            {"role": "system", "content": chat_plugin_module.BOT_INSTRUCTION},
            {"role": "user", "content": "Hello"}
        ]
        mock_openai_chat.assert_called_with(expected_messages)
        self.assertEqual(result, "[openai] AI response")

    def test_execute_unknown_service(self):
        # Patch CHAT_SERVICE before initializing the plugin
        with patch.object(chat_plugin_module, 'CHAT_SERVICE', 'openai'):
            # Initialize the plugin **after** patching
            plugin = ChatPlugin()

            # Execute the plugin with an unknown service
            result = plugin.execute(["--service", "unknown", "Hello"], "channel_id", "user_id")

        # Assert that the appropriate error message is returned
        self.assertIn("Unknown service: unknown", result)

    def test_execute_no_message(self):
        # Patch CHAT_SERVICE before initializing the plugin
        with patch.object(chat_plugin_module, 'CHAT_SERVICE', 'openai'):
            # Initialize the plugin **after** patching
            plugin = ChatPlugin()

            # Execute the plugin without providing a message
            result = plugin.execute(["--service", "openai"], "channel_id", "user_id")

        # Assert that the appropriate error message is returned
        self.assertIn("Please specify a service name and a message", result)

if __name__ == '__main__':
    unittest.main()
