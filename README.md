# Observability Controller Beta

A lightweight control layer that detects ambiguous or underspecified requests before invoking LLM, RAG, and agent workflows.

The Observability Controller evaluates whether a request contains sufficient information to proceed with reasoning, retrieval, planning, or execution. When critical information is missing, the controller can request clarification before downstream systems consume compute, retrieve documents, call tools, or generate responses.

---

## Why this matters

Many AI systems begin reasoning before they have enough information.

Example:

```text
My deployment failed.
```

Despite having almost no useful context, a model may immediately begin troubleshooting, retrieving documents, generating plans, or calling tools.

This can lead to:

- Generic or inaccurate responses
- Incorrect task decomposition
- Unnecessary retrieval operations
- Wasted agent execution
- Increased model consumption

The Observability Controller attempts to identify missing information before reasoning begins.

---

## How it works

```text
User Query
    ↓
Observability Controller
    ↓
Clarify or Proceed
    ↓
LLM / Agent / RAG System
```

If information is missing:

```json
{
  "decision": "clarify",
  "state": "underspecified"
}
```

If sufficient information exists:

```json
{
  "decision": "proceed",
  "state": "ready"
}
```

---

## Example ambiguity detection

### Ambiguous request

Input:

```text
The system is broken.
```

Output:

```json
{
  "decision": "clarify",
  "state": "underspecified"
}
```

Example clarification:

```text
Which system is affected and what behaviour are you observing?
```

### Sufficiently specified request

Input:

```text
The Kubernetes deployment entered CrashLoopBackOff after upgrading from v1.31 to v1.32.
```

Output:

```json
{
  "decision": "proceed",
  "state": "ready"
}
```

---

## Example workflows

### Standard workflow

```text
User
 ↓
LLM / Agent
 ↓
Reasoning begins immediately
```

### Clarification-first workflow

```text
User
 ↓
Observability Controller
 ↓
Clarify or Proceed
 ↓
LLM / Agent
```

### Agent workflow example

Without clarification:

```text
User
 ↓
Planner Agent
 ↓
Research Agent
 ↓
Execution Agent
```

With clarification:

```text
User
 ↓
Observability Controller
 ↓
Clarification
 ↓
Planner Agent
 ↓
Research Agent
 ↓
Execution Agent
```

The controller is designed to reduce ambiguity before downstream workflows begin planning, retrieval, execution, or reasoning.

---

## API

### Endpoint

```http
POST /observe
```

### Request

```json
{
  "message": "My deployment failed."
}
```

### Headers

```text
Content-Type: application/json
x-api-key: YOUR_API_KEY
```

---

## Early benchmark results

Initial testing on ten real-world operational issues showed:

```text
Baseline workflow tokens:      14,869
Controller workflow tokens:     6,071

Observed token reduction: ~59%
```

| Issue | Baseline Tokens | Controller Tokens |
|---------|---------:|---------:|
| Kubernetes CrashLoopBackOff | 1,832 | 715 |
| Postgres Join Timeout | 1,703 | 688 |
| Vector Retrieval Quality | 1,611 | 595 |
| API Cache Regression | 1,648 | 645 |

Judged evaluations showed broadly comparable diagnostic quality while significantly reducing downstream token consumption.

These results are early beta findings and should not be considered final performance claims.

---

## Workflow evaluation

The controller was evaluated across 24 multi-step workflow executions involving planner, researcher, analyst and writer stages.

Results:

```text
Workflow executions:        24
Completed successfully:     22
Stopped as underspecified:   2
```

In 7 cases, ambiguity or degraded intermediate outputs were identified and corrected during evaluation.

The controller prevented execution of workflows that remained underspecified and allowed sufficiently specified workflows to proceed through the execution chain.

These results are exploratory beta findings intended to evaluate clarification-first workflow control rather than establish final performance claims.

---

## Intended use

The controller is model agnostic and can be integrated ahead of:

- OpenAI workflows
- Claude workflows
- LangGraph pipelines
- CrewAI systems
- AutoGen agents
- Internal support assistants
- Operational triage systems
- Customer support workflows
- Custom RAG systems
- Internal AI copilots

Typical use cases include:

- Incident triage
- Support ticket routing
- AI agent workflows
- Retrieval-augmented generation (RAG)
- Internal engineering assistants
- Operational diagnostics

---

## Clarification modes

The controller currently supports two clarification workflows.

### Static clarification

Returns a predefined clarification question directly.

```text
Additional model tokens: 0
```

### Adaptive clarification

Returns a model agnostic clarification prompt that may be sent to OpenAI, Claude, Gemini, Ollama, Mistral, or internal models to generate a context-specific clarification question.

Example:

```text
Input:
"The patient became unwell."

Generated clarification:
"What symptoms is the patient experiencing?"
```

Typical clarification generation cost:

```text
~40–60 tokens
```

This is typically much smaller than invoking a full reasoning, retrieval, or diagnostic workflow.

---

## Beta access

This is currently a private beta API.

To request access or provide feedback:

**info@foundscript.com**

Please include a short description of your use case.

You will receive:

```text
API URL
API key
```

Never commit API keys into public repositories.

---

## Examples

### Basic API call

```text
examples/curl_example.sh
```

### Python integration

```text
examples/python_example.py
```

### OpenAI workflow example

```text
examples/openai_gated_example.py
```

### Model agnostic workflow example

```text
examples/model_agnostic_workflow.py
```

Supports Claude, Gemini, Ollama, Mistral, internal models and other providers.

---

## Current status

Private beta.

Current evaluation focuses on:

- Operational diagnostics
- Support triage
- RAG systems
- Agent workflows
- Internal AI assistants

The objective is to determine whether clarification-first reasoning improves downstream workflow quality, execution efficiency and resource utilisation before reasoning begins.

Future evaluation areas include:

- Clarification accuracy
- Agent workflow impact
- Retrieval quality improvements
- Tool call reduction
- Human preference testing