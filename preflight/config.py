"""Settings from ~/.config/preflight/.env; environment variables take priority."""

import os
from pathlib import Path

DEFAULT_ENV_PATH = Path.home() / ".config" / "preflight" / ".env"
DEFAULTS = {
    "CANVAS_BASE_URL": "https://uvg.instructure.com",
    "PREFLIGHT_TZ": "America/Guatemala",
    # Outside any repo, so auditing this repo never exposes or modifies work files.
    "PREFLIGHT_WORK": str(Path.home() / ".cache" / "preflight"),
}


class ConfigError(Exception):
    pass


def read_env_file(path):
    values = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip().strip("\"'")
    return values


def load_settings(env_path=None, environ=None, require_token=True):
    environ = os.environ if environ is None else environ
    path = Path(env_path or environ.get("PREFLIGHT_ENV") or DEFAULT_ENV_PATH)
    if require_token and not path.exists():
        raise ConfigError(f"No settings file at {path}. Copy .env.example there and add CANVAS_TOKEN.")

    settings = {**DEFAULTS, **(read_env_file(path) if path.exists() else {})}
    for key, value in environ.items():
        if key.startswith(("CANVAS_", "PREFLIGHT_")) and value:
            settings[key] = value

    if require_token and not settings.get("CANVAS_TOKEN"):
        raise ConfigError(f"CANVAS_TOKEN is empty in {path}.")
    settings["CANVAS_BASE_URL"] = settings["CANVAS_BASE_URL"].rstrip("/")
    return settings
