import pytest

from preflight.config import ConfigError, load_settings


def write_env(tmp_path, text):
    path = tmp_path / ".env"
    path.write_text(text, encoding="utf-8")
    return path


def test_reads_env_file_and_trims_base_url(tmp_path):
    env = write_env(tmp_path, "# comment\nCANVAS_BASE_URL=https://x.test/\nCANVAS_TOKEN=abc\n")
    settings = load_settings(env_path=env, environ={})
    assert settings["CANVAS_TOKEN"] == "abc"
    assert settings["CANVAS_BASE_URL"] == "https://x.test"


def test_environment_overrides_file(tmp_path):
    env = write_env(tmp_path, "CANVAS_TOKEN=from-file\n")
    settings = load_settings(env_path=env, environ={"CANVAS_TOKEN": "from-env"})
    assert settings["CANVAS_TOKEN"] == "from-env"


def test_defaults_when_only_token_is_set(tmp_path):
    settings = load_settings(env_path=write_env(tmp_path, "CANVAS_TOKEN=abc\n"), environ={})
    assert settings["CANVAS_BASE_URL"] == "https://uvg.instructure.com"
    assert settings["PREFLIGHT_TZ"] == "America/Guatemala"


def test_missing_token_names_the_file(tmp_path):
    env = write_env(tmp_path, "CANVAS_TOKEN=\n")
    with pytest.raises(ConfigError) as error:
        load_settings(env_path=env, environ={})
    assert str(env) in str(error.value)


def test_missing_file_is_a_config_error(tmp_path):
    with pytest.raises(ConfigError):
        load_settings(env_path=tmp_path / "nope.env", environ={})


def test_token_is_optional_for_commands_that_do_not_call_canvas(tmp_path):
    settings = load_settings(env_path=tmp_path / "nope.env", environ={"PREFLIGHT_TZ": "UTC"}, require_token=False)
    assert settings["PREFLIGHT_TZ"] == "UTC"
    assert "CANVAS_TOKEN" not in settings
