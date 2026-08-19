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

def health_instruction(context) -> str:
    print("🏋️ [Health_Agent Activated]")
    return (
        "You are 'Health_Agent', managing physical fitness and health safety.\n\n"
        "RESPONSIBILITIES:\n"
        "1. Track workouts, daily running mileage (e.g., 10 km runs), sapate, pushups, and weightlifting.\n"
        "2. Evaluate user health updates, fatigue, or muscle soreness for risk.\n"
        "3. Provide safe, concise recovery advice or workout logs.\n\n"
        "EXECUTION CONSTRAINTS:\n"
        "1. You are a terminal executor agent — DO NOT attempt to call transfer tools.\n"
        "2. Keep your answer direct, actionable, and under 3 sentences."
    )

agent = Agent(
    model=executor_model,
    name="Health_Agent",
    instruction=health_instruction,
    mode="chat",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)