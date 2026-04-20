from utils.command import run_command
from core.logger import setup_logger

logger = setup_logger("AutoHUB.restart_pc")

def run():
    logger.info("Reiniciando o computador...")
    run_command(f"shutdown /r /t {5}", logger)

if __name__ == "__main__":
    run()