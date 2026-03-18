---
title: HealthOS
sdk: docker
license: mit
short_description: 'HealthOS ML API — Clinical AI with FHIR RAG'
---

# 🧠 HealthOS — ML & LLM API

> **Clinical Intelligence Engine** · Powering real-time doctor–patient conversation analysis

---

## 🔗 Live API

| | |
|---|---|
| **Base URL** | [`https://biharibabu-healthos.hf.space/`](https://biharibabu-healthos.hf.space/) |
| **Docs (Swagger)** | [`/docs`](https://biharibabu-healthos.hf.space/docs) |
| **Framework** | FastAPI |
| **Hosting** | Hugging Face Spaces (Docker) |

---

## 📌 What This API Does

The HealthOS LLM API accepts a **transcribed conversation between a doctor and a patient** and returns:

- ✅ A structured **clinical summary** (SOAP-style)
- ✅ **FHIR R4-mapped** resources extracted from the dialogue
- ✅ Grounded, hallucination-resistant output via **RAG** over a public FHIR knowledge base

---

## ⚙️ Tech Stack

| Component | Technology |
|---|---|
| **API Framework** | FastAPI (Python) |
| **LLM Model** | Google Gemini 2.5 Flash |
| **RAG / Knowledge Base** | Publicly available FHIR R4 datasets |
| **Deployment** | Docker on Hugging Face Spaces |

---

## 🏗️ Architecture

```
Doctor–Patient Conversation (text)
            │
            ▼
    ┌───────────────────┐
    │    FastAPI Server  │
    │  /analyze endpoint │
    └────────┬──────────┘
             │
    ┌────────▼──────────────────────────┐
    │         RAG Pipeline              │
    │  Query → FHIR Knowledge Base      │
    │  Retrieve relevant clinical docs  │
    └────────┬──────────────────────────┘
             │
    ┌────────▼──────────────────────────┐
    │     Gemini 2.5 Flash (LLM)        │
    │  Conversation + Retrieved Context │
    │  → Structured Clinical Output     │
    └────────┬──────────────────────────┘
             │
    ┌────────▼──────────────────────────┐
    │         JSON Response             │
    │  • Summary / SOAP Note            │
    │  • FHIR R4 Resource Bundle        │
    └───────────────────────────────────┘
```

---

## 🚀 Quick Start

### Call the API

```bash
curl -X GET "https://biharibabu-healthos.hf.space/" \
 
```

### Example Response

```json
{
  "summary": {
    "chief_complaint": "Fever (102°F) for 3 days with dry cough and mild shortness of breath",
    "assessment": "Likely community-acquired pneumonia or viral infection",
    "plan": "Azithromycin course, rest for 5 days, follow-up if no improvement"
  },
  "fhir_bundle": {
    "resourceType": "Bundle",
    "type": "collection",
    "entry": [
      { "resourceType": "Condition", "code": "Fever", "severity": "moderate" },
      { "resourceType": "MedicationRequest", "medication": "Azithromycin" },
      { "resourceType": "CarePlan", "activity": "Rest for 5 days" }
    ]
  }
}
```

---

## 🧬 Why RAG over a FHIR Knowledge Base?

LLMs can hallucinate clinical terminology, incorrect drug dosages, or non-standard FHIR codes. To prevent this, HealthOS uses **Retrieval-Augmented Generation (RAG)**:

1. **Before generation**, the API queries a publicly available **FHIR R4 knowledge base**
2. Relevant clinical documents (conditions, medications, procedures) are retrieved
3. These are injected as **grounded context** into the Gemini prompt
4. The model generates output **anchored to verified FHIR data** — not just training memory

This ensures clinical accuracy, consistent FHIR coding, and reduced hallucination risk.

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Home Page |
| `GET` | `/docs` | Interactive Swagger UI |
| `GET` | `/health` | Health API |
| `POST` | `/llm` | Calling Model |


---

## 🐳 Run Locally with Docker

```bash
# Clone or pull the Space
git clone https://huggingface.co/spaces/biharibabu/healthos
cd healthos

# Set environment variables
echo "GEMINI_API_KEY=your_key_here" > .env

# Build and run
docker build -t healthos-ml .
docker run -p 7860:7860 --env-file .env healthos-ml
```

API will be available at `http://localhost:7860`

---

## 🔑 Environment Variables

```env
GEMINI_API_KEY=your_google_gemini_api_key
FHIR_KB_PATH=./data/fhir_knowledge_base     # Path to local FHIR knowledge base
LOG_LEVEL=INFO
```

> On Hugging Face Spaces, set these under **Settings → Repository Secrets**.

---

## 📜 License

**MIT License** — free to use, modify, and distribute with attribution.

---

<p align="center">
  <strong>HealthOS ML API · Team HealthWarriors · 2025</strong><br/>
  <em>Grounded. Fast. FHIR-Native.</em>
</p>