
import gradio as gr
import os
import requests
from integrations import save_to_notion, fetch_google_trends_data

MODAL_BASE = os.environ.get("MODAL_BASE")

def process_workflow(prompt, model, notion_enabled, dbid):
    response = requests.post(f"{MODAL_BASE}/generate-workflow", json={"prompt": prompt, "model": model})
    output = response.text
    if notion_enabled:
        save_to_notion("Generated Workflow", output, dbid)
    return output, "✅ Workflow generated"

def process_validator(prompt, model, notion_enabled, dbid):
    google_trends = fetch_google_trends_data(prompt)
    extra_context = f"\n\nTrends Data:\n{google_trends}" if google_trends else ""
    full_prompt = f"{prompt}{extra_context}"
    response = requests.post(f"{MODAL_BASE}/validate-idea", json={"prompt": full_prompt, "model": model})
    output = response.text
    if notion_enabled:
        save_to_notion("Idea Validation", output, dbid)
    return output, "✅ Validation complete"

def process_business_case(prompt, model, notion_enabled, dbid):
    response = requests.post(f"{MODAL_BASE}/business-case", json={"prompt": prompt, "model": model})
    output = response.text
    if notion_enabled:
        save_to_notion("Business Case", output, dbid)
    return output, "✅ Analysis ready"

def process_pitch(prompt, model, notion_enabled, dbid):
    google_trends = fetch_google_trends_data(prompt)
    extra_context = f"\n\nTrends Data:\n{google_trends}" if google_trends else ""
    full_prompt = f"{prompt}{extra_context}"
    response = requests.post(f"{MODAL_BASE}/pitch-deck", json={"prompt": full_prompt, "model": model})
    output = response.text
    if notion_enabled:
        save_to_notion("Pitch Deck", output, dbid)
    return output, "✅ Pitch deck created"

def process_market_strategy(prompt, model, notion_enabled, dbid):
    google_trends = fetch_google_trends_data(prompt)
    extra_context = f"\n\nTrends Data:\n{google_trends}" if google_trends else ""
    full_prompt = f"Generate a detailed Go-To-Market strategy for the prompt'{prompt}'.{extra_context}"
    response = requests.post(f"{MODAL_BASE}/gtm-strategy", json={"prompt": full_prompt, "model": model})
    output = response.text
    if notion_enabled:
        save_to_notion("GTM Strategy", output, dbid)
    return output, "✅ GTM strategy created"

with gr.Blocks(title="Startup Copilot") as demo:
    gr.Markdown("# 🚀 Startup Copilot")

    with gr.Tab("Workflow Builder"):
        idea1 = gr.Textbox(label="Describe your startup idea")
        model1 = gr.Radio(["zephyr", "mistral"], value="zephyr")
        notion1 = gr.Checkbox(label="Save to Notion")
        dbid1 = gr.Textbox(label="Your Notion Database ID", placeholder="Leave empty to use default (if set)")
        btn1 = gr.Button("Generate Workflow")
        out1 = gr.Markdown()
        status1 = gr.Textbox()
        btn1.click(process_workflow, [idea1, model1, notion1, dbid1], [out1, status1])

    with gr.Tab("Idea Validator"):
        idea2 = gr.Textbox(label="Describe your startup idea")
        model2 = gr.Radio(["zephyr", "mistral"], value="zephyr")
        notion2 = gr.Checkbox(label="Save to Notion")
        dbid2 = gr.Textbox(label="Your Notion Database ID", placeholder="Leave empty to use default (if set)")
        btn2 = gr.Button("Validate Idea")
        out2 = gr.Markdown()
        status2 = gr.Textbox()
        btn2.click(process_validator, [idea2, model2, notion2, dbid2], [out2, status2])

    with gr.Tab("Venture Analysis"):
        idea3 = gr.Textbox(label="Describe your business concept")
        model3 = gr.Radio(["zephyr", "mistral"], value="zephyr")
        notion3 = gr.Checkbox(label="Save to Notion")
        dbid3 = gr.Textbox(label="Your Notion Database ID", placeholder="Leave empty to use default (if set)")
        btn3 = gr.Button("Generate Business Case")
        out3 = gr.Markdown()
        status3 = gr.Textbox()
        btn3.click(process_business_case, [idea3, model3, notion3, dbid3], [out3, status3])

    with gr.Tab("Pitch Deck Creator"):
        idea4 = gr.Textbox(label="Briefly describe your startup")
        model4 = gr.Radio(["zephyr", "mistral"], value="zephyr")
        notion4 = gr.Checkbox(label="Save to Notion")
        dbid4 = gr.Textbox(label="Your Notion Database ID", placeholder="Leave empty to use default (if set)")
        btn4 = gr.Button("Generate Pitch Deck")
        out4 = gr.Markdown()
        status4 = gr.Textbox()
        btn4.click(process_pitch, [idea4, model4, notion4, dbid4], [out4, status4])

    with gr.Tab("GTM Wizard"):
        idea5 = gr.Textbox(label="Enter keyword / product")
        model5 = gr.Radio(["zephyr", "mistral"], value="zephyr")
        notion5 = gr.Checkbox(label="Save to Notion")
        dbid5 = gr.Textbox(label="Your Notion Database ID", placeholder="Leave empty to use default (if set)")
        btn5 = gr.Button("Generate GTM strategy")
        out5 = gr.Markdown()
        status5 = gr.Textbox()
        btn5.click(process_market_strategy, [idea5, model5, notion5, dbid5], [out5, status5])
