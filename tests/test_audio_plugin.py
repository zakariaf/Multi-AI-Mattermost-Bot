import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import shutil

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.plugins.audio_plugin import AudioPlugin
import src.plugins.audio_plugin as audio_plugin_module

class TestAudioPlugin(unittest.TestCase):

    @patch('src.plugins.audio_plugin.openai_transcribe')
    @patch('src.plugins.audio_plugin.MattermostClient')
    @patch('src.plugins.audio_plugin.os.remove')
    def test_execute_default_service(self, mock_remove, mock_mm_client, mock_transcribe):
        # Patch AUDIO_SERVICE before initializing the plugin
        with patch.object(audio_plugin_module, 'AUDIO_SERVICE', 'openai'):
            # Initialize the plugin after patching AUDIO_SERVICE
            plugin = AudioPlugin()
            plugin.initialize()  # Ensure TEMP_DIR is created

            # Set up mock return values
            mock_mm_client_instance = mock_mm_client.return_value
            mock_mm_client_instance.get_file_info.return_value = {
                'mime_type': 'audio/wav',
                'name': 'test.wav'
            }

            # Path to the actual .wav file in tests directory
            test_wav_path = os.path.join(os.path.dirname(__file__), 'sample_audio.wav')

            # Ensure the test .wav file exists
            self.assertTrue(os.path.exists(test_wav_path), f"Test .wav file not found at {test_wav_path}")

            # Mock the download_file method to copy the actual .wav file to the expected path
            def download_file_side_effect(file_id, audio_file_path):
                # Ensure the parent directory exists
                os.makedirs(os.path.dirname(audio_file_path), exist_ok=True)
                shutil.copy(test_wav_path, audio_file_path)

            mock_mm_client_instance.download_file.side_effect = download_file_side_effect

            # Set up the transcription return value
            mock_transcribe.return_value = (
                "The sun rises in the east and sets in the west. "
                "This simple fact has been observed by humans for thousands of years."
            )

            # Call the execute method with the file_id
            result = plugin.execute(["file_id"], "channel_id", "user_id")

        # Assertions to ensure that the methods were called as expected
        mock_mm_client_instance.get_file_info.assert_called_once_with("file_id")
        mock_mm_client_instance.download_file.assert_called_once_with(
            "file_id",
            os.path.join(audio_plugin_module.TEMP_DIR, "file_id_test.wav")
        )
        mock_transcribe.assert_called_once_with(
            os.path.join(audio_plugin_module.TEMP_DIR, "file_id_test.wav")
        )
        mock_mm_client_instance.post_message.assert_called_once_with(
            "channel_id",
            "Transcription by openai:\n\n"
            "The sun rises in the east and sets in the west. "
            "This simple fact has been observed by humans for thousands of years."
        )
        mock_remove.assert_called_once_with(
            os.path.join(audio_plugin_module.TEMP_DIR, "file_id_test.wav")
        )
        self.assertIsNone(result)

    @patch('src.plugins.audio_plugin.AUDIO_SERVICE', 'openai')
    def test_execute_unknown_service(self):
        # Initialize the plugin after patching AUDIO_SERVICE
        plugin = AudioPlugin()
        plugin.initialize()  # Ensure TEMP_DIR is created

        # Execute with an unknown service
        result = plugin.execute(["file_id", "--service", "unknown"], "channel_id", "user_id")

        # Assert that the appropriate error message is returned
        self.assertIn("Unknown service: unknown", result)

    @patch('src.plugins.audio_plugin.AUDIO_SERVICE', 'openai')
    def test_execute_no_args(self):
        # Initialize the plugin after patching AUDIO_SERVICE
        plugin = AudioPlugin()
        plugin.initialize()  # Ensure TEMP_DIR is created

        # Execute without any arguments
        result = plugin.execute([], "channel_id", "user_id")

        # Assert that the appropriate error message is returned
        self.assertIn("Please provide a file ID for the audio file", result)

if __name__ == '__main__':
    unittest.main()
