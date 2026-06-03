# Observability Controller Beta

A lightweight observability controller that determines whether sufficient diagnostic context exists before invoking LLM, RAG, and agent workflows.

The Observability Controller evaluates whether a problem contains sufficient diagnostic context to proceed with reasoning, or whether clarification should be requested before invoking expensive downstream model calls.

## The problem

Many AI systems begin reasoning before enough diagnostic context is available.

```text
My deployment failed.
```

A model may produce a long troubleshooting response despite having almost no useful diagnostic context.

## The approach

```text
User Query
    ↓
Observability Controller
    ↓
Clarify or Proceed
    ↓
LLM / Agent / RAG System
```

If context is missing:

```json
{
  "decision": "clarify",
  "state": "underspecified"
}
```

If enough context exists:

```json
{
  "decision": "proceed",
  "state": "ready"
}
```

## Example workflow

Without controller:

```text
User
 ↓
LLM
 ↓
Generic troubleshooting response
```

With controller (static clarification):

```text
User
 ↓
Observability Controller
 ↓
Clarify
 ↓
0 additional model tokens
```

With controller (adaptive clarification):

```text
User
 ↓
Observability Controller
 ↓
Clarify
 ↓
Small clarification model call (~40-60 tokens)
 ↓
Generated clarification question
```

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

## Early benchmark results

Initial testing on ten real-world operational issues showed:

```text
Baseline workflow tokens:      14,869
Controller workflow tokens:     6,071

Observed token reduction in benchmark: ~59%
```

| Issue | Baseline Tokens | Controller Tokens |
|---|---:|---:|
| Kubernetes CrashLoopBackOff | 1,832 | 715 |
| Postgres Join Timeout | 1,703 | 688 |
| Vector Retrieval Quality | 1,611 | 595 |
| API Cache Regression | 1,648 | 645 |

Judged evaluations showed broadly comparable diagnostic quality while significantly reducing downstream token consumption.

These results are early beta findings, not final performance claims.

## Intended use

The controller is model agnostic and can be integrated ahead of any LLM, agent, or retrieval workflow.

Use before:

- OpenAI workflows
- Claude workflows
- LangGraph pipelines
- CrewAI systems
- AutoGen agents
- Internal support assistants
- Custom RAG systems

## Clarification modes

The controller supports two clarification workflows.

### Static clarification

The controller returns a fallback clarification question directly.

```text
Additional model tokens: 0
```

### Adaptive clarification

The controller can return a model agnostic clarification prompt that may be sent to OpenAI, Claude, Gemini, Ollama, Mistral, or internal models to generate a domain-specific clarification question.

Example:
```text
Input:
"The patient became unwell."

Generated clarification:
"What symptoms is the patient experiencing?"
```

Typical clarification generation cost:

```text
~40-60 tokens
```

This cost is typically much smaller than invoking a full diagnostic reasoning workflow.

## Beta access

This is currently a private beta API.

To request access or provide feedback:

info@foundscript.com

Please include a brief description of your use case when requesting access.

You will receive:

```text
API URL
API key
```

Never commit API keys into public repositories.

## Examples

```text
examples/curl_example.sh
```

Basic API call example.

```text
examples/python_example.py
```

Simple Python integration.

```text
examples/openai_gated_example.py
```

Complete OpenAI workflow example showing controller-based model gating.

```text
examples/model_agnostic_workflow.py
```

Template for Claude, Gemini, Ollama, Mistral, internal models, and other providers.

## Current status

Private beta.

The current focus is evaluating clarification-first workflows across operational diagnostics, support triage, RAG systems, and AI agents to determine their impact on token consumption, observability, and diagnostic quality.