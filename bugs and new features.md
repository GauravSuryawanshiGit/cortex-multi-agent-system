# Cortex — Bugs & Expected Features

This document records the current routing issues identified during Cortex multi-agent testing and defines the expected behavior for the next iteration.

---

# 1. Multi-Agent Routing Bug

## Issue

The `Chief_Agent` currently fails to correctly decompose requests containing multiple independent intents.

A single user message can contain requests for multiple specialized agents, but the system frequently transfers the entire request to only one agent.

### Test Input

```text
Create a 10 km running plan, give me a GATE Computer Vision and Python study roadmap, review my monthly budget and API-key security, and organize my meetings and schedule for this week.
```

### Actual Behavior

The request was routed to:

```text
Health_Agent
```

The system then returned:

```text
System Alert: Request timed out.
Ensure local Ollama instance is active.
```

### Expected Behavior

The `Chief_Agent` should decompose the request:

```text
10 km running
        ↓
Health_Agent

GATE / Computer Vision / Python
        ↓
Study_Agent

Budget / API-key security
        ↓
Security_Agent

Meetings / Schedule
        ↓
Time_Agent
```

The individual responses should then be combined into one final response.

---

# 2. Time_Agent Routing Bug

## Issue

A schedule-related request was incorrectly routed to `Study_Agent`.

### Test Input

```text
Help me organize my schedule for this week. I have meetings, study sessions, project work, and exercise that need to be planned.
```

### Actual Behavior

The request was handled by:

```text
Study_Agent
```

The response generated a study-oriented weekly schedule.

### Expected Behavior

The request should be routed to:

```text
Chief_Agent
      ↓
Time_Agent
```

`Study_Agent` should only handle the study-related portion if the request explicitly requires study planning as a separate specialized task.

---

# 3. Multi-Agent Response Aggregation

## Issue

The current architecture appears to support single-agent handoff more reliably than multi-agent orchestration.

When a prompt contains multiple domains, the system does not consistently invoke all required agents.

### Expected Feature

Implement a multi-agent orchestration layer:

```text
                         USER
                           │
                           ▼
                    ┌─────────────┐
                    │ Chief_Agent │
                    │ Intent      │
                    │ Detection   │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
       Health           Study          Security
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                         Time
                           │
                           ▼
                    Response Aggregator
                           │
                           ▼
                     Final Response
```

The important requirement is that **all specialized agents are independent children of `Chief_Agent`**.

`Time_Agent` must not depend on `Study_Agent`, `Health_Agent`, or any other specialized agent.

---

# 4. Ollama Timeout Issue

## Issue

Complex multi-agent prompts occasionally produce:

```text
System Alert: Request timed out.
Ensure local Ollama instance is active.
```

This occurred while testing complex prompts containing multiple intents.

### Example

```text
Create a 10 km running plan, give me a GATE Computer Vision and Python study roadmap, review my monthly budget and API-key security, and organize my meetings and schedule for this week.
```

### Expected Behavior

The system should:

* Detect the individual intents.
* Route each intent independently.
* Avoid sending the entire complex request to a single agent.
* Handle agent execution independently.
* Aggregate completed responses.
* Provide a meaningful error only for the specific agent that fails.

For example:

```text
Health_Agent      → Success
Study_Agent       → Success
Security_Agent    → Success
Time_Agent        → Timeout

Final Response:
Health section
Study section
Security section
Time section → temporarily unavailable
```

A failure in one agent should not necessarily cause the entire request to fail.

---

# 5. Expected Feature — Intent Decomposition

The `Chief_Agent` should support multiple intents in one message.

### Example

```text
Create a workout plan,
prepare a GATE roadmap,
review my budget,
and organize my schedule.
```

The router should produce something similar to:

```text
[
    {
        "intent": "fitness",
        "agent": "Health_Agent"
    },
    {
        "intent": "study",
        "agent": "Study_Agent"
    },
    {
        "intent": "security_budget",
        "agent": "Security_Agent"
    },
    {
        "intent": "schedule",
        "agent": "Time_Agent"
    }
]
```

---

# 6. Expected Feature — Parallel Agent Execution

When multiple independent tasks are detected, the system should ideally execute them independently or in parallel.

### Desired Flow

```text
                    Chief_Agent
                         │
              ┌──────────┼──────────┐
              │          │          │
              ▼          ▼          ▼
           Health      Study     Security
              │          │          │
              └──────────┼──────────┘
                         │
                         ▼
                       Time
                         │
                         ▼
                   Aggregator
```

