from automations.restart_net import restart_net
from core.logger import setup_logger
from core.remote_client import restart_remote

# iniciando logger
logger = setup_logger("AutoHUB.runner", "runner")

# Lista de automações
AUTOMATIONS = {
    "1": {
        "name": "Reiniciar Rede Local",
        "function": restart_net
    },
    "2": {
        "name": "Reiniciar Rede Remoto",
        "function": lambda: restart_remote("192.168.0.67")
    }
}

# mostra o menu
def show_menu():
    print("\n=== AutoHub v0.01 ===")
    for key, value in AUTOMATIONS.items():
        print(f"{key} - {value['name']}")
    print("0 - Sair")

#função principal
def main():
    logger.info("===== NOVA EXECUÇÃO =====\n")
    logger.info("AutoHub iniciado")

    while True:
        show_menu()
        choice = input("Escolha uma opção: ")

        if choice == "0":
            logger.info("Encerrando AutoHub\n\n")
            break

        elif choice in AUTOMATIONS:
            func = AUTOMATIONS[choice]["function"]
            logger.info(f"Executando: {AUTOMATIONS[choice]['name']}")
            
            try:
                func()
                logger.info("Execução concluída com sucesso!")
            
            except Exception:
                logger.exception("Erro ao executar!")

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()