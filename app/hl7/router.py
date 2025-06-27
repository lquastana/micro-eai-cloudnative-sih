"""Simple routing logic based on message type or other fields."""
from typing import Callable, List, Optional, Dict
import yaml
from importlib import import_module

from .parser import get_message_type


class Router:
    def __init__(self):
        self._rules: List[Dict] = []

    def add_route(
        self,
        message_type: str,
        handler: Callable,
        field: Optional[str] = None,
        equals: Optional[str] = None,
    ):
        self._rules.append(
            {"type": message_type, "handler": handler, "field": field, "equals": equals}
        )

    def load_from_yaml(self, path: str):
        """Load routing rules from a YAML file."""
        with open(path, "r") as fh:
            data = yaml.safe_load(fh) or {}

        routes = data.get("routes", [])
        if isinstance(routes, dict):
            for msg_type, handler_path in routes.items():
                module_name, func_name = handler_path.rsplit(".", 1)
                module = import_module(module_name)
                handler = getattr(module, func_name)
                self.add_route(msg_type, handler)
        else:
            for rule in routes:
                handler_path = rule["handler"]
                module_name, func_name = handler_path.rsplit(".", 1)
                module = import_module(module_name)
                handler = getattr(module, func_name)
                self.add_route(
                    rule["type"], handler, rule.get("field"), rule.get("equals")
                )

    def route(self, message):
        message_type = get_message_type(message)
        for rule in self._rules:
            if rule["type"] != message_type:
                continue
            if rule["field"]:
                value = self._get_field(message, rule["field"])
                if value != rule.get("equals"):
                    continue
            rule["handler"](message)
            return
        self.default_handler(message)

    def _get_field(self, message, path: str):
        seg, index = path.split(".")
        try:
            segment = getattr(message, seg)
            field = getattr(segment, f"{seg}_{index}")
            return field.to_er7()
        except Exception:
            return None

    def default_handler(self, message):
        print(f"No handler for {get_message_type(message)}")
