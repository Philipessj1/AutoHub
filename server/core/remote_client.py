import requests
from core.logger import setup_logger

logger = setup_logger("AutoHUB.remote", "remote")

def run_remote(ip, command):
    url = f"http://{ip}:5000/run/{command}"

    try:
        logger.info(f"Enviando comando '{command}' para '{ip}'")

        response = requests.get(url, timeout=5)
        data = response.json()

        logger.info(f"Resposta: {data}")
    except Exception as e:
        logger.exception(f"Erro ao conectar com {ip}: {e}")   

def list_remote(ip):
    url = f"http://{ip}:5000/"

    try:
        data = requests.get(url, timeout=5).json()
        
        logger.info(f"Automações disponíveis em {ip}: {data.get('automations')}")
        return data.get("automations", [])
    
    except Exception as e:
        logger.exception(f"Erro ao obter automações: {e}")
        return []
