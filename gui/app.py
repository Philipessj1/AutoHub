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

        ## Comandos remotos
        # Menu de agents
        self.agent_menu = ctk.CTkOptionMenu(
            self,
            values=["Nenhum"]
        )
        self.agent_menu.pack(pady=5)

        # Input do Nome do Agent
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Nome do Agent")
        self.name_entry.pack(pady=5)

        # Input do Ip do Agent
        self.ip_entry = ctk.CTkEntry(self, placeholder_text="Ip do Agent")
        self.ip_entry.pack(pady=5)

        # Carrega os ips salvos
        self.load_agents()

        # Botão de salvar ips
        self.save_agent_btn = ctk.CTkButton(
            self,
            text="Salvar Agent",
            command=self.save_agent
        )
        self.save_agent_btn.pack(pady=5)

        # Botão listar remoto
        self.list_btn = ctk.CTkButton(
            self,
            text="Listar Comandos Remotos",
            command=self.load_remote_commands
        )
        self.list_btn.pack(pady=10)

        # Menu de comandos
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
        ip = self.get_selected_ip()

        if not ip:
            self.log("Nunhum agent selecionado!")
            return

        self.log(f"Buscando comandos de {ip}...")

        def task():
            # Buscar comandos remotos
            commands = list_remote(ip)

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
        ip = self.get_selected_ip()

        if not ip:
            self.log("Nenhum agent selecionado!")
            return

        self.log(f"Executando {cmd} em {ip}")
        run_remote(ip, cmd)
        self.log("Comando enviado!")

    # Rodar função em async
    def run_async(self, func):
        threading.Thread(target=func, daemon=True).start()
    
    # Carregar agents
    def load_agents(self):
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
                if isinstance(data, list):
                    self.agents = data

                    names = [agent["name"] for agent in data]
                    
                    # Insere os agents salvos no menu
                    if names:
                        self.agent_menu.configure(values=names)
                        self.agent_menu.set(names[0])

        except Exception as e:
            self.log(f"Erro ao carregar Agents: {e}")
            
    # Salvar IP
    def save_agent(self):
        name = self.name_entry.get().strip()
        ip = self.ip_entry.get().strip()

        if not name or not ip:
            self.log("Nome e IP são obrigatórios!")
            return

        # carregar agents existentes
        data = []

        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    content = f.read().strip()

                    if content:
                        data = json.loads(content)

            except:
                data = []

        # evitar duplicação
        for agent in data:
            if agent["name"] == name:
                self.log("Nome já existe!")
                return
        
        # Salva o arquivo
        data.append({"name": name, "ip": ip})

        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

        self.log("Agent salvo!")

        self.load_agents()
    
    def get_selected_ip(self):
        selected_name = self.agent_menu.get()

        for agent in self.agents:
            if agent["name"] == selected_name:
                return agent["ip"]

        return None
    
if __name__ == "__main__":
    app = AutoHUBApp()
    app.mainloop()