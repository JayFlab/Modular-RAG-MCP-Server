"""
Configuration loading and validation.

Reads config/settings.yaml, parses into Settings dataclass,
and validates required fields with clear error messages.
"""
import os
import yaml
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Settings:
    """Central configuration object for the entire application.

    Each section maps to a pluggable component layer.
    Only holds structure and minimal validation — no network/IO initialization.
    """
    llm: Dict[str, Any] = field(default_factory=dict)
    embedding: Dict[str, Any] = field(default_factory=dict)
    vision_llm: Dict[str, Any] = field(default_factory=dict)
    vector_store: Dict[str, Any] = field(default_factory=dict)
    splitter: Dict[str, Any] = field(default_factory=dict)
    retrieval: Dict[str, Any] = field(default_factory=dict)
    rerank: Dict[str, Any] = field(default_factory=dict)
    ingestion: Dict[str, Any] = field(default_factory=dict)
    evaluation: Dict[str, Any] = field(default_factory=dict)
    observability: Dict[str, Any] = field(default_factory=dict)
    dashboard: Dict[str, Any] = field(default_factory=dict)


# Required fields: list of (section, key) pairs that must exist
REQUIRED_FIELDS = [
    ("llm", "provider"),
    ("embedding", "provider"),
    ("vector_store", "backend"),
    ("splitter", "provider"),
]


def _resolve_env_vars(value: Any) -> Any:
    """Recursively resolve ${ENV_VAR} patterns in config values."""
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        env_var = value[2:-1]
        return os.environ.get(env_var, value)
    elif isinstance(value, dict):
        return {k: _resolve_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_resolve_env_vars(item) for item in value]
    return value


def load_settings(path: str = "config/settings.yaml") -> Settings:
    """Load settings from YAML file and validate required fields.

    Args:
        path: Path to the settings YAML file.

    Returns:
        A validated Settings instance.

    Raises:
        FileNotFoundError: If the config file doesn't exist.
        ValueError: If required fields are missing.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Configuration file not found: {path}\n"
            f"Please create it from the template or copy config/settings.yaml.example"
        )

    with open(path, "r", encoding="utf-8") as f:
        raw_config = yaml.safe_load(f)

    if not raw_config or not isinstance(raw_config, dict):
        raise ValueError(f"Configuration file is empty or invalid: {path}")

    # Resolve environment variables
    config = _resolve_env_vars(raw_config)

    # Build Settings object
    settings = Settings(
        llm=config.get("llm", {}),
        embedding=config.get("embedding", {}),
        vision_llm=config.get("vision_llm", {}),
        vector_store=config.get("vector_store", {}),
        splitter=config.get("splitter", {}),
        retrieval=config.get("retrieval", {}),
        rerank=config.get("rerank", {}),
        ingestion=config.get("ingestion", {}),
        evaluation=config.get("evaluation", {}),
        observability=config.get("observability", {}),
        dashboard=config.get("dashboard", {}),
    )

    # Validate
    validate_settings(settings)

    return settings


def validate_settings(settings: Settings) -> None:
    """Validate that all required fields are present.

    Raises:
        ValueError: With a clear message listing all missing fields.
    """
    missing = []

    for section_name, key in REQUIRED_FIELDS:
        section = getattr(settings, section_name, None)
        if section is None or not isinstance(section, dict):
            missing.append(f"{section_name}.{key} (section '{section_name}' is missing)")
        elif key not in section or section[key] is None:
            missing.append(f"{section_name}.{key}")

    if missing:
        fields_str = "\n  - ".join(missing)
        raise ValueError(
            f"Missing required configuration fields:\n  - {fields_str}\n"
            f"Please check config/settings.yaml and ensure all required fields are set."
        )
