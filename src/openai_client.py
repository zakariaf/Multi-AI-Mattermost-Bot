from openai import OpenAI
from config import (
    OPENAI_API_KEY,
    OPENAI_API_BASE,
    OPENAI_MODEL_NAME,
    OPENAI_MAX_TOKENS,
    OPENAI_TEMPERATURE
)
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

def generate_chat_response(messages):
    """
    Generates a response from the chat model based on the provided messages.

    :param messages: List of message dictionaries with 'role' and 'content'.
    :return: The assistant's reply as a string.
    """
    try:
        logger.debug(f"Sending messages to OpenAI: {messages}")
        response = client.chat.completions.create(
            model=OPENAI_MODEL_NAME,
            messages=messages,
            max_tokens=OPENAI_MAX_TOKENS,
            temperature=OPENAI_TEMPERATURE
        )
        assistant_message = response.choices[0].message.content.strip()
        logger.debug(f"Received response from OpenAI: {assistant_message}")
        return assistant_message
    except Exception as e:
        logger.error(f"Error generating chat response: {e}")
        return "I'm sorry, I couldn't process that request at the moment."

def generate_image(prompt):
    """
    Generates an image based on the provided prompt using OpenAI's DALL-E API.

    :param prompt: Description of the image to generate.
    :return: Base64-encoded image string or error message.
    """
    try:
        logger.debug(f"Generating image with prompt: {prompt}")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            quality= "hd",
            size="1024x1024",
            response_format="b64_json"
            n=1,
        )
        image_b64 = response.data[0].b64_json
        logger.debug("Image generated successfully.")
        return image_b64
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return None

def transcribe_audio(audio_file_path):
    """
    Transcribes audio content using OpenAI's Whisper API.

    :param audio_file_path: Path to the audio file to transcribe.
    :return: Transcribed text or error message.
    """
    try:
        logger.debug(f"Transcribing audio file: {audio_file_path}")
        with open(audio_file_path, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        logger.debug("Audio transcribed successfully.")
        return transcript.text.strip()
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        return "I'm sorry, I couldn't transcribe the audio."