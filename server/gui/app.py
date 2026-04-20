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
        self.geometry("500x500")

        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Config grid
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # Inicializa agents
        self.agents = []

        # Título
        self.label = ctk.CTkLabel(self.main_frame, text="AutoHUB", font=("Arial", 24))
        self.label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Botão local
        self.local_btn = ctk.CTkButton(
            self.main_frame,
            text="Reiniciar Rede Local",
            command=self.run_local,
            width=200
        )
        self.local_btn.grid(row=1, column=0, columnspan=2, pady=10)

        ## Comandos remotos
        # Menu de agents
        self.agent_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=["Nenhum"]
        )
        self.agent_menu.grid(row=2, column=0, columnspan=2, pady=10)

        # Input do Nome do Agent
        self.name_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Nome do Agent")
        self.name_entry.grid(row=3, column=0, padx=5, pady=5)

        # Input do Ip do Agent
        self.ip_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Ip do Agent")
        self.ip_entry.grid(row=3, column=1, padx=5, pady=5)

        # Botão de salvar agents
        self.save_agent_btn = ctk.CTkButton(
            self.main_frame,
            text="Salvar Agent",
            command=self.save_agent
        )
        self.save_agent_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Botão listar remoto
        self.list_btn = ctk.CTkButton(
            self.main_frame,
            text="Listar Comandos Remotos",
            command=self.load_remote_commands
        )
        self.list_btn.grid(row=5, column=0, columnspan=2, pady=10)

        # Menu de comandos
        self.commands_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=["Nenhum"]
        )
        self.commands_menu.grid(row=6, column=0, columnspan=2, pady=5)

        # Executar remoto
        self.run_remote_btn = ctk.CTkButton(
            self.main_frame,
            text="Executar Remoto",
            command=self.run_remote_command
        )
        self.run_remote_btn.grid(row=7, column=0, columnspan=2, pady=10)

        # Log
        self.log_box = ctk.CTkTextbox(self.main_frame, height=120)
        self.log_box.grid(row=8, column=0, columnspan=2, pady=10, sticky="nsew")

        self.main_frame.grid_rowconfigure(8, weight=1)

        # Carrega os agents salvos
        self.load_agents()

    # Pegar ip do Input (fallback)
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
            self.log("Nenhum agent selecionado!")
            return

        self.log(f"Buscando comandos de {ip}...")

        def task():
            commands = list_remote(ip)
            self.after(
                0, 
                self.update_commands_ui, 
                commands, 
                "Comandos carregados!",
                "Erro ao listar comandos."
                )

        self.run_async(task)

    # Update na interface após função
    def update_commands_ui(self, data, acemsg, errmsg):
        if data:
            self.commands_menu.configure(values=data)
            self.commands_menu.set(data[0])
            self.log(acemsg)
        else:
            self.log(errmsg)

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

                if not content:
                    return

                data = json.loads(content)

                if isinstance(data, list):
                    self.agents = data
                    names = [agent["name"] for agent in data]

                    if names:
                        self.agent_menu.configure(values=names)
                        self.agent_menu.set(names[0])

        except Exception as e:
            self.log(f"Erro ao carregar Agents: {e}")

    # Salvar Agent
    def save_agent(self):
        name = self.name_entry.get().strip()
        ip = self.ip_entry.get().strip()

        if not name or not ip:
            self.log("Nome e IP são obrigatórios!")
            return

        data = []

        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
            except:
                data = []

        for agent in data:
            if agent["name"] == name:
                self.log("Nome já existe!")
                return

        data.append({"name": name, "ip": ip})

        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

        self.log("Agent salvo!")

        self.load_agents()

    # Pegar IP do agent selecionado
    def get_selected_ip(self):
        selected_name = self.agent_menu.get()

        for agent in self.agents:
            if agent["name"] == selected_name:
                return agent["ip"]

        return None

if __name__ == "__main__":
    app = AutoHUBApp()
    app.mainloop()