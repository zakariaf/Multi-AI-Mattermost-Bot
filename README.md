# Multi-AI Mattermost Bot

A modular and extensible Python-based bot for Mattermost that integrates with various AI tools through a plugin architecture. This bot enables intelligent and automated interactions within your team's communication channels, supporting functionalities like chat, image generation, audio transcription, and more.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create and Activate a Virtual Environment](#2-create-and-activate-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Configure Environment Variables](#4-configure-environment-variables)
- [Usage](#usage)
  - [Starting the Bot](#starting-the-bot)
  - [Available Commands](#available-commands)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
- [Architecture](#architecture)
- [OpenAI API Integration](#openai-api-integration)
- [Mattermost Client Integration](#mattermost-client-integration)
- [Plugins](#plugins)
  - [Adding New Plugins](#adding-new-plugins)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Modular Plugin System:** Easily extend the bot's capabilities by adding new plugins for different AI services.
- **Multi-AI Integration:** Supports integration with various AI tools (e.g., OpenAI, Hugging Face, custom models) through flexible clients.
- **Automated Responses:** Instantly responds to user queries within Mattermost channels.
- **Rich Media Support:** Handles chat, audio transcription, image generation, and more.
- **Secure Configuration:** Manages sensitive information through environment variables.

## Prerequisites

Before setting up the Multi-AI Mattermost Bot, ensure you have the following:

- **Python 3.8+**: Ensure Python is installed on your system. [Download Python](https://www.python.org/downloads/)
- **Git**: For version control. [Download Git](https://git-scm.com/downloads)
- **Mattermost Server Access**: Access to your Mattermost instance and a bot account with an access token.
- **OpenAI API Key**: Obtain an API key from [OpenAI](https://platform.openai.com/account/api-keys).

## Installation

### 1. Clone the Repository

Begin by cloning the repository to your local machine:

```bash
git clone https://github.com/zakariaf/Multi-AI-Mattermost-Bot.git
cd Multi-AI-Mattermost-Bot
```

### 2. Create and Activate a Virtual Environment

It's recommended to use a virtual environment to manage dependencies:

```bash
python3 -m venv venv
```

Activate the virtual environment:

- **On macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

- **On Windows:**

  ```bash
  venv\Scripts\activate
  ```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project's root directory to store your configuration variables:

```bash
touch .env
```

Open the `.env` file in your preferred text editor and add the following variables:

```env
# Mattermost Configuration
MATTERMOST_URL=https://your-mattermost-server.com
MATTERMOST_TOKEN=your_mattermost_bot_token
MATTERMOST_BOTNAME=@ai-bot

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4
OPENAI_MAX_TOKENS=1500
OPENAI_TEMPERATURE=0.7

# Hugging Face Configuration (if applicable)
HUGGINGFACE_API_KEY=your_huggingface_api_key
HUGGINGFACE_API_BASE=https://api-inference.huggingface.co/models

# Custom Service Configuration
CUSTOM_AI_API_KEY=your_custom_ai_api_key

# Bot Configuration
BOT_CONTEXT_MSG=50
BOT_INSTRUCTION=You are a helpful assistant.

# Plugins Configuration
PLUGINS=chat,image,audio

# Service Configuration
CHAT_SERVICE=openai
IMAGE_SERVICE=dalle
AUDIO_SERVICE=openai

# Temporary Directory for file operations
TEMP_DIR=/tmp/mattermost_bot
```

**Notes:**

- **MATTERMOST_URL**: Your Mattermost server URL.
- **MATTERMOST_TOKEN**: The access token obtained from creating a Mattermost bot account.
- **MATTERMOST_BOTNAME**: Desired bot username (e.g., `@ai-bot`).
- **OPENAI_API_KEY**: Your OpenAI API key.
- **OPENAI_API_BASE**: Base URL for OpenAI API (default is `https://api.openai.com/v1`).
- **OPENAI_MODEL_NAME**: The OpenAI model to use (e.g., `gpt-4`).
- **OPENAI_MAX_TOKENS**: Maximum number of tokens for OpenAI responses.
- **OPENAI_TEMPERATURE**: Sampling temperature for OpenAI responses.
- **BOT_CONTEXT_MSG**: Number of previous messages to include in the context.
- **BOT_INSTRUCTION**: System-level instructions for the bot.
- **PLUGINS**: Comma-separated list of plugins to enable (`chat,image,audio`).
- **CHAT_SERVICE**, **IMAGE_SERVICE**, **AUDIO_SERVICE**: Default services to use for each plugin.
- **TEMP_DIR**: Directory for temporary file storage.

**Security Reminder:** Ensure that the `.env` file is **never** committed to version control. It's already included in `.gitignore`.

## Usage

### Starting the Bot

Once the environment is configured, you can start the bot:

```bash
python run_bot.py
```

**Note:** Ensure that your virtual environment is activated before running the bot.

### Available Commands

The bot supports several commands to utilize OpenAI's advanced features:

- **Chat Command**

  **Usage:**

  ```
  /chat [--service <service_name>] <message>
  ```

  **Example:**

  ```
  /chat What's the weather like today?
  ```

  **Description:**

  Engages in a conversation with the bot. Sends the provided message to the chat service (default is OpenAI's ChatCompletion API) and returns the assistant's reply.

- **Image Generation Command**

  **Usage:**

  ```
  /image <description> [--service <service_name>]
  ```

  **Example:**

  ```
  /image A serene landscape with mountains and a river during sunset.
  ```

  **Description:**

  Generates an image based on the provided description using the specified image service (default is OpenAI's DALL-E API) and uploads it to the Mattermost channel.

- **Audio Transcription Command**

  **Usage:**

  ```
  /audio <file_id> [--service <service_name>]
  ```

  **Example:**

  ```
  /audio abc123def456
  ```

  **Description:**

  Transcribes the audio file with the given `file_id` using the specified audio service (default is OpenAI's Whisper API) and posts the transcription to the channel.

**Note:** For the `/audio` command, you need to provide the `file_id` of an audio file that has been uploaded to Mattermost.

- **Help Command**

  **Usage:**

  ```
  /help [plugin_name]
  ```

  **Description:**

  Provides a list of available commands or detailed help for a specific plugin.

## Configuration

### Environment Variables

All configurations are managed via environment variables defined in the `.env` file. Here's a breakdown of each variable:

- **Mattermost Configuration:**
  - `MATTERMOST_URL`: URL of your Mattermost server.
  - `MATTERMOST_TOKEN`: Access token for the Mattermost bot.
  - `MATTERMOST_BOTNAME`: Username of the bot (e.g., `@ai-bot`).

- **OpenAI Configuration:**
  - `OPENAI_API_KEY`: API key for accessing OpenAI services.
  - `OPENAI_API_BASE`: Base endpoint for OpenAI API.
  - `OPENAI_MODEL_NAME`: Specifies the OpenAI model to use (e.g., `gpt-4`).
  - `OPENAI_MAX_TOKENS`: Sets the maximum tokens for responses.
  - `OPENAI_TEMPERATURE`: Controls the randomness of responses.

- **Bot Configuration:**
  - `BOT_CONTEXT_MSG`: Number of previous messages included in the context for generating responses.
  - `BOT_INSTRUCTION`: System prompt guiding the bot's behavior.

- **Plugins Configuration:**
  - `PLUGINS`: Enables specific plugins by listing them comma-separated (`chat,image,audio`).

- **Service Configuration:**
  - `CHAT_SERVICE`: Default chat service to use (`openai`).
  - `IMAGE_SERVICE`: Default image generation service (`dalle`).
  - `AUDIO_SERVICE`: Default audio transcription service (`openai`).

- **Temporary Directory:**
  - `TEMP_DIR`: Directory path for temporary file storage.

## Architecture

The Multi-AI Mattermost Bot is designed with a modular architecture to ensure scalability and maintainability. The core components are:

- **Mattermost Client (`mattermost_client.py`):** Handles communication with Mattermost's APIs.
- **OpenAI Client (`openai_client.py`):** Interfaces with OpenAI's APIs.
- **Bot Service (`botservice.py`):** Orchestrates the bot's operations.
- **Command Handler (`command_handler.py`):** Parses and executes user commands.
- **Plugins (`plugins/`):** Contains plugins to extend bot functionality.
- **Configuration (`config.py`):** Manages configuration settings.

### Data Flow

1. **Event Listening:** The Mattermost Client listens for new messages.
2. **Message Handling:** The Bot Service processes messages and uses the Command Handler to interpret commands.
3. **API Interaction:** The OpenAI Client interacts with OpenAI's APIs to generate responses.
4. **Response Dispatch:** The Mattermost Client sends responses back to Mattermost channels.

## OpenAI API Integration

The Multi-AI Mattermost Bot leverages OpenAI's APIs to provide advanced functionalities, including:

- **Chat Responses:** Generates intelligent and context-aware replies to user messages.
- **Image Generation:** Creates images based on textual descriptions using OpenAI's DALL-E API.
- **Audio Transcription:** Transcribes audio files into text using OpenAI's Whisper API.

### How It Works

- **Chat Responses:** When a user sends a message starting with `/chat`, the bot forwards the message to the chat service, which processes the input and returns a relevant response.
- **Image Generation:** Users can request image creation by providing a description using the `/image` command. The bot uses the image service to generate the image and shares it within the channel.
- **Audio Transcription:** Users can upload audio files and provide the file ID using the `/audio` command. The bot transcribes the audio and shares the transcription.

### Configuration

Ensure the following environment variables are set in your `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4
OPENAI_MAX_TOKENS=1500
OPENAI_TEMPERATURE=0.7
```

### Testing OpenAI Integration

To verify that the OpenAI integration is functioning correctly, run the provided test script:

```bash
python tests/test_openai.py
```

Ensure that you receive appropriate responses, generated images, and transcribed text based on your inputs.

## Mattermost Client Integration

The Multi-AI Mattermost Bot includes a dedicated Mattermost client to handle interactions with the Mattermost server. This client manages sending and receiving messages, handling WebSocket connections, and performing necessary operations to ensure seamless bot functionality.

### Features

- **WebSocket Connection:** Listens for real-time events such as new messages.
- **Message Posting:** Sends messages to specific channels or direct messages.
- **User Management:** Retrieves user information and manages direct channels.
- **Event Handling:** Processes incoming events and triggers appropriate responses.

### Configuration

Ensure the following environment variables are set in your `.env` file:

```env
# Mattermost Configuration
MATTERMOST_URL=https://your-mattermost-server.com
MATTERMOST_TOKEN=your_mattermost_bot_token
MATTERMOST_BOTNAME=@ai-bot
```

### Testing the Mattermost Client

To verify that the Mattermost client is functioning correctly, run the provided test script:

```bash
python tests/test_mattermost_client.py
```

**Expected Output:**

```
Bot User Info: { ... }
User Info: { ... }
Direct Channel ID: abc123...
Post Message Response: { ... }
```

**Check in Mattermost:**

- Ensure that the bot posts a test message in the specified channel or direct message.

### Integration with Bot Service

The `botservice.py` utilizes the `MattermostClient` to listen for incoming messages and respond accordingly. It handles command parsing and delegates tasks to the appropriate plugins based on user input.

## Plugins

The bot supports a modular plugin system, allowing you to extend its functionalities. Available plugins include:

- **Chat Plugin (`chat`):** Handles general chat interactions.
- **Image Plugin (`image`):** Generates images based on descriptions.
- **Audio Plugin (`audio`):** Transcribes audio files.

To enable or disable plugins, modify the `PLUGINS` variable in the `.env` file accordingly.

### Plugin Structure

Each plugin is located in the `src/plugins/` directory and extends the `BasePlugin` class defined in `base_plugin.py`. Plugins must implement the following methods:

- `name`: The name of the plugin.
- `description`: A brief description of the plugin.
- `usage`: Instructions on how to use the plugin.
- `execute(args, channel_id, user_id)`: The main method that performs the plugin's functionality.

### Adding New Plugins

1. **Create a New Plugin File:**

   ```bash
   touch src/plugins/your_plugin_name_plugin.py
   ```

2. **Implement the Plugin:**

   Define your plugin by extending the `BasePlugin` class.

   ```python
   from src.plugins.base_plugin import BasePlugin

   class YourPluginNamePlugin(BasePlugin):
       name = "your_plugin_name"
       description = "Description of your plugin"
       usage = "/your_command <arguments>"

       def execute(self, args, channel_id, user_id):
           # Your plugin logic here
           return "Plugin response"

       def initialize(self):
           # Optional initialization code
           pass

       def cleanup(self):
           # Optional cleanup code
           pass
   ```

3. **Register the Plugin:**

   Add your plugin to the `PLUGINS` variable in the `.env` file:

   ```env
   PLUGINS=chat,image,audio,your_plugin_name
   ```

4. **Update `__init__.py`:**

   Ensure your plugin is loaded by the plugin system. The `get_plugins()` function in `src/plugins/__init__.py` will dynamically import plugins based on the `PLUGINS` variable.

## Development

Before deploying, ensure that all functionalities work as expected by writing and running tests. You can add tests in the `tests/` directory corresponding to your new plugins or features.

## Testing

Ensure all components work as expected by running test scripts and verifying interactions within Mattermost.

- **OpenAI Integration Test:**

  ```bash
  python tests/test_openai.py
  ```

- **Mattermost Client Test:**

  ```bash
  python tests/test_mattermost_client.py
  ```

- **Plugin Tests:**

  ```bash
  python run_tests.py
  ```

## Contributing

Contributions are welcome! Please open issues and submit pull requests for any enhancements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).