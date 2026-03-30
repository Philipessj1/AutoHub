import requests

def restart_remote(ip):
    url = f"http://{ip}:5000/restart-network"

    try:
        response = requests.get(url, timeout=10)
        print(response.json())

    except Exception as e:
        print("Erro: ", e)