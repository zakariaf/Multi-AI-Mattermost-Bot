import importlib
import logging
from src.config import PLUGINS

logger = logging.getLogger(__name__)

def get_plugins():
    plugins = {}
    for plugin_name in PLUGINS:
        try:
            module = importlib.import_module(f"src.plugins.{plugin_name}_plugin")
            plugin_class = getattr(module, f"{plugin_name.capitalize()}Plugin")
            plugin = plugin_class()
            plugins[plugin.name] = plugin
            plugin.initialize()
        except (ImportError, AttributeError) as e:
            logger.error(f"Failed to load plugin {plugin_name}: {str(e)}")
    return plugins