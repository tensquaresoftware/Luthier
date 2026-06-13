"""Template rendering: substitute project variables into template content."""


def render(content: str, context: dict) -> str:
    """Fill a str.format template (literal braces are written as {{ }})."""
    return content.format(**context)


def render_tokens(content: str, tokens: dict) -> str:
    """Replace @KEY@ placeholders so source files stay valid C++ when edited."""
    for key, value in tokens.items():
        content = content.replace(f"@{key}@", value)
    return content
