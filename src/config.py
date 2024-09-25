import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Mattermost Configuration
MATTERMOST_URL = os.getenv('MATTERMOST_URL')
MATTERMOST_TOKEN = os.getenv('MATTERMOST_TOKEN')
MATTERMOST_BOTNAME = os.getenv('MATTERMOST_BOTNAME', '@chatgpt-bot')

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
OPENAI_MODEL_NAME = os.getenv('OPENAI_MODEL_NAME', 'gpt-4o')
OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '2000'))
OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))

# Bot Configuration
BOT_CONTEXT_MSG = int(os.getenv('BOT_CONTEXT_MSG', '50'))
BOT_INSTRUCTION = os.getenv('BOT_INSTRUCTION', 'You are a helpful assistant.')

# Plugins Configuration
PLUGINS = os.getenv('PLUGINS', 'chat,image,audio').split(',')

# Service Configuration
CHAT_SERVICE = os.getenv('CHAT_SERVICE', 'openai')
IMAGE_SERVICE = os.getenv('IMAGE_SERVICE', 'dalle')
AUDIO_SERVICE = os.getenv('AUDIO_SERVICE', 'openai')

# Temporary Directory for file operations
TEMP_DIR = os.getenv('TEMP_DIR', '/tmp/mattermost_bot')

# Validate Essential Configurations
if not MATTERMOST_URL:
    raise ValueError("MATTERMOST_URL is not set in the environment variables.")
if not MATTERMOST_TOKEN:
    raise ValueError("MATTERMOST_TOKEN is not set in the environment variables.")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")