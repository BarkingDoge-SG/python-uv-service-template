import os
import yaml
import importlib
from dotenv import load_dotenv
from pathlib import Path

from . import get_env      # noqa


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class ConfigLoader:
    DEFAULT_PATH = PROJECT_ROOT / "config.yaml"

    @staticmethod
    def load_config():
        """
        load config.yaml and return a dict
        """
        if not os.path.exists(ConfigLoader.DEFAULT_PATH):
            raise FileNotFoundError(f"Config file not found: {ConfigLoader.DEFAULT_PATH}")

        with open(ConfigLoader.DEFAULT_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def load_module(module_name: str):
        """
        read some configuration from config.yaml
        e.g. load_module("milvus") / load_module("models")
        """
        config = ConfigLoader.load_config()
        if module_name not in config:
            raise KeyError(f"Module '{module_name}' not found in config file.")
        return config[module_name]


class ModelLoader:
    def __init__(self):
        load_dotenv()
        self.model_config = ConfigLoader.load_module("models")

    def load_model(self, model_key: str):
        model_cfg = self.model_config.get(model_key)
        if not model_cfg:
            raise ValueError(f"Model config '{model_key}' not found in config.yaml.")

        model_name = model_cfg.get("model_name")
        class_name = model_cfg.get("class_name", "BGEM3FlagModel")
        params = model_cfg.get("config", {})

        module = importlib.import_module("FlagEmbedding")
        model_class = getattr(module, class_name)

        return model_class(model_name, **params)


