import json


input_data = '{"one": ["http", "yandex.ru"], "two": ["https", "google.com"]}'
output_data = json.loads(input_data)


if __name__ == "__main__":
    print(output_data)
