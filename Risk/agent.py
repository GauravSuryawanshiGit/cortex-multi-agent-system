from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


executor_model = LiteLlm(
    model="ollama_chat/qwen2.5:7b",
    api_base="http://localhost:11434",
    options={
        "num_predict": 128,   
        "temperature": 0.2,   
    }
)

def security_instruction(context) -> str:
    print("🛡️ [Security_Agent Activated]")
    return (
        "You are 'Security_Agent', managing financial risk, budget allocations, "
        "and digital privacy/log security.\n\n"
        "RESPONSIBILITIES:\n"
        "1. Review spending updates, budget limits, and resource allocations for financial risk.\n"
        "2. Audit user inputs or system logs for exposed API keys, passwords, or credentials.\n"
        "3. Provide concise warnings, safety steps, or approval status.\n\n"
        "EXECUTION CONSTRAINTS:\n"
        "1. You are a terminal executor agent — DO NOT attempt to call transfer tools.\n"
        "2. Keep your answer direct, actionable, and under 3 sentences."
    )

agent = Agent(
    model=executor_model,
    name="Security_Agent",
    instruction=security_instruction,
    mode="chat",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)