"""Read and override the editable C++ source templates.

Defaults ship in Templates/Source/. User overrides live in the app config
directory so a packaged (read-only) install can still be customized.
"""

from pathlib import Path

from PySide6.QtCore import QStandardPaths

from core.project_generator import templates_dir

SOURCE_FILES = (
    "PluginProcessor.h",
    "PluginProcessor.cpp",
    "PluginEditor.h",
    "PluginEditor.cpp",
)


def overrides_dir() -> Path:
    location = QStandardPaths.StandardLocation.AppConfigLocation
    base = QStandardPaths.writableLocation(location)
    return Path(base) / "templates" / "Source"


def has_override(name: str) -> bool:
    return (overrides_dir() / name).exists()


def read_default(name: str) -> str:
    return (templates_dir() / "Source" / name).read_text(encoding="utf-8")


def read_effective(name: str) -> str:
    override = overrides_dir() / name
    return override.read_text(encoding="utf-8") if override.exists() else read_default(name)


def save_override(name: str, content: str) -> None:
    target = overrides_dir() / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def reset(name: str) -> None:
    (overrides_dir() / name).unlink(missing_ok=True)