Where technically possible, independent agents should be executed concurrently to reduce total response time.

---

# 7. Expected Feature — Response Aggregation

After specialized agents finish their tasks, Cortex should combine their results.

Example final structure:

```text
## Fitness
[Health_Agent response]

## GATE / Computer Vision
[Study_Agent response]

## Budget & Security
[Security_Agent response]

## Schedule
[Time_Agent response]
```

The user should receive one coherent answer instead of multiple unrelated responses.

---

# 8. Expected Feature — Agent Ownership Boundaries

Each agent should have a clearly defined responsibility.

| Agent            | Responsibility                                    |
| ---------------- | ------------------------------------------------- |
| `Health_Agent`   | Health, fitness, workouts, running                |
| `Study_Agent`    | GATE, Computer Vision, Python, technical learning |
| `Security_Agent` | Security, API keys, secrets, budget               |
| `Time_Agent`     | Calendar, meetings, scheduling, time management   |
| `Chief_Agent`    | Intent detection, routing, orchestration          |

A specialized agent should not answer unrelated domains when another specialized agent is available.

---

# 9. Expected Feature — Improved Intent Classification

The router should classify based on **semantic intent**, not only keyword matching.

For example:

```text
"My week is completely unorganized. Help me manage my commitments."
```

should route to:

```text
Time_Agent
```

even though the word "schedule" may not appear.

Similarly:

```text
"I want to become fit enough to complete a 10 km run."
```

should route to:

```text
Health_Agent
```

---

# 10. Expected Feature — Error Isolation

If one agent fails, Cortex should not discard successful results from other agents.

### Desired Behavior

```text
Health_Agent      ✓ Completed
Study_Agent       ✓ Completed
Security_Agent    ✓ Completed
Time_Agent        ✗ Timeout

                 ↓

Final Response
────────────────────────────
Health            ✓
Study             ✓
Security          ✓
Schedule          ⚠ Temporarily unavailable
```

This provides a more resilient multi-agent architecture.

---

# 11. Expected Feature — Better Timeout Handling

The system should distinguish between:

```text
Agent timeout
Ollama unavailable
Model unavailable
Invalid agent response
Routing failure
```

Instead of always displaying:

```text
System Alert: Request timed out.
Ensure local Ollama instance is active.
```

The error message should identify the actual failing component.

---

# 12. Regression Test Suite

The following tests should pass after the routing system is updated.

| Test | Input Type                           | Expected Agent(s)         |
| ---- | ------------------------------------ | ------------------------- |
| 1    | 10 km running plan                   | Health                    |
| 2    | GATE Computer Vision                 | Study                     |
| 3    | Budget + API security                | Security                  |
| 4    | Weekly schedule                      | Time                      |
| 5    | Running + GATE                       | Health + Study            |
| 6    | Running + GATE + Budget              | Health + Study + Security |
| 7    | Running + GATE + Budget + Schedule   | All 4                     |
| 8    | Schedule + Security + Study + Health | All 4                     |
| 9    | Indirect fitness request             | Health                    |
| 10   | Indirect scheduling request          | Time                      |

---

# 13. Definition of Done

The multi-agent routing enhancement will be considered complete when:

* [ ] Single-agent routing works correctly.
* [ ] Multi-intent requests are detected.
* [ ] Multiple specialized agents can be invoked for one request.
* [ ] `Time_Agent` correctly handles scheduling requests.
* [ ] All four specialized agents remain direct children of `Chief_Agent`.
* [ ] Agent responses can be aggregated.
* [ ] One agent failure does not destroy successful results from other agents.
* [ ] Ollama/model timeout errors are isolated and descriptive.
* [ ] Complex multi-agent prompts complete reliably.
* [ ] All regression tests pass.

---

# Priority

## High Priority

1. Multi-intent detection
2. Correct `Time_Agent` routing
3. Multi-agent orchestration
4. Response aggregation
5. Timeout/error isolation

## Medium Priority

6. Parallel agent execution
7. Semantic intent classification
8. Improved error messages

---

# Summary

The current Cortex system successfully demonstrates **single-agent routing**, but testing shows that complex multi-intent requests are not yet being reliably decomposed across specialized agents.

The next architectural improvement should focus on transforming:

```text
User
 ↓
Chief_Agent
 ↓
One Agent
```

into:

```text
User
 ↓
Chief_Agent
 ↓
Intent Decomposition
 ↓
Multiple Specialized Agents
 ↓
Response Aggregation
 ↓
Final Response
```

This will make Cortex a true **multi-agent orchestration system** rather than a single-agent router.
