# 🚀 AutoHUB

AutoHUB é um sistema de automação distribuída desenvolvido em Python, capaz de executar tarefas localmente ou remotamente através de Agents instalados em máquinas da rede.

O projeto foi pensado para escalar automações de forma simples, centralizada e modular.

---

# 🧠 Conceito

O AutoHUB funciona com dois componentes principais:

## 🔹 Runner (cliente)
Interface que permite executar automações:
- Localmente
- Remotamente via rede

## 🔹 Agent (servidor)
Executa automações remotamente:
- Roda como serviço no Windows
- Fica disponível via HTTP (Flask)
- Executa comandos em background

---

# 🏗️ Estrutura do Projeto

AutoHUB/
│
├── agent/ # Servidor (Agent)
├── automations/ # Scripts de automação
├── core/ # Lógica principal
│ ├── logger.py
│ ├── runner.py
│ ├── remote_client.py
│ └── automation_loader.py
│
├── utils/ # Funções utilitárias
│ └── command.py
│
├── gui/ # Interface gráfica (CustomTkinter)
├── configs/ # Configurações (agents salvos)
├── logs/ # Logs do sistema
│
└── README.md

---

# ⚙️ Funcionalidades

## ✅ Execução local de automações
- Scripts Python executados diretamente

## 🌐 Execução remota
- Comunicação via HTTP
- Execução em outras máquinas da rede

## 🔄 Agent dinâmico
- Carrega automaticamente automações da pasta `automations`
- Não precisa alterar código ao adicionar novos scripts

## 🧵 Execução em background
- Automações não travam o sistema
- Uso de threads

## 📜 Logging
- Logs organizados por módulo
- Separação por execução

## 🖥️ Interface gráfica (GUI)
- Baseada em CustomTkinter
- Execução de comandos com um clique
- Seleção de Agents via dropdown
- Persistência de IPs

## 🧩 Arquitetura modular
- Separação clara entre:
  - automações
  - utilitários
  - core

---

# 🤖 Agent

O Agent é um servidor Flask que:

- Expõe rotas HTTP
- Executa automações dinamicamente
- Roda como processo em segundo plano

### Endpoints

```
GET /

Retorna status:
{
  "status": "Agent online",
  "automations": ["restart_net", "restart_pc"]
}

GET /run/<command>

Executa uma automação

```
## Interface Gráfica

Desenvolvida com:

CustomTkinter (Provisório)

Funcionalidades:

- Executar automações locais
- Listar automações remotas
- Executar comandos remotos
- Gerenciar Agents
- Logs em tempo real

### 📦 Distribuição (Agent)

O Agent pode ser convertido para .exe usando:

```pyinstaller agent_server.spec```

🔧 Características do build

- Inclusão automática de:
- automations
- core
- utils
- Suporte a import dinâmico
- Execução standalone (sem Python instalado)

### 🧠 Execução em background

O Agent pode:

- Rodar sem console
- Iniciar automaticamente com o sistema

### 🔐 Considerações futuras

- Autenticação de requests
- Controle de acesso por comando
- Logs centralizados
- Criptografia


## 🔜 Próximos passos
- Status online/offline dos Agents
- Heartbeat automático
- Agendamento de tarefas
- Sistema de plugins (automações externas)
- Auto-update do Agent
- Dashboard avançado
- Permissões por comando

# 👨‍💻 Autor

Philipe Mello