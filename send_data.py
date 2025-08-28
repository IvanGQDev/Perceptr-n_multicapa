import requests
url = "http://localhost:3000/usuarios"

def post_data(nuevo_usuario):
    response = requests.post(url, json=nuevo_usuario)

    if response.status_code == 200:
        print("Usuario Guardado", response.json())
    else:
        print("Error", response.status_code,response.text)