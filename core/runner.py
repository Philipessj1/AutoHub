from automations.restart_net import restart_net

AUTOMATIONS = {
    "1": {
        "name": "Reiniciar Rede",
        "function": restart_net
    }
}

def show_menu():
    print("\n=== AutoHub v0.01 ===")
    for key, value in AUTOMATIONS.items():
        print(f"{key} - {value['name']}")
        print("0 - Sair")

def main():
    while True:
        show_menu()
        choice = input("Escolha uma opção: ")

        if choice == "0":
            print("Saindo...")
            break

        elif choice in AUTOMATIONS:
            func = AUTOMATIONS[choice]["function"]
            func()

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()