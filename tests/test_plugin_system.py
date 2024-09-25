import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.plugins.base_plugin import BasePlugin
import src.plugins

class MockPlugin(BasePlugin):
    name = "mock"
    description = "A mock plugin for testing"
    usage = "/mock <args>"

    def execute(self, args, channel_id, user_id):
        return f"Executed mock plugin with args: {args}"

    def initialize(self):
        pass  # Mock initialization logic if needed

class TestPluginSystem(unittest.TestCase):

    def test_get_plugins(self):
        # Patching PLUGINS and import_module
        with patch('src.plugins.PLUGINS', ['mock']), \
             patch('src.plugins.importlib.import_module') as mock_import:

            # Create a mock module with a MockPlugin class
            mock_module = MagicMock()
            mock_module.MockPlugin = MockPlugin

            # Use side_effect to simulate the correct import behavior
            def import_side_effect(name):
                if name == 'src.plugins.mock_plugin':
                    return mock_module
                raise ImportError(f"Module {name} not found")

            mock_import.side_effect = import_side_effect

            # Call the actual function to be tested
            plugins = src.plugins.get_plugins()

            # Verify the result
            self.assertIn('mock', plugins)
            self.assertIsInstance(plugins['mock'], MockPlugin)
            mock_import.assert_called_once_with('src.plugins.mock_plugin')

    def test_base_plugin_abstract(self):
        with self.assertRaises(TypeError):
            BasePlugin()

if __name__ == '__main__':
    unittest.main()
