from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Dedicated terminal executor model using qwen2.5:7b
executor_model = LiteLlm(
    model="ollama_chat/qwen2.5:7b",
    api_base="http://localhost:11434",
    options={
        "num_predict": 128,   # Concise terminal responses
        "temperature": 0.2,   # Low variance for high precision
    }
)

def time_instruction(context) -> str:
    print("⏰ [Time_Agent Activated]")
    return (
        "You are 'Time_Agent', managing calendars, event adjustments, and daily schedules.\n\n"
        "RESPONSIBILITIES:\n"
        "1. Process calendar additions, event updates, and meeting reschedules.\n"
        "2. Keep track of day-to-day timeline shifts and time allocation updates.\n"
        "3. Provide direct, concise schedule summaries or confirmation steps.\n\n"
        "EXECUTION CONSTRAINTS:\n"
        "1. You are a terminal executor agent — DO NOT attempt to call transfer tools.\n"
        "2. Keep your answer direct, actionable, and under 3 sentences."
    )

agent = Agent(
    model=executor_model,
    name="Time_Agent",
    instruction=time_instruction,
    mode="chat",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)