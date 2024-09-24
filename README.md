# ChatGPT-Mattermost Bot

A comprehensive Python-based bot that integrates OpenAI's ChatGPT with Mattermost, enabling intelligent and automated interactions within your team's communication channels. This bot leverages the full capabilities of the OpenAI API, including chat, audio, file uploads, image generation, and more.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create and Activate a Virtual Environment](#2-create-and-activate-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Configure Environment Variables](#4-configure-environment-variables)
- [Usage](#usage)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
- [Plugins](#plugins)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Automated Responses**: Instantly responds to user queries within Mattermost channels.
- **Rich Media Support**: Handles audio, file uploads, and image generation using OpenAI's APIs.
- **Plugin System**: Extendable architecture allowing for custom functionalities.
- **Secure Configuration**: Manages sensitive information through environment variables.
- **Dockerized Deployment**: Simplifies deployment with Docker support.

## Prerequisites

Before setting up the ChatGPT-Mattermost Bot, ensure you have the following:

- **Python 3.8+**: Ensure Python is installed on your system. [Download Python](https://www.python.org/downloads/)
- **Git**: For version control. [Download Git](https://git-scm.com/downloads)
- **Mattermost Server Access**: Administrative access to your Mattermost instance.
- **OpenAI API Key**: Obtain an API key from [OpenAI](https://platform.openai.com/account/api-keys).

## Installation

### 1. Clone the Repository

Begin by cloning the repository to your local machine:

```bash
git clone https://github.com/yourusername/chatgpt-mattermost-bot.git
cd chatgpt-mattermost-bot
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
MATTERMOST_BOTNAME=@chatgpt-bot

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4
OPENAI_MAX_TOKENS=1500
OPENAI_TEMPERATURE=0.7

# Bot Configuration
BOT_CONTEXT_MSG=50
BOT_INSTRUCTION=You are a helpful assistant.

# Optional: Plugins Configuration
PLUGINS=image-plugin,graph-plugin,audio-plugin,files-plugin
```

**Notes:**

- **MATTERMOST_URL**: Your Mattermost server URL.
- **MATTERMOST_TOKEN**: The access token obtained from creating a Mattermost bot account.
- **MATTERMOST_BOTNAME**: Desired bot username (e.g., `@chatgpt-bot`).
- **OPENAI_API_KEY**: Your OpenAI API key.
- **OPENAI_API_BASE**: Base URL for OpenAI API (default is `https://api.openai.com/v1`).
- **OPENAI_MODEL_NAME**: The OpenAI model to use (e.g., `gpt-4`).
- **OPENAI_MAX_TOKENS**: Maximum number of tokens for OpenAI responses.
- **OPENAI_TEMPERATURE**: Sampling temperature for OpenAI responses.
- **BOT_CONTEXT_MSG**: Number of previous messages to include in the context.
- **BOT_INSTRUCTION**: System-level instructions for the bot.
- **PLUGINS**: Comma-separated list of plugins to enable.

**Security Reminder:** Ensure that the `.env` file is **never** committed to version control. It's already included in `.gitignore`.

## Usage

Once the environment is configured, you can start the bot:

```bash
python src ....
```

**Note:** Ensure that your virtual environment is activated before running the bot.

## Configuration

### Environment Variables

All configurations are managed via environment variables defined in the `.env` file. Here's a breakdown of each variable:

- **Mattermost Configuration:**
  - `MATTERMOST_URL`: URL of your Mattermost server.
  - `MATTERMOST_TOKEN`: Access token for the Mattermost bot.
  - `MATTERMOST_BOTNAME`: Username of the bot (e.g., `@chatgpt-bot`).

- **OpenAI Configuration:**
  - `OPENAI_API_KEY`: API key for accessing OpenAI services.
  - `OPENAI_API_BASE`: Base endpoint for OpenAI API.
  - `OPENAI_MODEL_NAME`: Specifies the OpenAI model to use.
  - `OPENAI_MAX_TOKENS`: Sets the maximum tokens for responses.
  - `OPENAI_TEMPERATURE`: Controls the randomness of responses.

- **Bot Configuration:**
  - `BOT_CONTEXT_MSG`: Number of previous messages included in the context for generating responses.
  - `BOT_INSTRUCTION`: System prompt guiding the bot's behavior.

- **Plugins Configuration:**
  - `PLUGINS`: Enables specific plugins by listing them comma-separated.

## Plugins

The bot supports a modular plugin system, allowing you to extend its functionalities. Available plugins include:

- **Image Plugin (`image-plugin`)**: Generates images based on descriptions.
- **Graph Plugin (`graph-plugin`)**: Creates graphs from data or descriptions.
- **Audio Plugin (`audio-plugin`)**: Processes and generates audio content.
- **Files Plugin (`files-plugin`)**: Handles file uploads and management.

To enable or disable plugins, modify the `PLUGINS` variable in the `.env` file accordingly.

## Development

### Adding New Plugins

1. **Create a New Plugin File:**

   ```bash
   touch src/plugins/YourNewPlugin.py
   ```

2. **Implement the Plugin:**

   Define your plugin by extending the base plugin class.

3. **Register the Plugin:**

   Update the bot service to recognize and initialize your new plugin.

### Testing

Before deploying, ensure that all functionalities work as expected by writing and running tests.

## Deployment

For production deployment, consider containerizing the application using Docker and orchestrating with tools like Docker Compose or Kubernetes. Ensure that environment variables are securely managed and that the bot has the necessary permissions within Mattermost.

## Contributing

Contributions are welcome! Please open issues and submit pull requests for any enhancements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).
