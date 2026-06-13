"""Main window: sidebar, page stack, and the Generate action bar."""

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from pathlib import Path

from app.pages.preferences import PreferencesPage
from app.pages.project import ProjectPage
from app.pages.templates import TemplatesPage
from app.sidebar import Sidebar, SIDEBAR_WIDTH
from core import plugin_settings, templates_store
from core.preferences import Preferences
from core.project_generator import ProjectGenerator
from core.project_reader import read_project


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Luthier")
        self.resize(940, 660)
        self.setMinimumSize(900, 650)
        self._prefs = Preferences(Preferences.default_path())
        self._prefs.load()
        self._generator = ProjectGenerator(overrides=templates_store.overrides_dir())
        self._defaults = self._form_defaults()
        self._build_ui()
        self._show_load_error_if_any()
        self._refresh_generate_enabled()

    def _form_defaults(self) -> dict:
        keys = ("manufacturer", "manufacturerCode", "pluginCode", "destination")
        return {key: self._prefs.get(key) for key in keys}

    def _build_ui(self) -> None:
        central = QWidget()
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addLayout(self._build_body(), 1)
        root.addWidget(self._build_bottom_bar())
        self.setCentralWidget(central)

    def _build_body(self) -> QHBoxLayout:
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        self._sidebar = Sidebar()
        self._stack = self._build_stack()
        self._sidebar.sectionChanged.connect(self._stack.setCurrentIndex)
        body.addWidget(self._sidebar)
        body.addWidget(self._stack, 1)
        return body

    def _build_stack(self) -> QStackedWidget:
        stack = QStackedWidget()
        self._project_page = ProjectPage(self._defaults, plugin_settings.bundle_id, self._prefs)
        self._prefs_page = PreferencesPage(self._prefs)
        self._templates_page = TemplatesPage()
        stack.addWidget(self._project_page)
        stack.addWidget(self._prefs_page)
        stack.addWidget(self._templates_page)
        self._project_page.validityChanged.connect(self._refresh_generate_enabled)
        return stack

    def _build_bottom_bar(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("BottomBar")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 8, 16, 8)
        layout.setSpacing(12)
        self._open = QPushButton("Open Project…")
        self._open.setFixedWidth(SIDEBAR_WIDTH)
        self._open.clicked.connect(self._on_open)
        self._status = QLabel("")
        self._generate = QPushButton("Generate Project")
        self._generate.setObjectName("GenerateButton")
        self._generate.clicked.connect(self._on_generate)
        layout.addWidget(self._open)
        layout.addWidget(self._status, 1)
        layout.addWidget(self._generate)
        return bar

    def _show_load_error_if_any(self) -> None:
        if self._generator.error:
            self._set_status(self._generator.error, ok=False)

    def _refresh_generate_enabled(self, _valid: bool = False) -> None:
        ready = self._generator.error is None and self._project_page.is_valid()
        self._generate.setEnabled(ready)

    def _on_generate(self) -> None:
        values = self._project_page.values()
        if not self._confirm_overwrite(values):
            return
        self._run_generation(values)

    def _on_open(self) -> None:
        start = self._prefs.get("destination") or ""
        directory = QFileDialog.getExistingDirectory(self, "Open JUCE plugin project", start)
        if directory:
            self._load_project(Path(directory))

    def _load_project(self, project_dir: Path) -> None:
        values = read_project(project_dir)
        if values is None:
            self._set_status(f"Not a JUCE plugin project: {project_dir}", ok=False)
            return
        self._project_page.load(values)
        self._prefs.update(values)
        self._set_status(f"Loaded {values['projectName']} from {project_dir}", ok=True)

    def _confirm_overwrite(self, values: dict) -> bool:
        if not self._generator.project_exists(values["destinationDir"], values["projectName"]):
            return True
        answer = QMessageBox.question(
            self,
            "Overwrite project",
            f"A folder named '{values['projectName']}' already exists. Overwrite it?",
        )
        return answer == QMessageBox.Yes

    def _run_generation(self, values: dict) -> None:
        try:
            project_dir = self._generator.generate(values, self._project_page.config())
        except Exception as error:
            self._set_status(f"Generation failed: {error}", ok=False)
            return
        self._set_status(f"Project generated at {project_dir}", ok=True)

    def _set_status(self, text: str, ok: bool) -> None:
        self._status.setText(text)
        self._status.setObjectName("StatusOk" if ok else "StatusErr")
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)
