"""Left navigation panel switching between form sections."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QListWidget, QVBoxLayout, QWidget

from app.resources import resource_path

SECTIONS = ["Project", "Preferences", "Templates"]
SIDEBAR_WIDTH = 190
_LOGO_MARGIN = 28


class Sidebar(QWidget):
    sectionChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self.setObjectName("Sidebar")
        self.setFixedWidth(SIDEBAR_WIDTH)
        self._list = self._make_list()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 12, 8, 12)
        layout.addWidget(self._list, 1)
        layout.addWidget(self._make_logo(), 0, Qt.AlignHCenter)

    def _make_list(self) -> QListWidget:
        widget = QListWidget()
        widget.addItems(SECTIONS)
        widget.setCurrentRow(0)
        widget.currentRowChanged.connect(self.sectionChanged)
        return widget

    def _make_logo(self) -> QSvgWidget:
        logo = QSvgWidget(resource_path("luthier.svg"))
        size = logo.renderer().defaultSize()
        width = SIDEBAR_WIDTH - _LOGO_MARGIN
        logo.setFixedSize(width, round(size.height() * width / size.width()))
        return logo
