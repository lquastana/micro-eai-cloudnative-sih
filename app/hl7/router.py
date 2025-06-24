"""Simple routing logic based on message type or other fields."""
from typing import Callable

from .parser import get_message_type


class Router:
    def __init__(self):
        self._routes: dict[str, Callable] = {}

    def add_route(self, message_type: str, handler: Callable):
        self._routes[message_type] = handler

    def route(self, message):
        message_type = get_message_type(message)
        handler = self._routes.get(message_type)
        if handler:
            handler(message)
        else:
            self.default_handler(message)

    def default_handler(self, message):
        print(f"No handler for {get_message_type(message)}")
