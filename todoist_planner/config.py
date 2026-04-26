"""Configuration management for todoist-planner."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


REPO_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILEPATH = REPO_DIR / 'config.yaml'


@dataclass
class TwilioConfig:
    """Twilio WhatsApp API configuration."""
    account_sid: str
    auth_token: str
    from_number: str  # Twilio WhatsApp number (e.g., "whatsapp:+14155238886")
    to_number: str    # Your WhatsApp number (e.g., "whatsapp:+33612345678")


@dataclass
class ScheduleConfig:
    """Configuration for which projects to include on different days."""
    weekday_projects: list[str] = field(default_factory=lambda: ["Mistral", "Boîte de réception"])
    weekend_projects: list[str] = field(default_factory=lambda: ["Personal", "GluGlu", "Boîte de réception"])
    num_tasks: int = 3


@dataclass
class AnthropicConfig:
    """Anthropic API configuration."""
    api_key: str


@dataclass
class Config:
    """Main configuration container."""
    twilio: TwilioConfig
    schedule: ScheduleConfig
    anthropic: AnthropicConfig | None = None


def load_config(config_path: Optional[Path] = None) -> Config:
    """Load configuration from YAML file.

    Args:
        config_path: Path to config file. Defaults to config.yaml in repo root.

    Returns:
        Config object with all settings.

    Raises:
        FileNotFoundError: If config file doesn't exist.
        ValueError: If required fields are missing.
    """
    if config_path is None:
        config_path = CONFIG_FILEPATH

    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file not found at {config_path}. "
            f"Please copy config.example.yaml to config.yaml and fill in your credentials."
        )

    with config_path.open('r') as f:
        data = yaml.safe_load(f)

    # Parse Twilio config
    twilio_data = data.get('twilio', {})
    required_twilio_fields = ['account_sid', 'auth_token', 'from_number', 'to_number']
    missing_fields = [f for f in required_twilio_fields if not twilio_data.get(f)]
    if missing_fields:
        raise ValueError(f"Missing required Twilio fields: {missing_fields}")

    twilio_config = TwilioConfig(
        account_sid=twilio_data['account_sid'],
        auth_token=twilio_data['auth_token'],
        from_number=twilio_data['from_number'],
        to_number=twilio_data['to_number'],
    )

    # Parse schedule config with defaults
    schedule_data = data.get('schedule', {})
    default_weekday = ["Mistral", "Boîte de réception"]
    default_weekend = ["Personal", "GluGlu", "Boîte de réception"]
    schedule_config = ScheduleConfig(
        weekday_projects=schedule_data.get('weekday_projects', default_weekday),
        weekend_projects=schedule_data.get('weekend_projects', default_weekend),
        num_tasks=schedule_data.get('num_tasks', 3),
    )

    # Parse Anthropic config (optional)
    anthropic_config = None
    anthropic_data = data.get('anthropic', {})
    if anthropic_data.get('api_key'):
        anthropic_config = AnthropicConfig(api_key=anthropic_data['api_key'])

    return Config(twilio=twilio_config, schedule=schedule_config, anthropic=anthropic_config)
