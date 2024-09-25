import logging
from src.plugins import get_plugins

logger = logging.getLogger(__name__)

class CommandHandler:
    def __init__(self):
        self.plugins = get_plugins()
        self.commands = {
            'help': self.help_command,
            # Add more built-in commands here
        }

    def execute(self, command, args, channel_id, user_id):
        if command in self.commands:
            return self.commands[command](args, channel_id, user_id)
        elif command in self.plugins:
            return self.plugins[command].execute(args, channel_id, user_id)
        else:
            return f"Unknown command: {command}"

    def help_command(self, args, channel_id, user_id):
        if args:
            plugin_name = args[0].lower()
            if plugin_name in self.plugins:
                plugin = self.plugins[plugin_name]
                return f"{plugin.name}: {plugin.description}\nUsage: {plugin.usage}"
            else:
                return f"Unknown plugin: {plugin_name}"

        help_text = "Available commands:\n"
        help_text += "  /help [plugin_name] - Show this help message or get help for a specific plugin\n"
        # Add help text for other built-in commands here

        for plugin in self.plugins.values():
            help_text += f"  /{plugin.name} - {plugin.description}\n"

        return help_text

    # Add more command methods here