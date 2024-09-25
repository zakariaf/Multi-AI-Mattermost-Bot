# tests/test_command_handler.py

import unittest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.command_handler import CommandHandler

class TestCommandHandler(unittest.TestCase):

    @patch('src.command_handler.get_plugins')
    def test_execute_plugin_command(self, mock_get_plugins):
        # Create a mock plugin using SimpleNamespace
        mock_plugin = SimpleNamespace(
            name='test',
            description='Test plugin',
            usage='/test <args>',
            execute=MagicMock(return_value=None)
        )
        mock_get_plugins.return_value = {'test': mock_plugin}

        # Instantiate CommandHandler after patching get_plugins
        handler = CommandHandler()

        # Execute the 'test' command
        handler.execute('test', ['arg1', 'arg2'], 'channel_id', 'user_id')

        # Assert that the plugin's execute method was called with correct arguments
        mock_plugin.execute.assert_called_once_with(['arg1', 'arg2'], 'channel_id', 'user_id')

    @patch('src.command_handler.get_plugins')
    def test_help_command(self, mock_get_plugins):
        # Create mock plugins using SimpleNamespace
        mock_image_plugin = SimpleNamespace(
            name='image',
            description='Image manipulation',
            usage='/image <args>'
        )
        mock_audio_plugin = SimpleNamespace(
            name='audio',
            description='Audio transcription',
            usage='/audio <args>'
        )
        mock_get_plugins.return_value = {
            'image': mock_image_plugin,
            'audio': mock_audio_plugin
        }

        # Instantiate CommandHandler after patching get_plugins
        handler = CommandHandler()

        # Execute the 'help' command without arguments
        result = handler.execute('help', [], 'channel_id', 'user_id')

        # Assert that the help text contains information about available commands
        self.assertIn('Available commands:', result)
        self.assertIn('/image - Image manipulation', result)
        self.assertIn('/audio - Audio transcription', result)

    @patch('src.command_handler.get_plugins')
    def test_help_command_for_plugin(self, mock_get_plugins):
        # Create a mock plugin using SimpleNamespace
        mock_plugin = SimpleNamespace(
            name='test',
            description='Test plugin',
            usage='/test <args>'
        )
        mock_get_plugins.return_value = {'test': mock_plugin}

        # Instantiate CommandHandler after patching get_plugins
        handler = CommandHandler()

        # Execute the 'help' command for the 'test' plugin
        result = handler.execute('help', ['test'], 'channel_id', 'user_id')

        # Assert that the help text for the specific plugin is correct
        self.assertIn('test: Test plugin', result)
        self.assertIn('Usage: /test <args>', result)

    @patch('src.command_handler.get_plugins')
    def test_execute_unknown_command(self, mock_get_plugins):
        # Mock plugins (can be empty or contain some plugins)
        mock_get_plugins.return_value = {}

        # Instantiate CommandHandler after patching get_plugins
        handler = CommandHandler()

        # Execute an unknown command
        result = handler.execute('unknown', [], 'channel_id', 'user_id')

        # Assert that the appropriate error message is returned
        self.assertEqual(result, 'Unknown command: unknown')

    @patch('src.command_handler.get_plugins')
    def test_execute_help_command_with_unknown_plugin(self, mock_get_plugins):
        # Create mock plugins using SimpleNamespace
        mock_existing_plugin = SimpleNamespace(
            name='existing_plugin',
            description='Existing plugin',
            usage='/existing <args>'
        )
        mock_get_plugins.return_value = {'existing_plugin': mock_existing_plugin}

        # Instantiate CommandHandler after patching get_plugins
        handler = CommandHandler()

        # Execute the 'help' command for an unknown plugin
        result = handler.execute('help', ['unknown_plugin'], 'channel_id', 'user_id')

        # Assert that the appropriate error message is returned
        self.assertIn('Unknown plugin: unknown_plugin', result)

if __name__ == '__main__':
    unittest.main()
