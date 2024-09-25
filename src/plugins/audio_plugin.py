import os
import requests
import shutil
from urllib.parse import urlparse
from src.plugins.base_plugin import BasePlugin
from src.openai_client import transcribe_audio as openai_transcribe
from src.mattermost_client import MattermostClient
from src.config import TEMP_DIR, AUDIO_SERVICE

class AudioPlugin(BasePlugin):
    name = "audio"
    description = "Transcribe audio files"
    usage = "/audio <file_id|file_url|file_path|file> [--service <service_name>]"

    def __init__(self):
        self.services = {
            "openai": openai_transcribe,
            # Add other transcription services here, e.g.:
            # "google": google_transcribe,
            # "azure": azure_transcribe,
        }
        self.default_service = AUDIO_SERVICE
        self.mm_client = MattermostClient()  # Initialize once

    def execute(self, args, channel_id, user_id):
        if not args:
            return f"Please provide a file ID, URL, or file path for the audio file. Usage: {self.usage}"

        # Parse arguments
        service = self.default_service
        file_input = None

        # Check for '--service' flag
        if "--service" in args:
            service_index = args.index("--service")
            if service_index + 1 < len(args):
                service = args[service_index + 1]
                # Remove the service flag and its value from args
                args = args[:service_index] + args[service_index + 2:]
            else:
                return "Please specify a service name after --service"

        if not args:
            return f"Please provide a file ID, URL, or file path for the audio file. Usage: {self.usage}"

        file_input = args[0]

        # Validate the service
        if service not in self.services:
            return f"Unknown service: {service}. Available services: {', '.join(self.services.keys())}"

        # Determine if the input is a URL, file path, or file ID
        if self.is_url(file_input):
            # Handle URL input
            audio_file_path = self.download_file_from_url(file_input)
            if not audio_file_path:
                return "Failed to download the audio file from the provided URL."
        elif self.is_valid_path(file_input):
            # Handle local file path input
            if not os.path.isfile(file_input):
                return f"The provided file path does not exist or is not a file: {file_input}"
            audio_file_path = file_input
        else:
            # Assume it's a Mattermost file ID
            audio_file_path = self.download_file_from_id(file_input)
            if not audio_file_path:
                return "Failed to download the audio file from the provided file ID."

        # Ensure the TEMP_DIR exists
        os.makedirs(TEMP_DIR, exist_ok=True)

        try:
            # Transcribe the audio
            transcribe_function = self.services[service]
            transcript = transcribe_function(audio_file_path)
            response_message = f"Transcription by {service}:\n\n{transcript}"
            return response_message
        except Exception as e:
            return f"Failed to transcribe the audio using {service}: {str(e)}"
        finally:
            # Clean up the downloaded file if it was downloaded from a URL or file ID
            if self.is_url(file_input) or not self.is_valid_path(file_input):
                try:
                    os.remove(audio_file_path)
                except Exception as e:
                    # Log the error if needed
                    pass

    def initialize(self):
        os.makedirs(TEMP_DIR, exist_ok=True)
        print(f"Initialized {self.name} plugin with default service: {self.default_service}")

    def cleanup(self):
        print(f"Cleaning up {self.name} plugin")

    def is_url(self, string):
        """
        Checks if the provided string is a valid URL.
        """
        try:
            result = urlparse(string)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def download_file_from_url(self, url):
        """
        Downloads a file from the provided URL to the TEMP_DIR.
        Returns the file path if successful, else None.
        """
        try:
            local_filename = os.path.join(TEMP_DIR, os.path.basename(urlparse(url).path))
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            return local_filename
        except Exception as e:
            # Log the error if needed
            return None

    def download_file_from_id(self, file_id):
        """
        Downloads a file from Mattermost using the file ID.
        Returns the file path if successful, else None.
        """
        try:
            file_info = self.mm_client.get_file_info(file_id)
            if not file_info:
                return None

            if not file_info['mime_type'].startswith('audio/'):
                return None

            audio_file_path = os.path.join(TEMP_DIR, f"{file_id}_{file_info['name']}")
            success = self.mm_client.download_file(file_id, audio_file_path)
            if success:
                return audio_file_path
            else:
                return None
        except Exception as e:
            # Log the error if needed
            return None

    def is_valid_path(self, path):
        """
        Checks if the provided path is a valid file system path.
        """
        # For security reasons, you might want to restrict paths
        # Here, we'll assume any absolute path is valid
        return os.path.isabs(path)