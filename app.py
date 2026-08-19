import html
import requests
import streamlit as st

st.set_page_config(
    page_title="Cortex OS",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = "http://localhost:8080/chat"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "weekly_spend" not in st.session_state:
    st.session_state.weekly_spend = 0

if "study_hours" not in st.session_state:
    st.session_state.study_hours = 0.0

if "active_agent" not in st.session_state:
    st.session_state.active_agent = "Chief_Agent"

st.html(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 8% 0%,
                rgba(45, 134, 255, 0.11),
                transparent 28%
            ),
            radial-gradient(
                circle at 92% 0%,
                rgba(145, 82, 255, 0.09),
                transparent 27%
            ),
            #090d13;

        color: #edf3f8;

        font-family:
            Inter,
            "Segoe UI",
            Roboto,
            Arial,
            sans-serif;

        font-size: 1rem;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #101720 0%,
                #0c1219 100%
            );

        border-right: 1px solid #25313e;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.4rem;
    }

    .sidebar-brand {
        color: #f5f9fd;

        font-size: 1.55rem;

        font-weight: 800;

        letter-spacing: -0.5px;
    }

    .sidebar-subtitle {
        color: #8190a0;

        font-size: 0.84rem;

        margin-top: 5px;

        line-height: 1.5;
    }

    .sidebar-heading {
        color: #dce6ef;

        font-size: 0.78rem;

        font-weight: 750;

        text-transform: uppercase;

        letter-spacing: 1px;

        margin-bottom: 11px;
    }

    .about-card {
        padding: 14px;

        border-radius: 12px;

        border: 1px solid #29394a;

        background:
            linear-gradient(
                135deg,
                rgba(42, 111, 180, 0.10),
                rgba(111, 78, 176, 0.08)
            );
    }

    .about-title {
        color: #eef5fb;

        font-size: 0.94rem;

        font-weight: 700;

        margin-bottom: 7px;
    }

    .about-text {
        color: #7d8b9b;

        font-size: 0.78rem;

        line-height: 1.7;
    }

    .sidebar-agent {
        display: flex;

        align-items: center;

        gap: 8px;

        padding: 9px 5px;

        border-radius: 8px;

        transition: background 0.2s ease;
    }

    .sidebar-agent:hover {
        background: rgba(255, 255, 255, 0.025);
    }

    .sidebar-agent-dot {
        width: 7px;
        height: 7px;

        min-width: 7px;

        border-radius: 50%;
    }

    .sidebar-agent-name {
        color: #68c2ff;

        font-family:
            "SFMono-Regular",
            Consolas,
            monospace;

        font-size: 0.81rem;

        font-weight: 650;
    }

    .sidebar-agent-role {
        color: #6f7d8d;

        font-size: 0.71rem;
    }

    .sidebar-status {
        display: flex;

        align-items: center;

        justify-content: center;

        gap: 7px;

        color: #58d177;

        font-size: 0.73rem;

        font-weight: 650;

        margin-top: 16px;
    }

    .sidebar-status-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #3fb950;

        box-shadow:
            0 0 8px rgba(63, 185, 80, 0.75);
    }

    .cortex-header {
        position: relative;

        display: flex;

        align-items: center;

        justify-content: space-between;

        min-height: 98px;

        padding: 16px 23px;

        margin-bottom: 21px;

        border: 1px solid #2b3d50;

        border-radius: 16px;

        background:
            linear-gradient(
                110deg,
                rgba(18, 32, 49, 0.98),
                rgba(13, 18, 27, 0.98)
            );

        overflow: hidden;

        box-shadow:
            0 14px 40px rgba(0, 0, 0, 0.23);
    }

    .cortex-header::before {
        content: "";

        position: absolute;

        top: 0;
        left: 0;

        width: 60%;
        height: 3px;

        background:
            linear-gradient(
                90deg,
                #35c5ff 0%,
                #5e9cff 35%,
                #8e6cff 68%,
                #c86cff 88%,
                transparent 100%
            );
    }

    .cortex-header::after {
        content: "";

        position: absolute;

        right: -100px;
        top: -145px;

        width: 350px;
        height: 350px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(91, 108, 255, 0.12),
                transparent 66%
            );

        pointer-events: none;
    }

    .cortex-brand {
        display: flex;

        align-items: center;

        gap: 16px;

        position: relative;

        z-index: 2;
    }

    .cortex-icon {
        width: 60px;
        height: 60px;

        display: flex;

        align-items: center;

        justify-content: center;

        border-radius: 17px;

        background:
            linear-gradient(
                135deg,
                #1479b8 0%,
                #426fd1 48%,
                #7148b9 100%
            );

        border: 1px solid rgba(137, 219, 255, 0.62);

        color: #ffffff;

        font-size: 1.72rem;

        font-weight: 900;

        box-shadow:
            0 0 30px rgba(61, 169, 255, 0.20),
            inset 0 1px 0 rgba(255, 255, 255, 0.18);
    }

    .cortex-title {
        display: flex;

        align-items: baseline;

        gap: 8px;

        font-size: 2.5rem;

        font-weight: 850;

        letter-spacing: -1.7px;

        line-height: 1;

        text-shadow:
            0 0 25px rgba(78, 170, 255, 0.10);
    }

    .cortex-title-main {
        color: #f7fbff;
    }

    .cortex-title-accent {
        background:
            linear-gradient(
                90deg,
                #45c9ff 0%,
                #679eff 38%,
                #9175ff 70%,
                #d36cff 100%
            );

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;

        background-clip: text;

        filter:
            drop-shadow(
                0 0 13px rgba(118, 122, 255, 0.20)
            );
    }

    .cortex-subtitle {
        margin-top: 9px;

        color: #8b99a9;

        font-size: 0.94rem;

        font-weight: 500;

        letter-spacing: 0.25px;
    }

    .system-status {
        position: relative;

        z-index: 2;

        display: flex;

        align-items: center;

        gap: 8px;

        padding: 8px 12px;

        border-radius: 9px;

        background:
            rgba(63, 185, 80, 0.055);

        border:
            1px solid rgba(63, 185, 80, 0.23);

        color: #61d47a;

        font-size: 0.78rem;

        font-weight: 650;
    }

    .status-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #3fb950;

        box-shadow:
            0 0 9px rgba(63, 185, 80, 0.82);
    }

    .chat-title {
        display: flex;

        align-items: center;

        gap: 9px;

        color: #e1eaf2;

        font-size: 0.94rem;

        font-weight: 750;

        letter-spacing: 0.15px;

        margin: 3px 0 13px 4px;
    }

    .chat-title-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #54bcff;

        box-shadow:
            0 0 9px rgba(84, 188, 255, 0.75);
    }

    .empty-state {
        min-height: 510px;

        display: flex;

        flex-direction: column;

        align-items: center;

        justify-content: center;

        text-align: center;
    }

    .empty-icon {
        width: 76px;
        height: 76px;

        display: flex;

        align-items: center;

        justify-content: center;

        border-radius: 21px;

        background:
            linear-gradient(
                135deg,
                rgba(51, 167, 255, 0.14),
                rgba(141, 108, 255, 0.14)
            );

        border: 1px solid #3c77a3;

        color: #8bd4ff;

        font-size: 2rem;

        font-weight: 900;

        box-shadow:
            0 0 32px rgba(66, 154, 255, 0.12);

        margin-bottom: 20px;
    }

    .empty-title {
        color: #f0f6fb;

        font-size: 1.68rem;

        font-weight: 750;

        letter-spacing: -0.45px;

        margin-bottom: 9px;
    }

    .empty-text {
        color: #788696;

        font-size: 0.94rem;

        line-height: 1.75;

        max-width: 510px;
    }

    [data-testid="stChatMessage"] {
        background: transparent !important;

        border: none !important;

        padding-top: 8px;

        padding-bottom: 8px;
    }

    [data-testid="stChatMessageContent"] {
        border-radius: 14px;

        padding: 14px 17px;

        line-height: 1.75;

        font-size: 1rem;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        margin-left: 14%;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    )
    [data-testid="stChatMessageContent"] {
        background:
            linear-gradient(
                135deg,
                #1d5989,
                #19456d
            );

        border:
            1px solid #2d71a5;

        color: #ffffff;

        border-bottom-right-radius: 5px;

        box-shadow:
            0 8px 24px rgba(0, 0, 0, 0.15);
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        margin-right: 5%;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    )
    [data-testid="stChatMessageContent"] {
        background:
            linear-gradient(
                135deg,
                #151d27,
                #111820
            );

        border:
            1px solid #2b3947;

        color: #e8eef4;

        border-bottom-left-radius: 5px;

        box-shadow:
            0 8px 24px rgba(0, 0, 0, 0.14);
    }

    .agent-badge {
        display: inline-flex;

        align-items: center;

        gap: 8px;

        padding: 6px 11px;

        margin-bottom: 9px;

        border-radius: 8px;

        background:
            linear-gradient(
                90deg,
                rgba(49, 163, 255, 0.12),
                rgba(139, 103, 255, 0.10)
            );

        border:
            1px solid rgba(89, 171, 255, 0.29);

        color: #70c8ff;

        font-family:
            "SFMono-Regular",
            Consolas,
            monospace;

        font-size: 0.74rem;

        font-weight: 650;
    }

    .agent-status {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #3fb950;

        box-shadow:
            0 0 8px rgba(63, 185, 80, 0.82);
    }

    .pipeline-title {
        display: flex;

        align-items: center;

        gap: 9px;

        color: #e1eaf2;

        font-size: 0.94rem;

        font-weight: 750;

        letter-spacing: 0.15px;

        margin: 3px 0 13px 4px;
    }

    .pipeline-title-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #9b78ff;

        box-shadow:
            0 0 9px rgba(155, 120, 255, 0.75);
    }

    .pipeline {
        padding: 15px;

        border:
            1px solid #283645;

        border-radius: 13px;

        background:
            linear-gradient(
                180deg,
                #101720,
                #0d131a
            );
    }

    .pipeline-step {
        padding: 14px 10px;

        border-radius: 10px;

        text-align: center;

        background: #121a23;

        border:
            1px solid #2b3846;

        color: #dce5ed;

        font-size: 0.83rem;

        font-weight: 650;
    }

    .pipeline-step.active {
        background:
            linear-gradient(
                135deg,
                rgba(45, 139, 222, 0.13),
                rgba(126, 91, 205, 0.10)
            );

        border-color: #3976a4;

        box-shadow:
            0 0 18px rgba(61, 169, 255, 0.05);
    }

    .pipeline-label {
        display: block;

        color: #6c7b8b;

        font-size: 0.64rem;

        text-transform: uppercase;

        letter-spacing: 0.8px;

        margin-bottom: 6px;
    }

    .pipeline-agent {
        color: #70c8ff;

        font-family:
            "SFMono-Regular",
            Consolas,
            monospace;

        font-size: 0.80rem;

        font-weight: 750;
    }

    .pipeline-live {
        margin-top: 7px;

        color: #58cf76;

        font-size: 0.64rem;
    }

    .pipeline-arrow {
        height: 28px;

        line-height: 28px;

        text-align: center;

        color: #536171;

        font-size: 16px;
    }

    [data-testid="stChatInput"] {
        margin-top: 13px;
    }

    [data-testid="stChatInput"] > div {
        background:
            linear-gradient(
                135deg,
                #151e28,
                #111820
            ) !important;

        border:
            1px solid #344555 !important;

        border-radius: 15px !important;

        box-shadow:
            0 11px 32px rgba(0, 0, 0, 0.23);
    }

    [data-testid="stChatInput"] > div:focus-within {
        border-color: #448dc2 !important;

        box-shadow:
            0 0 0 1px rgba(68, 141, 194, 0.23),
            0 11px 32px rgba(0, 0, 0, 0.23);
    }

    [data-testid="stChatInput"] textarea {
        font-size: 1rem !important;
    }

    .about-cortex {
        text-align: center;

        color: #5e6b79;

        font-size: 0.72rem;

        margin-top: 19px;
    }

    @media (max-width: 900px) {

        .cortex-title {
            font-size: 1.8rem;
        }

        .system-status {
            display: none;
        }

        [data-testid="stChatMessage"]:has(
            [data-testid="chatAvatarIcon-user"]
        ) {
            margin-left: 2%;
        }

        [data-testid="stChatMessage"]:has(
            [data-testid="chatAvatarIcon-assistant"]
        ) {
            margin-right: 2%;
        }

    }

    </style>
    """
)

with st.sidebar:

    st.html(
        """
        <div class="sidebar-brand">
            Cortex OS
        </div>

        <div class="sidebar-subtitle">
            Multi-Agent Intelligence Network
        </div>
        """
    )

    st.divider()

    st.html(
        """
        <div class="sidebar-heading">
            About Cortex
        </div>

        <div class="about-card">

            <div class="about-title">
                Local AI Operating System
            </div>

            <div class="about-text">
                A personal multi-agent system that routes
                requests to specialized AI agents for
                intelligent task execution.
            </div>

        </div>
        """
    )

    st.html(
        """
        <div class="sidebar-heading">
            Active Swarm
        </div>
        """
    )

    agents = [
        ("Chief_Agent", "Router"),
        ("Health_Agent", "Fitness & Safety"),
        ("Study_Agent", "Academics & Coding"),
        ("Security_Agent", "Risk & Keys"),
        ("Time_Agent", "Schedule & Calendar"),
    ]

    for name, role in agents:

        is_active = name == st.session_state.active_agent

        color = "#3fb950" if is_active else "#566272"

        st.html(
            f"""
            <div class="sidebar-agent">

                <span
                    class="sidebar-agent-dot"
                    style="background:{color};"
                ></span>

                <span class="sidebar-agent-name">
                    {html.escape(name)}
                </span>

                <span class="sidebar-agent-role">
                    {html.escape(role)}
                </span>

            </div>
            """
        )

    st.divider()

    st.html(
        """
        <div class="sidebar-status">

            <span class="sidebar-status-dot"></span>

            Local Swarm Connected

        </div>
        """
    )

st.html(
    """
    <div class="cortex-header">

        <div class="cortex-brand">

            <div class="cortex-icon">
                C
            </div>

            <div>

                <div class="cortex-title">

                    <span class="cortex-title-main">
                        Cortex
                    </span>

                    <span class="cortex-title-accent">
                        OS
                    </span>

                </div>

                <div class="cortex-subtitle">
                    Multi-Agent Intelligence Network
                </div>

            </div>

        </div>

        <div class="system-status">

            <span class="status-dot"></span>

            Local Swarm

        </div>

    </div>
    """
)

chat_column, pipeline_column = st.columns(
    [3.7, 1.15],
    gap="medium"
)

with chat_column:

    st.html(
        """
        <div class="chat-title">

            <span class="chat-title-dot"></span>

            Cortex Chat

        </div>
        """
    )

    if not st.session_state.messages:

        st.html(
            """
            <div class="empty-state">

                <div class="empty-icon">
                    C
                </div>

                <div class="empty-title">
                    How can Cortex help you?
                </div>

                <div class="empty-text">
                    Ask anything. Cortex will route your request
                    through the appropriate intelligence agent.
                </div>

            </div>
            """
        )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            if message["role"] == "assistant":

                message_agent = message.get(
                    "agent",
                    "Chief_Agent"
                )

                st.html(
                    f"""
                    <div class="agent-badge">

                        <span class="agent-status"></span>

                        {html.escape(message_agent)}

                    </div>
                    """
                )

            st.markdown(
                message["content"]
            )

with pipeline_column:

    active_agent = st.session_state.active_agent

    st.html(
        f"""
        <div class="pipeline-title">

            <span class="pipeline-title-dot"></span>

            Intelligence Pipeline

        </div>

        <div class="pipeline">

            <div class="pipeline-step">

                <span class="pipeline-label">
                    Stage 01
                </span>

                User Input

            </div>

            <div class="pipeline-arrow">
                ↓
            </div>

            <div class="pipeline-step active">

                <span class="pipeline-label">
                    Stage 02
                </span>

                Chief_Agent

                <div class="pipeline-live">
                    Router
                </div>

            </div>

            <div class="pipeline-arrow">
                ↓
            </div>

            <div class="pipeline-step active">

                <span class="pipeline-label">
                    Active Agent
                </span>

                <span class="pipeline-agent">
                    {html.escape(active_agent)}
                </span>

                <div class="pipeline-live">
                    ● Working Agent
                </div>

            </div>

            <div class="pipeline-arrow">
                ↓
            </div>

            <div class="pipeline-step">

                <span class="pipeline-label">
                    Final Stage
                </span>

                Response

            </div>

        </div>
        """
    )

user_prompt = st.chat_input(
    "Ask Cortex anything..."
)

if user_prompt:

    with chat_column:

        with st.chat_message("user"):

            st.markdown(user_prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    with chat_column:

        with st.chat_message("assistant"):

            with st.spinner(
                "Chief_Agent is routing your request..."
            ):

                try:

                    response = requests.post(
                        BACKEND_URL,
                        json={"message": user_prompt},
                        timeout=120,
                    )

                    response.raise_for_status()

                    data = response.json()

                    agent_reply = data.get(
                        "reply",
                        "No response generated."
                    )

                    active_agent = data.get(
                        "active_agent",
                        "Chief_Agent"
                    )

                    updated_state = data.get(
                        "updated_state",
                        {}
                    )

                    st.session_state.active_agent = (
                        active_agent
                    )

                    st.session_state.weekly_spend = (
                        updated_state.get(
                            "current_weekly_spend",
                            st.session_state.weekly_spend
                        )
                    )

                    st.session_state.study_hours = (
                        updated_state.get(
                            "study_hours_today",
                            st.session_state.study_hours
                        )
                    )

                    st.html(
                        f"""
                        <div class="agent-badge">

                            <span class="agent-status"></span>

                            {html.escape(active_agent)}

                        </div>
                        """
                    )

                    st.markdown(
                        agent_reply
                    )

                except requests.exceptions.Timeout:

                    agent_reply = (
                        "System Alert: Request timed out. "
                        "Ensure local Ollama instance is active."
                    )

                    st.markdown(
                        agent_reply
                    )

                except requests.exceptions.RequestException:

                    agent_reply = (
                        "System Alert: Backend unreachable. "
                        "Ensure FastAPI server is running on port 8080."
                    )

                    st.markdown(
                        agent_reply
                    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": agent_reply,
            "agent": st.session_state.active_agent,
        }
    )

    st.rerun()

st.html(
    """
    <div class="about-cortex">
        Cortex OS · Local Multi-Agent Personal Operating System
    </div>
    """
)