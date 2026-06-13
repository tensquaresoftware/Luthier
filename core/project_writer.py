"""Write a generated project tree from the template files."""

import shutil
from pathlib import Path
from typing import Optional

from core import rendering

_RENDERED = (
    "CMakeLists.txt",
    "project-configuration.cmake",
    ".vscode/settings.json",
    ".vscode/tasks.json",
    ".vscode/launch.json",
    "README.md",
)

_TOKENIZED = (
    "Source/PluginProcessor.h",
    "Source/PluginProcessor.cpp",
    "Source/PluginEditor.h",
    "Source/PluginEditor.cpp",
)

_VERBATIM = (
    ".vscode/extensions.json",
    ".cursorrules",
    ".gitignore",
    "CMakeUserPresets.json",
    "CMake/CopyVst3Elevated.ps1",
)


class ProjectWriter:
    """Renders and writes every project file into the destination directory."""

    def __init__(self, templates_dir: Path, project_dir: Path, overrides: Optional[Path] = None):
        self._templates = templates_dir
        self._project = project_dir
        self._overrides = overrides

    def write(self, context: dict, tokens: dict) -> None:
        self._reset_project_dir()
        for relative in _RENDERED:
            self._write(relative, rendering.render(self._read(relative), context))
        for relative in _TOKENIZED:
            self._write(relative, rendering.render_tokens(self._read(relative), tokens))
        for relative in _VERBATIM:
            self._write(relative, self._read(relative))

    def _reset_project_dir(self) -> None:
        if self._project.exists():
            shutil.rmtree(self._project)

    def _read(self, relative: str) -> str:
        source = self._override_for(relative) or self._templates / relative
        return source.read_text(encoding="utf-8")

    def _override_for(self, relative: str) -> Optional[Path]:
        if not self._overrides or relative not in _TOKENIZED:
            return None
        candidate = self._overrides / Path(relative).name
        return candidate if candidate.exists() else None

    def _write(self, relative: str, content: str) -> None:
        target = self._project / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
