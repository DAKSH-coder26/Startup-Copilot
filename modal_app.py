from modal import App, Secret, Image, asgi_app
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import re

app = App(
    "StartupCopilot",
    secrets=[
        Secret.from_name("notion-secrets"),
        Secret.from_name("my-mistral-secrets")
    ]
)

llm_image = Image.debian_slim().pip_install(
    "transformers==4.38.2",
    "torch==2.2.1",
    "accelerate==0.27.2",
    "sentencepiece==0.2.0",
    "bitsandbytes==0.42.0",
    "tokenizers==0.15.1",
    "fastapi",
    "pytrends"
).env({"REBUILD_FLAG": "7"})

MODEL_CONFIGS = {
    "mistral": {
        "name": "mistralai/Mistral-7B-Instruct-v0.2",
        "max_tokens": 4096,
        "gpu": "H100"
    },
    "zephyr": {
        "name": "HuggingFaceH4/zephyr-7b-beta",
        "max_tokens": 4096,
        "gpu": "H100"
    }
}

model_cache = {}

def load_model(model_name: str):
    if model_name in model_cache:
        return model_cache[model_name]
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        load_in_4bit=True
    )
    model_cache[model_name] = (tokenizer, model)
    return tokenizer, model

def clean_output(text: str) -> str:
    text = re.sub(r'^.*?\|assistant\|', '', text, flags=re.DOTALL)
    text = re.sub(r'^.*?(## Workflow)', r'\1', text, flags=re.DOTALL)
    return text.strip()

@app.function(image=llm_image, gpu="H100", timeout=600)
def generate_workflow(prompt: str, model_choice: str = "zephyr") -> str:
    config = MODEL_CONFIGS[model_choice]
    tokenizer, model = load_model(config["name"])
    system_prompt = """You are an expert workflow automation engineer..."""
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    formatted = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(formatted, return_tensors="pt").to("cuda")
    max_available = config["max_tokens"] - inputs["input_ids"].shape[1]
    outputs = model.generate(**inputs, max_new_tokens=min(1024, max(max_available, 1)), temperature=0.5, top_p=0.9, do_sample=False)
    return clean_output(tokenizer.decode(outputs[0], skip_special_tokens=True))

@app.function(image=llm_image, gpu="H100")
def validate_idea(prompt: str, model_choice: str = "zephyr") -> str:
    config = MODEL_CONFIGS[model_choice]
    tokenizer, model = load_model(config["name"])
    system_prompt = """You are a startup analyst..."""
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    formatted = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(formatted, return_tensors="pt").to("cuda")
    max_available = config["max_tokens"] - inputs["input_ids"].shape[1]
    outputs = model.generate(**inputs, max_new_tokens=min(1024, max(max_available, 1)), temperature=0.5, top_p=0.9, do_sample=False)
    return clean_output(tokenizer.decode(outputs[0], skip_special_tokens=True))

@app.function(image=llm_image, gpu="H100")
def generate_business_case(prompt: str, model_choice: str = "zephyr") -> str:
    config = MODEL_CONFIGS[model_choice]
    tokenizer, model = load_model(config["name"])
    system_prompt = """You are a business consultant..."""
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    formatted = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(formatted, return_tensors="pt").to("cuda")
    max_available = config["max_tokens"] - inputs["input_ids"].shape[1]
    outputs = model.generate(**inputs, max_new_tokens=min(1024, max(max_available, 1)), temperature=0.5, top_p=0.9, do_sample=False)
    return clean_output(tokenizer.decode(outputs[0], skip_special_tokens=True))

@app.function(image=llm_image, gpu="H100")
def generate_pitch_deck(prompt: str, model_choice: str = "zephyr") -> str:
    config = MODEL_CONFIGS[model_choice]
    tokenizer, model = load_model(config["name"])
    system_prompt = """You are a pitch deck expert..."""
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    formatted = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(formatted, return_tensors="pt").to("cuda")
    max_available = config["max_tokens"] - inputs["input_ids"].shape[1]
    outputs = model.generate(**inputs, max_new_tokens=min(1024, max(max_available, 1)), temperature=0.5, top_p=0.9, do_sample=False)
    return clean_output(tokenizer.decode(outputs[0], skip_special_tokens=True))

@app.function(image=llm_image, gpu="H100")
def market_strategy(prompt: str, model_choice: str = "zephyr") -> str:
    config = MODEL_CONFIGS[model_choice]
    tokenizer, model = load_model(config["name"])
    system_prompt = """You are a startup go-to-market strategist..."""
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    formatted = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(formatted, return_tensors="pt").to("cuda")
    max_available = config["max_tokens"] - inputs["input_ids"].shape[1]
    outputs = model.generate(**inputs, max_new_tokens=min(1024, max(max_available, 1)), temperature=0.5, top_p=0.9, do_sample=False)
    return clean_output(tokenizer.decode(outputs[0], skip_special_tokens=True))

@app.function(image=llm_image)
@asgi_app()
def fastapi_app():
    from fastapi import FastAPI, Request

    app1 = FastAPI()

    @app1.post("/generate-workflow")
    async def generate_workflow_web(request: Request):
        data = await request.json()
        result = generate_workflow.remote(data["prompt"], data.get("model", "zephyr"))
        clean_result = result.replace("\\n", "\n")
        return clean_result
    
    @app1.post("/validate-idea")
    async def validate_idea_web(request: Request):
        data = await request.json()
        result = validate_idea.remote(data["prompt"], data.get("model", "zephyr"))
        clean_result = result.replace("\\n", "\n")
        return clean_result
    
    @app1.post("/business-case")
    async def business_case_web(request: Request):
        data = await request.json()
        result = generate_business_case.remote(data["prompt"], data.get("model", "zephyr"))
        clean_result = result.replace("\\n", "\n")
        return clean_result
    
    @app1.post("/pitch-deck")
    async def pitch_deck_web(request: Request):
        data = await request.json()
        result = generate_pitch_deck.remote(data["prompt"], data.get("model", "zephyr"))
        clean_result = result.replace("\\n", "\n")
        return clean_result

    @app1.post("/gtm-strategy")
    async def gtm_strategy_web(request: Request):
        data = await request.json()
        result = market_strategy.remote(data["prompt"], data.get("model", "zephyr"))
        clean_result = result.replace("\\n", "\n")
        return clean_result

    return app1