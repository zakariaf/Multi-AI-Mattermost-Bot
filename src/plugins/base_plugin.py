from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @property
    @abstractmethod
    def usage(self):
        pass

    @abstractmethod
    def execute(self, args, channel_id, user_id):
        pass

    def initialize(self):
        # Default implementation, can be overridden by subclasses
        pass

    def cleanup(self):
        # Default implementation, can be overridden by subclasses
        pass