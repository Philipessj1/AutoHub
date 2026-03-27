from automations.restart_net import restart_net
from core.logger import setup_logger

# iniciando logger
logger = setup_logger()

# Lista de automações
AUTOMATIONS = {
    "1": {
        "name": "Reiniciar Rede",
        "function": restart_net
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
    print("\n\n")
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
            
            except Exception as e:
                logger.info(f"Erro ao executar: {e}")

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()