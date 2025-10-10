import json
import os.path
import threading

class Settings:
    _instance = None
    _initialized = False
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._data = {}
        self.load_from_json(os.path.join(os.getcwd(), "settings.json"))

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __contains__(self, item):
        return item in self._data

    def set(self, key, value):
        self._data[key] = value

    def get(self, key, default=None):
        return self._data.get(key, default)

    def load_from_json(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError("JSON data is not a dictionary")
                self._data.update(data)
        except FileNotFoundError:
            print(f"[WARN] File {filepath} not found")
        except json.JSONDecodeError as e:
            print(f"[ERROR] Error decoding JSON file {filepath}: {e}")