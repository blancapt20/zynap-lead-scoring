# Zynap AI Lead Enrichment Agent

A lightweight AI-powered pipeline that enriches raw lead data using an LLM and scores it based on business rules to produce CRM-ready output.

## 🧠 Architecture Overview

The system follows a modular pipeline design:

```text
Input (JSON leads)
    ↓
LLM Enrichment Agent
    ↓
Deterministic Scoring Engine
    ↓
CRM Routing Logic
    ↓
Structured JSON Output
```

Core components:

- **LeadEnrichmentAgent** (`src/lead_scoring/enrichment/agent.py`): LLM wrapper for structured extraction with retry + fallback handling.
- **LeadScorer** (`src/lead_scoring/scoring/rules.py`, `src/lead_scoring/scoring/engine.py`): deterministic business logic for reproducible scores.
- **CRM Router** (`src/lead_scoring/output/formatter.py`): maps score to actionable CRM route.
- **Main Orchestrator** (`src/lead_scoring/main.py`): coordinates the full pipeline from input loading to JSON output.

## 🛠 Tech Stack

- Python `3.11+`
- Groq API (Llama3-70B) for production LLM integration
- Pydantic (schema validation)
- python-dotenv (environment configuration)
- Pytest (functional verification)

> Note: current default execution uses a deterministic `MockLLMClient` so local runs are stable and testable without external API calls.

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/blancapt20/zynap-lead-scoring.git
cd zynap-lead-scoring
```

### 2. Create virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key

Create a `.env` file:

```env
GROQ_API_KEY=your_key_here
```

### 5. Run the script

Package entrypoint (recommended in this repo):

```bash
python -m lead_scoring.main
```

Optional CLI entrypoint (after `pip install -e .`):

```bash
lead-scoring
```

## 📥 Input Format

Expected lead record:

```json
{
  "id": "lead_001",
  "email": "example@email.com",
  "raw_note": "Unstructured text..."
}
```

Input file location: `data/leads.json`.

## 📤 Output Format

Example pipeline output:

```json
{
  "id": "lead_001",
  "email": "sarah.connor@sky-net.org",
  "enriched_data": {
    "industry": "Cybersecurity",
    "size": 250,
    "intent": "Automate threat response operations"
  },
  "score": 85,
  "crm_action": "PRIORITY_sales_route"
}
```

## 🧮 Scoring Logic

### Scoring Rules

Industry Fit:

- Cybersecurity / AI -> +50
- Fintech -> +25
- Other -> +0

Size Fit:

- > 100 employees -> +25
- 10-100 employees -> +10
- <=10 employees -> +0

Content Quality:

- Meaningful intent detected -> +10
- Vague/empty note -> +0

Routing threshold:

- score > 70 -> `PRIORITY_sales_route`
- otherwise -> `marketing_route`

## 🤖 LLM Design Decisions

The LLM is used exclusively for structured extraction (`industry`, `size`, `intent`).  
All business scoring and routing logic remains deterministic to ensure reliability and reproducibility.

Design choices:

- Strict JSON-only prompt contract for predictable parsing
- Validation through Pydantic models
- Retry logic on transient failures
- Safe fallback enrichment on malformed/failed responses
- Clear separation between AI extraction and business rules

## ✅ Test Plan (prove functionality)

Run all tests:

```bash
pytest -q
```

Run by module:

```bash
pytest tests/test_enrichment.py -q
pytest tests/test_scoring.py -q
pytest tests/test_output.py -q
```

What these tests prove:

- `test_enrichment.py`: extraction correctness, model validity, and fallback behavior under failure/malformed payloads
- `test_scoring.py`: scoring rule correctness, combined totals, and score clamping
- `test_output.py`: CRM routing correctness and final object shape

Quick validation flow:

1. Run `pytest -q`
2. Run `python -m lead_scoring.main`
3. Confirm high-fit leads receive higher scores and correct CRM route

## ⚠️ Assumptions

- Company size is stored as an integer estimate.
- Ambiguous or missing enrichment values default safely (`industry="Other"`, `size=0`).
- "Interested in pricing" is treated as low-intent content.
- Email domain is not currently used as a scoring signal.

## 🔮 Future Improvements

- Plug in live Groq client with configurable model + temperature
- Add confidence scoring for enrichment output
- Add async/batch processing for higher throughput
- Add structured output enforcement via function/tool calling
- Add persistence layer and CRM API integration
- Add observability (metrics, latency, error rate, retries)

