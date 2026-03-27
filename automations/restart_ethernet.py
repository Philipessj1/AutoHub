import subprocess
import time

ADAPTER_NAME = "Ethernet"

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("Erro:", result.stderr)
    else:
        print(result.stdout)

def restart_ethernet():
    print("Desativando adaptador...")
    run_command(f'netsh interface set interface "{ADAPTER_NAME}" admin=disable')

    time.sleep(5)

    print("Ativando adaptador...")
    run_command(f'netsh interface set interface "{ADAPTER_NAME}" admin=enable')

if __name__ == "__main__":
    restart_ethernet()