from flask import Flask, jsonify
from core.logger import setup_logger
from core.automation_loader import load_automations
import threading
import socket

app = Flask(__name__)
logger = setup_logger("AutoHUB.agent")

AUTOMATIONS = load_automations()

def run_in_background(fname, func):
    def wrapper():
        try:
            logger.info(f"Iniciando execução: {fname}")
            func()
            logger.info(f"Finalizando com sucesso: {fname}")
        except Exception:
            logger.exception(f"Erro durante a execução: {fname}")
   
    thread = threading.Thread(target=wrapper)
    thread.daemon = True
    thread.start()

def is_already_running(port=5000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("0.0.0.0", port))
        s.close()
        return False
    except:
        return True

@app.route("/")
def home():
    return jsonify({
        "status": "Agent online",
        "automations": list(AUTOMATIONS.keys())
    })

@app.route("/run/<command>")
def run_cmd_route(command):
    if command not in AUTOMATIONS:
        return jsonify({"status": "error", "message": "Comando não encontrado"}), 404

    logger.info(f"Comando recebido: {command}")

    run_in_background(command, AUTOMATIONS[command])
    
    return jsonify({
            "status": "accepted",
            "message": "Execução Iniciada"
            })

if __name__ == "__main__":
    if is_already_running(5000):
        print("Agent já está rodando!")
        exit()

    logger.info("Iniciando Agent...")
    app.run(host="0.0.0.0", port=5000)