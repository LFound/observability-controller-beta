# Observability Controller Beta

A lightweight pre-reasoning observability controller for LLM, RAG and agent workflows.

The Observability Controller evaluates whether a problem contains sufficient diagnostic context to proceed with reasoning, or whether clarification should be requested before invoking expensive downstream model calls.

## The problem

Most AI systems begin reasoning immediately.

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
  "state": "underspecified",
  "clarification_question": "What specific system is affected, and what error messages, logs, recent changes, environment, metrics, example input/output, or reproduction steps are available?"
}
```

If enough context exists:

```json
{
  "decision": "proceed",
  "state": "ready"
}
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

Observed reduction in benchmark: ~59%
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

Use before:

- OpenAI workflows
- Claude workflows
- LangGraph pipelines
- CrewAI systems
- AutoGen agents
- Internal support assistants
- Custom RAG systems

## Beta access

This is currently a private beta API.

To request access, contact Luke Found / FoundScript.

You will receive:

```text
API URL
API key
```

Never commit API keys into public repositories.

## Examples

See:

```text
examples/python_example.py
examples/curl_example.sh
```

## Current status

Private beta.

The current focus is evaluating whether clarification-first workflows can improve operational diagnostics, reduce token consumption and improve reasoning efficiency across LLM and agent systems.