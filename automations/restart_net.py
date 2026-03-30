from core.logger import setup_logger
import subprocess
import time

# iniciando logger
logger = setup_logger("AutoHUB.restart_net", "restart_net")

# nome do adaptador Ex: Ethernet, Wi-fi
ADAPTER_NAME = "Ethernet"

# roda um comando no windows
def run_command(cmd):
    logger.debug(f"CMD: {cmd}")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        logger.error(result.stderr.strip())
    else:
        output = result.stdout.strip()
        if output:
            logger.info(output)

# função principal 
def restart_net():
    logger.info("Desativando adaptador...")
    run_command(f'netsh interface set interface "{ADAPTER_NAME}" admin=disable')

    time.sleep(3)

    logger.info("Ativando adaptador...")
    run_command(f'netsh interface set interface "{ADAPTER_NAME}" admin=enable')

if __name__ == "__main__":
    restart_net()