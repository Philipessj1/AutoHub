import customtkinter as ctk
import threading
import os
import json
from core.remote_client import run_remote, list_remote
from automations.restart_net import run as restart_net

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "configs/agents.json"

class AutoHUBApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Nome e Tamanho da GUI
        self.title("AutoHUB")
        self.geometry("500x400")

        # Título
        self.label = ctk.CTkLabel(self, text="AutoHUB", font=("Arial", 24))
        self.label.pack(pady=10)

        # Botão local
        self.local_btn = ctk.CTkButton(
            self,
            text="Reiniciar Rede Local",
            command=self.run_local
        )
        self.local_btn.pack(pady=10)

        # Botão listar remoto
        self.list_btn = ctk.CTkButton(
            self,
            text="Listar Comandos Remotos",
            command=self.load_remote_commands
        )
        self.list_btn.pack(pady=10)

        # Input do Ip do Agent
        self.ip_entry = ctk.CTkEntry(self, placeholder_text="Ip do Agent")
        self.ip_entry.pack(pady=5)

        # Carrega os ips salvos
        self.load_ips()

        # Botão de salvar ips
        self.save_ip_btn = ctk.CTkButton(
            self,
            text="Salvar IP",
            command=self.save_ip
        )
        self.save_ip_btn.pack(pady=5)

        # Dropdown de comandos
        self.commands_menu = ctk.CTkOptionMenu(
            self,
            values=["Nenhum"]
        )
        self.commands_menu.pack(pady=10)

        # Executar remoto
        self.run_remote_btn = ctk.CTkButton(
            self,
            text="Executar Remoto",
            command=self.run_remote_command
        )
        self.run_remote_btn.pack(pady=10)

        # Log
        self.log_box = ctk.CTkTextbox(self, height=120)
        self.log_box.pack(pady=10, padx=10, fill="both")

    # Pegar ip do Input
    def get_ip(self):
        return self.ip_entry.get().strip()

    # Log na Interface
    def log(self, message):
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")

    # Rodar função localmente
    def run_local(self):
        self.log("Executando local...")
        self.run_async(restart_net)
        self.log("Concluído!")

    # Carregar funções remotamente
    def load_remote_commands(self):
        self.log("Buscando comandos remotos...")

        def task():
            # Buscar comandos remotos
            commands = list_remote(self.get_ip())

            # atualizar UI na thread principal
            self.after(0, self.update_commands_ui, commands)

        self.run_async(task)

    # Update na interface após função
    def update_commands_ui(self, commands):
        if commands:
            self.commands_menu.configure(values=commands)
            self.commands_menu.set(commands[0])
            self.log("Comandos carregados!")
        else:
            self.log("Nenhum comando encontrado.")

    # Rodar funções remotamente
    def run_remote_command(self):
        cmd = self.commands_menu.get()
        remote_ip = self.get_ip()

        self.log(f"Executando remoto: {cmd}")
        run_remote(remote_ip, cmd)
        self.log("Comando enviado!")

    # Rodar função em async
    def run_async(self, func):
        threading.Thread(target=func, daemon=True).start()
    
    # Carregar IPs
    def load_ips(self):
        if not os.path.exists(CONFIG_FILE):
            return

        try:
            with open(CONFIG_FILE, "r") as f:
                content = f.read().strip()

                # arquivo vazio → ignora
                if not content:
                    return  

                data = json.loads(content)

                # garantir que é lista
                if isinstance(data, list) and data:
                    self.ip_entry.insert(0, data[0])
                else:
                    self.log("Formato inválido no agents.json")

        except Exception as e:
            self.log(f"Erro ao carregar IPs: {e}")
            
    # Salvar IP
    def save_ip(self):
        ip = self.get_ip()

        if not ip:
            self.log("IP vazio!")
            return

        data = []

        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    content = f.read().strip()

                    if content:
                        data = json.loads(content)

                    if not isinstance(data, list):
                        data = []
            except:
                data = []

        if ip not in data:
            data.append(ip)

            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f, indent=4)

            self.log("IP salvo!")
        else:
            self.log("IP já existe.")

if __name__ == "__main__":
    app = AutoHUBApp()
    app.mainloop()