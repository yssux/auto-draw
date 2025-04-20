import importlib.util
import os
import sys

def lan_sel():
    lang = input("Language/Langue (EN-FR): ").strip().upper()

    if lang == "EN":
        lang_path = os.path.join("en-EN", "autoDraw.py")
    elif lang == "FR":
        lang_path = os.path.join("fr-FR", "dessin_autom.py")
    else:
        print("Error: Invalid language.")
        return lan_sel()

    abs_path = os.path.abspath(lang_path)
    module_dir = os.path.dirname(abs_path)

    # Add the module directory to sys.path so internal imports work
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)

    spec = importlib.util.spec_from_file_location("lang_module", abs_path)
    lang_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lang_module)

if __name__ == "__main__":
    lan_sel()
