# 🚀 Startup Copilot (Work-in-Progress)

> **Note**: The project showcases integrations of LLMs with real-world productivity tools. This is an in-progress GenAI tool. 

---

## 🧠 What is Startup Copilot?

**Startup Copilot** is a generative AI-powered assistant for early-stage startup founders.

It helps with:
- 🧠 Idea validation (Google Trends + LLM)
- ⚙️ Workflow generation
- 📊 Business case analysis
- 🎯 Go-To-Market strategy
- 📣 Pitch deck drafting

All results can be optionally synced to Notion!

---

## 🏗️ Architecture

- **Frontend:** Gradio UI (tab-based)
- **Backend:** Modal Functions (GPU, torch, transformers)
- **Models Used:** Zephyr 7B, Mistral 7B
- **APIs:** Google Trends via PyTrends, Notion API
- **Deployment:** FastAPI wrapped in Modal's ASGI App

---

## 📦 Setup Instructions

Clone the repo and add your `.env` file with these variables:

```env
MODAL_BASE=https://your-modal-app.modal.run
NOTION_TOKEN=your-notion-secret
NOTION_DATABASE_ID1=your-notion-db
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

Run locally:
```bash
python app.py
```

---

## 🔍 Screenshots

*(Add 1–2 images or a small GIF of your Gradio UI here if possible)*

---

## 🚧 Work in Progress

- [x] Modal deployment
- [x] LLM-based modules
- [x] Notion integration
- [ ] PDF Pitch Deck formatting
- [ ] User auth and history
- [ ] Deployment to HF Space or Vercel (planned)

---

## 💬 Why I Built This

I’m exploring ways to make GenAI truly useful for early-stage founders. This project is part of my self-driven learning, applying APIs, cloud, and LLMs in practical ways.

---

## 🧠 Skills Demonstrated

- Prompt engineering for multiple agent roles
- LLM model handling with Hugging Face + torch
- Modal app building (FastAPI + GPU infra)
- API integration (Google Trends, Notion)
- Frontend UX with Gradio

---

## 📄 License

MIT
