import json


inData = '{"one": ["http", "yandex.ru"], "two": ["https", "google.com"]}'

outData = json.loads(inData)

print(outData)
