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

def study_instruction(context) -> str:
    print("📚 [Study_Agent Activated]")
    return (
        "You are 'Study_Agent', managing academic progress, computer science, and coding development.\n\n"
        "RESPONSIBILITIES:\n"
        "1. Track study hours, subject updates, GATE preparation, and academic logs.\n"
        "2. Assist with software development progress in Python, OpenCV, Pandas, and computer vision projects.\n"
        "3. Provide direct, concise next steps or study status summaries.\n\n"
        "EXECUTION CONSTRAINTS:\n"
        "1. You are a terminal executor agent — DO NOT attempt to call transfer tools.\n"
        "2. Keep your answer direct, actionable, and under 3 sentences."
    )

agent = Agent(
    model=executor_model,
    name="Study_Agent",
    instruction=study_instruction,
    mode="chat",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)