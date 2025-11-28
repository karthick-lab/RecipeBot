import json
import os
import sys

#from llama_cpp import Llama
#from modules.recipe_parser import parse_gemini_response

#from config_loader import load_config

#CONFIG = load_config()


#MODEL_PATH = CONFIG["mistral_model"]
#llm = Llama(model_path=MODEL_PATH, n_ctx=2048)

#def query_mistral(prompt):
    #print("🔗 Sending prompt to Mistral...")
    #response = llm(prompt, max_tokens=512, stop=["</s>"])
    #text = response["choices"][0]["text"].strip()
    #return parse_gemini_response(text)