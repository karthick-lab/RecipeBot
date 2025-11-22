import json
import os
import sys

from llama_cpp import Llama
from modules.recipe_parser import parse_gemini_response

exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
config_file = os.path.join(exe_dir, "config.json")

with open(config_file, "r") as f:
    CONFIG = json.load(f)

MODEL_PATH = CONFIG["mistral_model"]
llm = Llama(model_path=MODEL_PATH, n_ctx=2048)

def query_mistral(prompt):
    print("🔗 Sending prompt to Mistral...")
    response = llm(prompt, max_tokens=512, stop=["</s>"])
    text = response["choices"][0]["text"].strip()
    return parse_gemini_response(text)