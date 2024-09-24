from config import (
    MATTERMOST_URL,
    MATTERMOST_TOKEN,
    MATTERMOST_BOTNAME,
    OPENAI_API_KEY,
    OPENAI_API_BASE,
    OPENAI_MODEL_NAME,
    OPENAI_MAX_TOKENS,
    OPENAI_TEMPERATURE,
    BOT_CONTEXT_MSG,
    BOT_INSTRUCTION,
    PLUGINS
)

def test_config():
    assert MATTERMOST_URL is not None, "MATTERMOST_URL is not set."
    assert MATTERMOST_TOKEN is not None, "MATTERMOST_TOKEN is not set."
    assert OPENAI_API_KEY is not None, "OPENAI_API_KEY is not set."
    print("All environment variables are loaded correctly.")

if __name__ == "__main__":
    test_config()