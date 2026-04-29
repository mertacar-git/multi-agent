# Multi-Agent AI System

A lightweight multi-agent architecture that simulates real-world software teamwork by assigning a clear role to each AI agent.  
I designed this project to explore how task planning, implementation, and quality control can be separated into specialized roles while still using a practical and resource-efficient setup.

## Overview

This project demonstrates a collaborative AI workflow where one user request is processed by three role-specific agents:

- **Planner**: Understands the request and splits it into actionable steps.
- **Developer**: Implements the plan and produces an initial solution.
- **Reviewer**: Evaluates the output, suggests fixes, and drives iterative improvement.

The objective is to mimic how human teams work in modern software projects: plan first, build second, review continuously.

## Why I Built This

Single-agent systems are fast, but they can miss structure, quality checks, and revision loops.  
I built this project to test whether a role-based agent pipeline can provide:

- better task clarity,
- more consistent output quality,
- and improved reasoning transparency.

## Core Features

- **Task decomposition** for turning broad goals into concrete subtasks.
- **Role-based prompting** so each agent focuses on a single responsibility.
- **Iterative improvement loop** to refine drafts before final output.
- **Collaboration simulation** that mirrors real software team dynamics.
- **Resource-aware design** with no requirement for heavy GPU infrastructure.

## Agent Roles

### 1) Planner Agent

- Analyzes user intent.
- Identifies constraints and priorities.
- Produces a structured execution plan for downstream agents.

### 2) Developer Agent

- Consumes planner output.
- Converts tasks into implementation-ready content.
- Delivers a first-pass solution.

### 3) Reviewer Agent

- Checks quality, consistency, and completeness.
- Detects missing steps or weak reasoning.
- Sends feedback for revision until output quality is acceptable.

## Workflow

The system follows this high-level flow:

`User -> Planner -> Developer -> Reviewer`

In extended scenarios, the Reviewer can loop feedback back to the Developer for one or more refinement cycles.

## Tech Stack

- **Python** for orchestration and agent execution logic.
- **LangChain** or **CrewAI** for multi-agent coordination patterns.
- Modular prompt templates for role specialization.

## Optimization Strategy

To keep the project practical and cost-efficient:

- A **single model** can be reused across all roles with different role prompts.
- Minimal hardware assumptions are made.
- The architecture favors prompt engineering and flow design over expensive infrastructure.

## Example Execution Scenario

1. User asks for a solution (for example, a product requirement draft).
2. Planner creates a scoped plan with tasks.
3. Developer produces a draft solution.
4. Reviewer evaluates quality and returns improvement notes.
5. Developer revises based on feedback.
6. Final response is delivered.

## Project Goal

The main goal is to **simulate real-world AI collaboration** in a simple, reproducible setup that can be adapted to many domains (software tasks, documentation, analysis pipelines, and more).

## Repository Structure

Current minimal structure:

```text
multi_agent/
├── multi_agent.md
└── README.md
```

As the project evolves, this can expand into:

```text
multi_agent/
├── agents/
│   ├── planner.py
│   ├── developer.py
│   └── reviewer.py
├── prompts/
│   ├── planner_prompt.txt
│   ├── developer_prompt.txt
│   └── reviewer_prompt.txt
├── orchestrator.py
├── requirements.txt
└── README.md
```

## Setup (Planned)

When code modules are added, setup can follow this pattern:

1. Create a virtual environment:
   - `python -m venv .venv`
2. Activate it:
   - Windows: `.venv\Scripts\activate`
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Run the orchestrator:
   - `python orchestrator.py`

## Roadmap

- Add concrete Python implementation for each agent role.
- Add prompt templates and configurable task schemas.
- Add logging and evaluation metrics for each iteration cycle.
- Add sample tasks and benchmark-style comparisons.

## Contribution

Contributions are welcome as the project grows.  
Potential contribution areas:

- agent prompt quality,
- orchestration improvements,
- evaluation and observability,
- examples and documentation quality.

## License

License information can be added based on your preferred open-source model (MIT, Apache-2.0, etc.).

