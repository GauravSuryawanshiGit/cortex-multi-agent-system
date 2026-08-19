import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from typing import Any
from dotenv import load_dotenv
from fastapi import FastAPI, Response
from pydantic import BaseModel
from google.genai import types

from google.adk.apps import App
try:
    from google.adk.apps import ContextCacheConfig
except ImportError:
    try:
        from google.adk.apps.app import ContextCacheConfig
    except ImportError:
        ContextCacheConfig = None

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import uvicorn

import Chief_Agent.agent as chief
import Health_Agent.agent as health
import Security_Agent.agent as security
import Study_Agent.agent as study
import Time_Agent.agent as time
from utils.state_manager import LifeOSState

base_dir = Path(__file__).resolve().parent
root_env_path = base_dir / ".env"

if root_env_path.exists():
    load_dotenv(dotenv_path=root_env_path)
    print(f"Success: System core loaded root security key from {root_env_path}")

shared_memory = LifeOSState()

cache_config = ContextCacheConfig() if ContextCacheConfig else None
adk_app = App(
    name="cortex",
    root_agent=chief.agent,
    context_cache_config=cache_config,
)

session_service = InMemorySessionService()

runner = Runner(
    app=adk_app,
    session_service=session_service,
)

specialized_runners = {
    "Health_Agent": Runner(
        app=App(name="cortex", root_agent=health.agent, context_cache_config=cache_config),
        session_service=session_service,
    ),
    "Study_Agent": Runner(
        app=App(name="cortex", root_agent=study.agent, context_cache_config=cache_config),
        session_service=session_service,
    ),
    "Security_Agent": Runner(
        app=App(name="cortex", root_agent=security.agent, context_cache_config=cache_config),
        session_service=session_service,
    ),
    "Time_Agent": Runner(
        app=App(name="cortex", root_agent=time.agent, context_cache_config=cache_config),
        session_service=session_service,
    ),
}


def select_specialized_runner(message_text: str):
    lowered_message = message_text.lower()
    routing_terms = {
        "Health_Agent": ("workout", "run", "pushup", "fitness", "health"),
        "Study_Agent": ("gate", "study", "coding", "python", "opencv", "computer vision"),
        "Security_Agent": ("spending", "budget", "security", "secret key", "password"),
        "Time_Agent": ("schedule", "calendar", "meeting", "reschedule"),
    }
    for agent_name, terms in routing_terms.items():
        if any(term in lowered_message for term in terms):
            return specialized_runners[agent_name], agent_name
    return runner, "Chief_Agent"

app = FastAPI(title="Cortex API")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
async def root():
    return {"status": "online", "app": "cortex"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)


@app.post("/chat")
async def chat(request: ChatRequest) -> dict[str, Any]:
    user_id = "streamlit-user"
    session_id = "streamlit-session"
    selected_runner, selected_agent = select_specialized_runner(request.message)
    active_session_id = session_id if selected_agent == "Chief_Agent" else f"{session_id}-{selected_agent}"
    
    session = await session_service.get_session(
        app_name="cortex",
        user_id=user_id,
        session_id=active_session_id
    )
    
    if not session:
        session = await session_service.create_session(
            app_name="cortex",
            user_id=user_id,
            session_id=active_session_id,
            state=shared_memory.model_dump(),
        )

    message = types.Content(
        role="user",
        parts=[types.Part(text=request.message)],
    )
    
    reply = ""
    active_agent = selected_agent
    
    try:
        async for event in selected_runner.run_async(
            user_id=user_id,
            session_id=active_session_id,
            new_message=message,
        ):
            try:
                if hasattr(event, "author") and event.author:
                    active_agent = event.author
                elif hasattr(event, "agent_name") and event.agent_name:
                    active_agent = event.agent_name

                if event.is_final_response() and event.content and event.content.parts:
                    reply = "".join(part.text or "" for part in event.content.parts)
            except Exception:
                print(traceback.format_exc())
                
    except Exception as err:
        print(f"Ollama Agent Runner Failure: {err}")
        print(traceback.format_exc())
        error_text = str(err)
        if "model" in error_text and "not found" in error_text:
            reply = f"Ollama model is not installed: {error_text}"
        elif "connection" in error_text.lower() or "connect" in error_text.lower():
            reply = "Ollama is unavailable at http://localhost:11434. Start Ollama and try again."
        else:
            reply = f"Agent execution failed: {error_text}"

    updated_session = await session_service.get_session(
        app_name="cortex",
        user_id=user_id,
        session_id=active_session_id
    )
    updated_state = updated_session.state if updated_session else shared_memory.model_dump()

    return {
        "reply": reply or "No response was generated.",
        "active_agent": active_agent,
        "updated_state": updated_state
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)