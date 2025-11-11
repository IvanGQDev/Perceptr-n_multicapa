import requests
#url = "http://localhost:3000/usuarios"
url = "https://api-ig4jmd5a5q-uc.a.run.app/usuarios"
#url = "http://127.0.0.1:5001/conflikta-2ea2d/us-central1/api/usuarios"

def post_data(nuevo_usuario):
    response = requests.post(url, json=nuevo_usuario)

    if response.status_code == 200:
        print("Usuario Guardado", response.json())
    else:
        print("Error", response.status_code,response.text)