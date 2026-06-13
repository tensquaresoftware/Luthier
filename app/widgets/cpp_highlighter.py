"""Minimal C++ syntax highlighter for the templates editor."""

import re

from PySide6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat

_KEYWORDS = (
    "alignas alignof and auto bool break case catch char class const constexpr "
    "continue default delete do double else enum explicit extern false float for "
    "friend goto if inline int long mutable namespace new noexcept nullptr operator "
    "override final private protected public return short signed sizeof static struct "
    "switch template this throw true try typedef typename union unsigned using virtual "
    "void volatile while"
).split()


def _fmt(color: str, italic: bool = False) -> QTextCharFormat:
    fmt = QTextCharFormat()
    fmt.setForeground(QColor(color))
    fmt.setFontItalic(italic)
    return fmt


def _build_rules() -> list:
    keywords = r"\b(?:" + "|".join(_KEYWORDS) + r")\b"
    return [
        (re.compile(r"\b[A-Z][A-Za-z0-9_]*\b"), _fmt("#82aaff")),
        (re.compile(keywords), _fmt("#c792ea")),
        (re.compile(r"\b\d[\w.]*\b"), _fmt("#f78c6c")),
        (re.compile(r'"[^"\\]*(?:\\.[^"\\]*)*"|\'(?:\\.|[^\'])\''), _fmt("#c3e88d")),
        (re.compile(r"^\s*#\s*\w+"), _fmt("#89ddff")),
        (re.compile(r"//[^\n]*"), _fmt("#6a737d", italic=True)),
    ]


class CppHighlighter(QSyntaxHighlighter):
    """Regex-based highlighter: keywords, types, strings, numbers, comments."""

    def __init__(self, document):
        super().__init__(document)
        self._rules = _build_rules()
        self._comment = _fmt("#6a737d", italic=True)
        self._open = re.compile(r"/\*")
        self._close = re.compile(r"\*/")

    def highlightBlock(self, text: str) -> None:
        for pattern, fmt in self._rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), fmt)
        self._apply_block_comments(text)

    def _apply_block_comments(self, text: str) -> None:
        self.setCurrentBlockState(0)
        start = 0 if self.previousBlockState() == 1 else self._find(self._open, text, 0)
        while start >= 0:
            closing = self._close.search(text, start)
            if not closing:
                self.setCurrentBlockState(1)
                self.setFormat(start, len(text) - start, self._comment)
                return
            self.setFormat(start, closing.end() - start, self._comment)
            start = self._find(self._open, text, closing.end())

    @staticmethod
    def _find(pattern, text: str, offset: int) -> int:
        match = pattern.search(text, offset)
        return match.start() if match else -1
