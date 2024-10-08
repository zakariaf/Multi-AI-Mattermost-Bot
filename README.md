![Under Development](https://img.shields.io/badge/status-under%20development-yellow.svg)

# Multi-AI Mattermost Bot (Under Development)

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
- [Development Status](#development-status)
- [Upcoming Features](#upcoming-features)
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
  /audio <file_id|file_url|file_path> [--service <service_name>]
  ```

  **Examples:**

  1. **Transcribe an Uploaded Audio File by `file_id`:**

    ```
    /audio abc123def456
    ```

  2. **Transcribe an Audio File via a Direct URL:**

    ```
    /audio https://example.com/path/to/audio.wav
    ```

  3. **Transcribe a Local Audio File on the Server:**

    ```
    /audio /path/to/local/audio.wav
    ```

  4. **Transcribe an Audio File Using a Specific Transcription Service:**

    ```
    /audio abc123def456 --service whisper
    ```

  **Description:**

  The `/audio` command allows you to transcribe audio files directly within Mattermost. You can provide the audio input in three different ways:

  1. **`file_id`:**
    - **Description:** The unique identifier of an audio file that has been uploaded to Mattermost.
    - **Usage:** Obtain the `file_id` by uploading an audio file to a channel and retrieving its details.
    - **Example:** `/audio abc123def456`

  2. **`file_url`:**
    - **Description:** A direct URL to an audio file accessible over the internet. This allows the bot to download and transcribe audio from external sources.
    - **Usage:** Provide a valid URL pointing to an audio file (e.g., `.wav`, `.mp3`).
    - **Example:** `/audio https://example.com/path/to/audio.wav`

  3. **`file_path`:**
    - **Description:** The absolute path to a local audio file on the server where the bot is running.
    - **Usage:** Ensure that the bot has read access to the specified file path on the server.
    - **Example:** `/audio /path/to/local/audio.wav`

  Additionally, you can specify a transcription service using the optional `--service` flag. If not provided, the bot will use the default service configured in the bot settings.

  **Optional `--service` Flag:**

  ```
  --service <service_name>
  ```

  - **Description:** Specifies the transcription service to use for processing the audio file.
  - **Supported Services:** Depends on your bot's configuration (e.g., `openai`, `google`, `azure`).
  - **Default Service:** If not specified, the bot uses the default service set in the configuration (e.g., OpenAI's Whisper API).
  - **Example:** `/audio abc123def456 --service google`

  **Example with Service Flag:**

  ```
  /audio https://example.com/path/to/audio.wav --service whisper
  ```

  **Note:**

  - **Supported Audio Formats:** Ensure that the audio files are in supported formats such as `.wav` or `.mp3` to guarantee successful transcription.
  - **Obtaining `file_id`:**
    - Upload an audio file to a Mattermost channel.
    - Click on the file to view its details.
    - Retrieve the `file_id` from the file's URL or details pane.
  - **Local File Access:** When using `file_path`, verify that the bot has the necessary permissions to access the specified path on the server.
  - **Service Availability:**
    - The availability of transcription services depends on your bot's configuration and the services you've integrated.
    - Ensure that the specified service (e.g., `openai`) is correctly configured and accessible.
  - **Security Considerations:**
    - Be cautious when providing `file_path` to prevent unauthorized access to sensitive files on the server.
    - Validate URLs to ensure they point to legitimate and secure audio sources.

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

## Development Status

The **Multi-AI Mattermost Bot** is actively under development. Currently, it offers foundational functionalities, including:

- **Text Interactions:** Engaging in conversations and responding to user queries.
- **Image Processing:** Analyzing and responding to image-related commands.
- **Audio Transcription:** Transcribing audio files using integrated transcription services.

While these core features are operational, the project is evolving to incorporate advanced capabilities and optimizations to enhance user experience, scalability, and maintainability.

## Upcoming Features

The following enhancements and features are planned to elevate the bot's functionality and user experience:

- **Threaded Responses:**
  - **Description:** Modify the bot to post responses as threaded replies to specific messages instead of sending new standalone messages. This will organize conversations more coherently within Mattermost channels.
  - **Benefit:** Enhances readability and maintains context within ongoing discussions.

- **Comprehensive Thread Support:**
  - **Description:** Extend the bot's ability to handle entire threads, allowing it to maintain and reference conversation history within specific threads.
  - **Benefit:** Enables more meaningful and context-aware interactions within complex conversations.

- **Dockerization:**
  - **Description:** Containerize the application using Docker to ensure consistent deployment environments and simplify the setup process.
  - **Benefit:** Facilitates easier deployment across different systems and enhances scalability.

- **Organized Client Libraries:**
  - **Description:** Create a dedicated `clients` directory to house all AI service client modules (e.g., OpenAI, Claude, Hugging Face), promoting better project structure.
  - **Benefit:** Improves code organization, making it easier to manage and integrate additional AI services in the future.

- **File Upload Support:**
  - **Description:** Enable the bot to handle file uploads alongside text, images, and audio. Allow users to upload files (e.g., documents, PDFs) and interact with the bot using these files in combined inputs.
  - **Benefit:** Expands the bot's utility by allowing it to process and respond to a wider variety of user inputs, similar to platforms like ChatGPT.

- **Enhanced Plugin Architecture:**
  - **Description:** Refine the plugin system to support a more modular and scalable architecture. This includes improving the `chat_plugin` and other existing plugins to better adhere to the plugin architecture, facilitating easier integration and management of additional plugins.
  - **Benefit:** Increases the bot's flexibility and maintainability, making it simpler to add or update functionalities through plugins.

- **Multi-Service Integration:**
  - **Description:** Integrate additional AI services (e.g., Claude, Hugging Face) to diversify the bot's capabilities and offer users a broader range of AI-powered features.
  - **Benefit:** Enhances the bot's functionality by leveraging various AI models and services, catering to diverse user needs.

- **Comprehensive Testing and Documentation:**
  - **Description:** Develop extensive unit and integration tests to ensure reliability and maintain comprehensive documentation to assist users and contributors.
  - **Benefit:** Ensures code quality and facilitates easier onboarding for new contributors, promoting sustainable project growth.

- **Security Enhancements:**
  - **Description:** Implement robust authentication and authorization mechanisms to secure interactions and data handling within the bot.
  - **Benefit:** Protects user data and ensures that only authorized users can access and interact with the bot's functionalities.

- **Real-Time Notifications and Analytics:**
  - **Description:** Provide real-time updates and insights into bot usage and performance, aiding in monitoring and optimization.
  - **Benefit:** Allows for proactive maintenance and optimization based on usage patterns and performance metrics.

## Contributing

Contributions are welcome! Please open issues and submit pull requests for any enhancements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).
