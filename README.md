# Luthier

A Projucer-inspired desktop GUI for creating, reopening, and configuring CMake-based JUCE audio plugin projects.

![Luthier](Docs/Luthier.png)

Luthier is a self-contained [PySide6](https://doc.qt.io/qtforpython/) desktop app that generates ready-to-build, CMake-based JUCE plugin projects (AU / VST3 / Standalone): fill a form, validate inline, and generate. It can also reopen an existing generated project to tweak and regenerate it, and stores your defaults in a persistent preferences file — no hand-editing of configuration scripts.

## Features

- **Project** — one scrollable page for the whole plugin:
  - identity: technical/display names, version, manufacturer, copyright, website, e-mail, plugin & manufacturer codes, auto-computed bundle ID, with live inline validation;
  - plugin type (Synthesizer, Audio Effect, MIDI Effect) and formats (AU, VST3, Standalone);
  - compilation: C++ standard, preprocessor definitions, header search paths;
  - artefacts: copy to system plugin folders and/or a central per-OS directory.
- **Preferences** — persistent defaults (identity + default artefact settings) stored as JSON in the OS configuration directory.
- **Templates** — view, edit, replace, or reset the C++ source templates (`PluginProcessor` / `PluginEditor`) used for new projects; overrides persist on disk.
- **Reopen a project** — read an existing generated project back into the form and regenerate it in place.

## Requirements

- Python 3.11+
- PySide6 (`pip install -r requirements.txt`)
- No external dependencies beyond PySide6: the CMake project templates ship inside Luthier (`Templates/`) and the generation engine is built in (`core/`).

## Run from source

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

Check that the bundled templates are reachable (headless):

```bash
.venv/bin/python main.py --check
```

## Build a standalone app

PyInstaller bundles the templates and resources into a self-contained app.
It does not cross-compile — build on each target OS.

```bash
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/pyinstaller Build/luthier.spec --noconfirm --distpath Dist --workpath Build
```

The same `Build/luthier.spec` works on all platforms:

| OS      | Output                       |
| ------- | ---------------------------- |
| macOS   | `Dist/Luthier.app`           |
| Windows | `Dist/Luthier/Luthier.exe`   |
| Linux   | `Dist/Luthier/Luthier`       |

On Windows, activate the virtual environment with `.venv\Scripts\activate` and
run `pyinstaller Build\luthier.spec`.

## License

Luthier is released under the [MIT License](LICENSE).

Packaged builds are distributed with Qt (via PySide6) under the LGPLv3 — see [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
