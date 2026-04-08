import os
import sys
import importlib

BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

def load_automations():
    automations = {}

    automations_path = os.path.join(BASE_DIR, "automations")

    for file in os.listdir(automations_path):
        if file.endswith(".py") and file != "__init__.py":
            module_name = file[:-3]

            module = importlib.import_module(f"automations.{module_name}")

            if hasattr(module, "run"):
                automations[module_name] = module.run
    
    return automations