from src.plugins.base_plugin import BasePlugin
from src.openai_client import generate_chat_response as openai_chat
from src.config import CHAT_SERVICE, BOT_INSTRUCTION, BOT_CONTEXT_MSG

class ChatPlugin(BasePlugin):
    name = "chat"
    description = "Chat with the AI assistant"
    usage = "Just type your message to chat, or use /chat [--service <service_name>] <message>"

    def __init__(self):
        self.conversation_context = {}
        self.services = {
            "openai": openai_chat,
            # Add other chat services here, e.g.:
            # "gpt4all": gpt4all_chat,
            # "huggingface": huggingface_chat,
        }
        self.default_service = CHAT_SERVICE

    def execute(self, args, channel_id, user_id):
        service = self.default_service
        if args and args[0] == "--service":
            if len(args) < 3:
                return "Please specify a service name and a message after --service"
            service = args[1]
            message = " ".join(args[2:])
            if service not in self.services:
                return f"Unknown service: {service}. Available services: {', '.join(self.services.keys())}"
        else:
            message = " ".join(args)

        # Get or create conversation context
        context = self.conversation_context.get(user_id, [])
        context.append({"role": "user", "content": message})

        # Trim context if it's too long
        if len(context) > BOT_CONTEXT_MSG:
            context = context[-BOT_CONTEXT_MSG:]

        # Prepare messages for the chat service
        messages = [{"role": "system", "content": BOT_INSTRUCTION}] + context

        # Generate response
        chat_function = self.services[service]
        response = chat_function(messages)

        # Update context
        context.append({"role": "assistant", "content": response})
        self.conversation_context[user_id] = context

        return f"[{service}] {response}"

    def initialize(self):
        print(f"Initialized {self.name} plugin with default service: {self.default_service}")

    def cleanup(self):
        print(f"Cleaning up {self.name} plugin")