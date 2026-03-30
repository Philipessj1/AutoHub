from flask import Flask, jsonify
from core.logger import setup_logger
from automations.restart_net import restart_net
import threading

app = Flask(__name__)
logger = setup_logger("AutoHUB.agent")

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

def run_cmd(fname, func):
    logger.info(f"Comando recebido: {fname}")

    try:
        run_in_background(fname, func)
        return jsonify({
            "status": "accepted",
            "message": "Execução Iniciada"
            })
    
    except Exception as e:
        logger.exception("Erro ao executar restart-network")
        return jsonify({"status": "error", "message": str(e)})

@app.route("/")
def home():
    return jsonify({"status": "Agent online"})

@app.route("/restart-network")
def run_restart():
    response = run_cmd("restart-network", restart_net)
    return response


if __name__ == "__main__":
    logger.info("Iniciando Agent...")
    app.run(host="0.0.0.0", port=5000)