import os
import importlib

AUTOMATIONS_PATH = "automations"

def load_automations():
    automations = {}

    for file in os.listdir(AUTOMATIONS_PATH):
        if file.endswith(".py") and not file.startswith("_"):
            module_name = file[:-3]

            module = importlib.import_module(f"{AUTOMATIONS_PATH}.{module_name}")

            if hasattr(module, "run"):
                automations[module_name] = module.run
    
    return automations