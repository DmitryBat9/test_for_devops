def get_value(data, path):
    """Возвращает значение из вложенного словаря по пути из ключей."""

    keys = path.split(".")
    current_value = data

    for key in keys:
        current_value = current_value[key]

    return current_value


if __name__ == "__main__":
    data = {
        "a": {
            "b": {
                "c": "+++"
            }
        }
    }

    result = get_value(data, "a.b.c")
    print(result)
