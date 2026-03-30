from automations.restart_net import run as restart_net
from core.logger import setup_logger
from core.remote_client import run_remote, list_remote

# iniciando logger
logger = setup_logger("AutoHUB.runner", "runner")

REMOTE_IP = "192.168.0.67"

# Lista de automações
OPTIONS = {
    "1": {
        "name": "Reiniciar Rede Local",
        "function": restart_net
    },
    "2": {
        "name": "Listar comandos remotos",
        "function": lambda: print(list_remote(REMOTE_IP))
    }
}

# mostra o menu
def show_menu():
    print("\n=== AutoHub v0.02 ===")
    for key, value in OPTIONS.items():
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

        elif choice in OPTIONS:
            func = OPTIONS[choice]["function"]
            logger.info(f"Executando: {OPTIONS[choice]['name']}")
            
            try:
                func()
                logger.info("Execução concluída com sucesso!")
            
            except Exception:
                logger.exception("Erro ao executar!")

        elif choice == "remote":
            commands = list_remote(REMOTE_IP)

            if not commands:
                print("Nenhuma automação encontrada.")
                continue

            print("\n=== Comandos Remotos ===")
            for i, cmd in enumerate(commands):
                print(f"{i + 1} - {cmd}")
            
            selected = input("Escolha o comando: ")

            try:
                cmd = commands[int(selected) - 1]
                run_remote(REMOTE_IP, cmd)
            
            except:
                print("Escolha inválida!")
        else:
            print("Opção inválida")

if __name__ == "__main__":
    main()