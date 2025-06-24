"""Simple routing logic based on message type or other fields."""
from typing import Callable
import yaml
from importlib import import_module

from .parser import get_message_type


class Router:
    def __init__(self):
        self._routes: dict[str, Callable] = {}

    def add_route(self, message_type: str, handler: Callable):
        self._routes[message_type] = handler

    def load_from_yaml(self, path: str):
        """Load routing rules from a YAML file."""
        with open(path, "r") as fh:
            data = yaml.safe_load(fh) or {}
        for msg_type, handler_path in data.get("routes", {}).items():
            module_name, func_name = handler_path.rsplit(".", 1)
            module = import_module(module_name)
            handler = getattr(module, func_name)
            self.add_route(msg_type, handler)

    def route(self, message):
        message_type = get_message_type(message)
        handler = self._routes.get(message_type)
        if handler:
            handler(message)
        else:
            self.default_handler(message)

    def default_handler(self, message):
        print(f"No handler for {get_message_type(message)}")
