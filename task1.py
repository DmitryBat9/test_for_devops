import sys


def format_text(text: str, width: int = 70) -> str:
    """Переносит текст по словам, не превышая заданную ширину строки."""

    if width <= 0:
        raise ValueError("текст должен быть не пустым")

    words = text.split()

    for word in words:
        if len(word) > width:
            raise ValueError(
                "есть слово длиннее допустимой ширины"
            )

    lines: list[str] = []
    current_line: list[str] = []
    current_length = 0

    for word in words:
        # Учитываем пробел перед словом, если строка уже не пустая.
        candidate_length = (
            current_length + len(word) + (1 if current_line else 0)
        )

        if candidate_length <= width:
            current_line.append(word)
            current_length = candidate_length
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)

    if current_line:
        lines.append(" ".join(current_line))

    return "\n".join(lines)


if __name__ == "__main__":
    input_text = input() # можно через stdin.read(), но тогда с прерыванием программы через Ctrl+Z -> Enter

    try:
        print(format_text(input_text))
    except ValueError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(1)