from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

import Health_Agent.agent as Health_Agent
import Study_Agent.agent as Study_Agent
import Security_Agent.agent as Security_Agent
import Time_Agent.agent as Time_Agent

router_model = LiteLlm(
    model="ollama_chat/qwen2.5:7b",
    api_base="http://localhost:11434",
    options={
        "num_predict": 64,
        "temperature": 0.0,
    }
)

def chief_instruction(context) -> str:
    return (
        "You are 'Chief_Agent', the central routing node of Cortex.\n"
        "Your ONLY task is to transfer incoming requests to the correct sub-agent.\n\n"
        "ROUTING RULES:\n"
        "1. Workouts, 10km runs, sapate, pushups, physical health -> Transfer to 'Health_Agent'\n"
        "2. GATE prep, computer vision, OpenCV, Python, study hours -> Transfer to 'Study_Agent'\n"
        "3. Spending, budgets, security audits, secret keys -> Transfer to 'Security_Agent'\n"
        "4. Schedule adjustments, calendar updates, meetings -> Transfer to 'Time_Agent'\n\n"
        "A request containing workouts, health, GATE, study, coding, spending, security, schedule, or calendar topics is NOT general: you MUST transfer it to the matching agent.\n"
        "For greetings and other questions that do not match a routing rule, answer directly.\n"
        "TRANSFER MATCHING REQUESTS IMMEDIATELY; DO NOT ANSWER THEM YOURSELF."
    )

agent = Agent(
    model=router_model,
    name="Chief_Agent",
    instruction=chief_instruction,
    sub_agents=[
        Health_Agent.agent,
        Study_Agent.agent,
        Security_Agent.agent,
        Time_Agent.agent,
    ]
)