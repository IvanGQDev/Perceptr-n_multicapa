import json
import chardet

def cargar_json(file_path):
    with open(file_path, "rb") as f:
        raw_data = f.read(10000)
        encoding_detected = chardet.detect(raw_data)["encoding"]
    with open(file_path, "r", encoding=encoding_detected) as f:
        return json.load(f)
