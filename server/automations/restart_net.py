from core.logger import setup_logger
from utils.command import run_command
import time

# iniciando logger
logger = setup_logger("AutoHUB.restart_net", "restart_net")

# nome do adaptador Ex: Ethernet, Wi-fi
ADAPTER_NAME = "Ethernet"

# função principal 
def run():
    logger.info("Desativando adaptador...")
    run_command(f'netsh interface set interface "{ADAPTER_NAME}" admin=disable', logger)

    logger.info("Ativando adaptador...")
    run_command(f'netsh interface set interface "{ADAPTER_NAME}" admin=enable', logger, 3)

if __name__ == "__main__":
    run()