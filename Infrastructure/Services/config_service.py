import json
import os
from typing import Optional


class ConfigService:

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            config_path = os.path.join(base_dir, "config.json")
        self._config_path = config_path
        self._raw: Optional[dict] = None

    def load(self) -> dict:
        if self._raw is None:
            with open(self._config_path, "r", encoding="utf-8") as f:
                self._raw = json.load(f)
        return self._raw
