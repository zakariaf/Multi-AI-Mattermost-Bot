import os
from src.plugins.base_plugin import BasePlugin
from src.openai_client import transcribe_audio as openai_transcribe
from src.mattermost_client import MattermostClient
from src.config import TEMP_DIR, AUDIO_SERVICE

class AudioPlugin(BasePlugin):
    name = "audio"
    description = "Transcribe audio files"
    usage = "/audio <file_id> [--service <service_name>]"

    def __init__(self):
        self.services = {
            "openai": openai_transcribe,
            # Add other transcription services here, e.g.:
            # "google": google_transcribe,
            # "azure": azure_transcribe,
        }
        self.default_service = AUDIO_SERVICE

    def execute(self, args, channel_id, user_id):
        if not args:
            return f"Please provide a file ID for the audio file. Usage: {self.usage}"

        service = self.default_service
        file_id = args[0]

        if len(args) > 2 and args[1] == "--service":
            service = args[2]
            if service not in self.services:
                return f"Unknown service: {service}. Available services: {', '.join(self.services.keys())}"

        mm_client = MattermostClient()
        file_info = mm_client.get_file_info(file_id)

        if not file_info:
            return "Failed to get file information. Please check if the file ID is correct."

        if not file_info['mime_type'].startswith('audio/'):
            return "The provided file is not an audio file."

        audio_file_path = os.path.join(TEMP_DIR, f"{file_id}_{file_info['name']}")
        mm_client.download_file(file_id, audio_file_path)

        try:
            transcribe_function = self.services[service]
            transcript = transcribe_function(audio_file_path)
            mm_client.post_message(channel_id, f"Transcription by {service}:\n\n{transcript}")
            return None
        except Exception as e:
            return f"Failed to transcribe the audio using {service}: {str(e)}"
        finally:
            os.remove(audio_file_path)

    def initialize(self):
        os.makedirs(TEMP_DIR, exist_ok=True)
        print(f"Initialized {self.name} plugin with default service: {self.default_service}")

    def cleanup(self):
        print(f"Cleaning up {self.name} plugin")