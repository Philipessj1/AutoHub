import os
import shutil
from core.logger import setup_logger

logger = setup_logger("AutoHUB.copy_xdoc")

SOURCE_BASE = r"C:\Backup\DATS_PDVAlterdata\2020\abril"
DESTINATION = r"\\192.168.0.4\alterdat\CUPOM MENSAL\Teste"

def run():
    logger.info("Iniciando cópia de arquivos XDoc...")

    copied = 0

    # percorre tudo recursivamente
    for root, dirs, files in os.walk(SOURCE_BASE):
        for file in files:
            if file.startswith("XDoc") and file.lower().endswith(".dat"):

                source_file = os.path.join(root, file)

                # troca extensão
                new_name = file[:-4] + ".xml"
                dest_file = os.path.join(DESTINATION, new_name)

                try:
                    shutil.copy2(source_file, dest_file)
                    logger.info(f"Copiado: {source_file} → {dest_file}")
                    copied += 1

                except Exception as e:
                    logger.error(f"Erro ao copiar {source_file}: {e}")

    logger.info(f"Total copiado: {copied}")