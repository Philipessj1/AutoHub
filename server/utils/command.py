import subprocess

# roda um comando no windows
def run_command(cmd, logger=None, timeout=None):
    logger.debug(f"CMD: {cmd}")

    if timeout and timeout > 0:
        msg = f"Esperando {timeout} segundos..."
        if logger:
            logger.info(msg)
        else:
            print(msg)

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)

    if result.returncode != 0:
        if logger:
            logger.error(result.stderr.strip())
        else:
            print("Erro:", result.stderr.strip())
    else:
        output = result.stdout.strip()
        if logger:
            logger.info(output)
        else:
            print(output)
