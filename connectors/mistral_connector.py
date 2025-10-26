from llama_cpp import Llama
from modules.recipe_parser import parse_recipe

MODEL_PATH = r"C:\Users\admin\Desktop\Models\mistral-7b-instruct-v0.2.Q5_K_S.gguf"
llm = Llama(model_path=MODEL_PATH, n_ctx=2048)

def query_mistral(prompt):
    print("🔗 Sending prompt to Mistral...")
    response = llm(prompt, max_tokens=512, stop=["</s>"])
    text = response["choices"][0]["text"].strip()
    return parse_recipe(text)