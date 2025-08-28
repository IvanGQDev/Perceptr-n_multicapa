import uuid

def generar_id():
    return str(uuid.uuid4())

def convertir_posiciones(track_data):
    posiciones = {}
    for key, val in track_data.items():
        coords = val.split()
        posiciones[key] = {
            'x': float(coords[0].split('=')[1]),
            'y': float(coords[1].split('=')[1]),
            'z': float(coords[2].split('=')[1])
        }
    return posiciones
