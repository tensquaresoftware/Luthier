"""Label + multi-line text field for optional, one-entry-per-line values."""

from PySide6.QtWidgets import QHBoxLayout, QPlainTextEdit, QWidget

from app.widgets.validated_field import make_field_label

_FIELD_HEIGHT = 64


class TextAreaField(QWidget):
    """A labelled multi-line editor; the value is the raw text (one item per line)."""

    def __init__(self, label: str, placeholder: str = ""):
        super().__init__()
        self._edit = QPlainTextEdit()
        self._edit.setPlaceholderText(placeholder)
        self._edit.setFixedHeight(_FIELD_HEIGHT)
        self._build_ui(label)

    def value(self) -> str:
        return self._edit.toPlainText()

    def set_value(self, value: str) -> None:
        self._edit.setPlainText(value)

    def _build_ui(self, label: str) -> None:
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 4, 0, 4)
        row.setSpacing(8)
        row.addWidget(make_field_label(label))
        row.addWidget(self._edit, 1)
        row.addSpacing(24)
