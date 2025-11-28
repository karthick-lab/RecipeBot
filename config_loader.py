import os, sys, json

def load_config():
    # If a config path is passed as an argument, use it
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        # fallback: look in the folder where the script/exe is launched
        exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        config_file = os.path.join(exe_dir, "config.json")

    with open(config_file, "r") as f:
        return json.load(f)