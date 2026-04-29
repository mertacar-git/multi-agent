# Multi-Agent AI System (Local + OpenAI)

This project is a working role-based multi-agent workflow where:

- **Planner** creates the execution plan,
- **Developer** produces the implementation draft,
- **Reviewer** evaluates and requests revisions,
- and the orchestrator loops until approval or max iterations.

It is designed to run with:
- **LM Studio** (local, OpenAI-compatible endpoint),
- **OpenAI API key** (cloud),
- optionally **Ollama**.

## Why This Project

I built this to simulate real software team behavior with AI roles, instead of relying on a single general response. The goal is cleaner planning, higher quality drafts, and explicit review feedback.

## Architecture

Flow:

`User -> Planner -> Developer -> Reviewer -> (Approve or Revise)`

Core components:

- `orchestrator.py`: CLI entrypoint and iteration loop.
- `multi_agent/config.py`: provider/env configuration loader.
- `multi_agent/llm/openai_compat.py`: LM Studio + OpenAI compatible client.
- `multi_agent/llm/ollama.py`: optional Ollama adapter.
- `multi_agent/agents/*`: planner/developer/reviewer logic.
- `multi_agent/prompts/*`: role prompts.

## Project Structure

```text
multi_agent/
├── examples/
│   └── sample_request.txt
├── multi_agent/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── developer.py
│   │   ├── planner.py
│   │   ├── reviewer.py
│   │   └── types.py
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── ollama.py
│   │   └── openai_compat.py
│   ├── prompts/
│   │   ├── developer.md
│   │   ├── planner.md
│   │   └── reviewer.md
│   ├── __init__.py
│   └── config.py
├── .env.example
├── .gitignore
├── orchestrator.py
├── requirements.txt
└── README.md
```

## Setup

1) Create and activate virtual environment:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

2) Install dependencies:

```bash
pip install -r requirements.txt
```

3) Create `.env` from `.env.example` and set provider values.

## Configuration

Environment variables:

- `PROVIDER=lmstudio|openai|ollama`
- `OPENAI_BASE_URL=http://localhost:1234/v1` (LM Studio default)
- `OPENAI_MODEL=local-model`
- `OPENAI_API_KEY=` (required for `PROVIDER=openai`)
- `OLLAMA_BASE_URL=http://localhost:11434`
- `OLLAMA_MODEL=llama3.1`
- `TIMEOUT_SECONDS=90`

## Run

Using direct input:

```bash
python orchestrator.py --input "Design a task tracking API with clear milestones." --max-iterations 2
```

Using sample input file:

```bash
python orchestrator.py --input-file examples/sample_request.txt --max-iterations 2
```

Console output includes:

- planner output,
- developer drafts per iteration,
- reviewer feedback per iteration,
- final output.

## Provider Modes

### LM Studio (local, default)

1. Start LM Studio local server with OpenAI-compatible API.
2. Use:
   - `PROVIDER=lmstudio`
   - `OPENAI_BASE_URL=http://localhost:1234/v1`
   - `OPENAI_MODEL=<your_local_model_name>`

### OpenAI (API key)

Use:
- `PROVIDER=openai`
- `OPENAI_API_KEY=<your_key>`
- `OPENAI_MODEL=gpt-4o-mini` (or preferred model)

### Ollama (optional)

Use:
- `PROVIDER=ollama`
- `OLLAMA_BASE_URL=http://localhost:11434`
- `OLLAMA_MODEL=llama3.1`

## Notes

- Reviewer approval is parsed from `APPROVED: yes|no`.
- If reviewer does not approve within `--max-iterations`, orchestrator returns the best last draft.
- Prompt behavior can be tuned in `multi_agent/prompts/`.

