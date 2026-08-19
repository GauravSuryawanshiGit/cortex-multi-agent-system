## Live System View

![Cortex AI Operational Dashboard UI](image_7C2KM_.png)

# Cortex Multi-Agent Core Setup Guide

This repository contains a localized, modular Python multi-agent system powered by `google.adk` and `Ollama`. The central routing hub (**Chief_Agent**) dynamically analyzes and transfers user prompts to specialised sub-agents.

## Repository Structure

```text
Cortex_Core/
│
├── main.py                 # Central Orchestrator & Router
├── image_7C2KM_.png        # UI Dashboard Screenshot
│
├── Health_Agent/
│   ├── __init__.py         # Module Exposer
│   └── agent.py            # Health/Fitness Specialized Worker
│
├── Study_Agent/
│   ├── __init__.py
│   └── agent.py            # GATE/Computer Vision Worker
│
├── Security_Agent/
│   ├── __init__.py
│   └── agent.py            # Secret Audit & Budget Worker
│
└── Time_Agent/
    ├── __init__.py
    └── agent.py            # Calendar & Schedule Worker
```

Each autonomous sub-agent operates as an isolated module within its own folder, completely managed by the central top-level architecture.

---

# System Requirements

Before running the agents, ensure you have the following prerequisites installed on your local machine:

1. **Ollama**: [Download Ollama](https://ollama.com) and pull your local model:
   ```bash
   ollama pull qwen2.5:3b
   ```
2. **Python Dependencies**: Install the Google Agent Development Kit framework:
   ```bash
   pip install google-adk
   ```

---

# Project Configuration

The central system assumes an active local inference host engine running in the background.

### API Core Target Configuration
Ensure your local host runtime configuration inside `main.py` matches your custom deployment parameters:
* **Host Endpoint**: `http://localhost:11434`
* **Target Model Node**: `ollama_chat/qwen2.5:3b`

---

# Clone and Initialize

1. Open your terminal or development environment.
2. Clone the repository framework to your computer:
   ```bash
   git clone https://github.com
   cd Cortex_Core
   ```

---

# Verification and Run Loop

### Starting the Core Orchestrator
Execute the entry script from the root directory of your workspace:

```bash
python main.py
```

---

# Intelligence Routing Pipeline

The `Chief_Agent` inspects incoming queries and triggers immediate sub-agent context transfers based on the following classification matrices:

| Input Focus Keywords | Assigned Hand-off Target |
| :--- | :--- |
| Workouts, 10km runs, pushups, physical health | **Health_Agent** |
| GATE prep, computer vision, OpenCV, Python | **Study_Agent** |
| Spending, budgets, security audits, secret keys | **Security_Agent** |
| Schedule adjustments, calendar updates, meetings | **Time_Agent** |

---

# Security & Secrets Compliance

Since this system handles personal information such as secret API keys, budget ledger records, and private schedules:

* **Local Inference**: All operations run locally inside your system container through Ollama. No personal workspace telemetry data is sent to external clouds.
* **Environment Guards**: Never commit raw private tokens, path strings, or secret strings to remote Git branches. Add any config override files to your local `.gitignore`.
