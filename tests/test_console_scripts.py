import importlib
import pathlib

import pytest

tomllib = pytest.importorskip("tomllib")
ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_every_console_script_target_exists_and_is_callable():
    """F-34 regression: `fanus = "fanus.main:main"` pointed at a function that did not
    exist, so the installed `fanus` command crashed. Every entry point must resolve."""
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    scripts = data["project"].get("scripts", {})
    assert scripts, "no console scripts declared"
    for name, target in scripts.items():
        module_name, func_name = target.split(":")
        module = importlib.import_module(module_name)
        assert callable(getattr(module, func_name, None)), f"{name} -> {target} does not resolve"
