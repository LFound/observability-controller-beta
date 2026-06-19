# Observability Controller Beta

> Detect underspecified support, operational and workflow requests before invoking LLM, RAG and agent systems.

![Status](https://img.shields.io/badge/status-private_beta-blue)
![Evaluations](https://img.shields.io/badge/evaluations-107-success)
![Real%20World](https://img.shields.io/badge/real_world-97%25-success)
![Workflow](https://img.shields.io/badge/token_reduction-43%25-brightgreen)

A lightweight control layer that evaluates whether a request contains sufficient information to proceed with reasoning, retrieval, planning or execution.

When critical information is missing, the controller can request clarification before downstream systems consume compute, retrieve documents, call tools or generate responses.

The controller is particularly suited to support, operational and workflow-driven AI systems where incomplete requests can trigger unnecessary reasoning, retrieval or execution.

The controller operates before the model or workflow and does not depend on a specific LLM provider, framework or agent architecture.

Current beta evaluation:

```text
107 labelled evaluations
4 benchmark families

Conversation benchmark:      100.0%
Support benchmark:           100.0%
Cross-domain benchmark:      100.0%
Real-world benchmark:         97.3%

Workflow token reduction:     43.0%
```
---

## Why this matters

Many AI systems begin reasoning before they have enough information.

Example:

```text
My deployment failed.
```

Despite having almost no useful context, a model may immediately begin troubleshooting, retrieving documents, generating plans or calling tools.

This can lead to:

- Generic or inaccurate responses
- Incorrect task decomposition
- Unnecessary retrieval operations
- Wasted agent execution
- Agent drift
- Repeated reasoning cycles
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

The controller is designed to reduce ambiguity before downstream workflows begin planning, retrieval, execution or reasoning.

---

## API

### Endpoint

```http
POST /observe
```

### Request

```json
{
  "message": "My deployment failed.",
  "mode": "sufficiency_v2"
}
```

### Headers

```text
Content-Type: application/json
x-api-key: YOUR_API_KEY
```

---

## Data handling

The controller is stateless by design.

It evaluates the request supplied to `/observe` and returns a routing decision such as `proceed` or `clarify`.

The controller does not require:

- A database
- Conversation memory
- Stored prompt history
- Training on user data

The current beta API does not intentionally retain user prompts between requests. No request-body logging is implemented in the application code.

Operators should still review deployment logs, reverse-proxy logs and hosting-provider settings to ensure request bodies are not captured unintentionally.

Do not send sensitive personal, medical, financial or regulated data during beta testing unless a separate data processing agreement is in place.

---

## Evaluation

The controller has been evaluated across multiple benchmark families designed to assess context sufficiency detection, clarification behaviour and workflow efficiency.

Current evaluation covers:

```text
107 labelled evaluations
4 benchmark families
```

### Benchmark summary

| Benchmark                      |     Cases | Result |
| ------------------------------ | --------: | -----: |
| Conversation evaluation        |        30 | 100.0% |
| Support benchmark              |        20 | 100.0% |
| Cross-domain support benchmark |        20 | 100.0% |
| Real-world prompt benchmark    | 37 scored |  97.3% |

### Conversation evaluation

Multi-turn clarification benchmark:

```text
Threads:                 10
Total turns:             30

Correct:                 30 / 30
Accuracy:                100.0%

False positives:         0
False negatives:         0
```

### Support benchmark

Generic support and troubleshooting requests:

```text
Scored cases:            20
Correct:                 20

Accuracy:                100.0%

Clarify precision:       100.0%
Clarify recall:          100.0%
```

### Cross-domain benchmark

Domains included:

* Telecommunications
* Ecommerce
* Banking
* Healthcare administration
* General customer support

```text
Scored cases:            20
Correct:                 20

Accuracy:                100.0%

Clarify precision:       100.0%
Clarify recall:          100.0%
```

### Real-world prompt benchmark

Prompts adapted from real-world issue reporting styles, support requests, operational incidents and technical troubleshooting scenarios.

```text
Scored cases:            37
Correct:                 36

Accuracy:                97.3%

Clarify precision:       100.0%
Clarify recall:           94.4%

False positives:         0
False negatives:         1
```

### Workflow token benchmark

Evaluation of clarification-first workflows versus a naive baseline workflow.

```text
Cases:                       10

Baseline workflow tokens:    5,498
Controller workflow tokens:  3,136

Tokens saved:                2,362
Reduction:                   43.0%
```

These results suggest that identifying insufficient context before reasoning begins can reduce unnecessary model activity in workflows where clarification would otherwise occur after an incomplete response.

### Limitations

Current evaluation should be considered engineering validation rather than a formal academic benchmark.

Limitations include:

* Relatively small sample sizes
* Hand-labelled evaluation sets
* Limited production traffic
* No human preference studies
* Limited real-world deployment data

Future evaluation will focus on larger frozen benchmark sets, production trace analysis and agentic workflow testing.

---

## Experimental workflow control

In addition to request-level clarification, the controller has been evaluated experimentally within multi-stage workflows involving planner, researcher, analyst and writer stages.

Early evaluation explored:

- Intermediate handoff validation
- Ambiguity detection between workflow stages
- Repair and revalidation of degraded intermediate outputs
- Workflow stopping when sufficient context could not be recovered

These capabilities remain experimental and are not currently exposed through the public API.

---

## Intended use

The Observability Controller operates before the model or workflow and does not depend on a specific LLM provider, framework or agent architecture.

It can be integrated ahead of:

* OpenAI workflows
* Claude workflows
* Gemini workflows
* LangGraph pipelines
* CrewAI systems
* AutoGen agents
* Custom RAG systems
* Internal AI copilots
* Proprietary agent frameworks

The controller is particularly suited to environments where users frequently submit incomplete requests and downstream reasoning, retrieval or execution can be expensive.

Typical use cases include:

* Customer support systems
* Support ticket routing
* IT and engineering helpdesks
* Incident triage
* Operational diagnostics
* Internal AI assistants
* Agent workflows
* Retrieval augmented generation (RAG)
* Knowledge management systems
* Internal engineering assistants
* Workflow orchestration pipelines

---

## Clarification modes

The controller currently supports two clarification workflows.

### Direct clarification

Returns a predefined clarification question directly.

```text
Additional model tokens: 0
```

### Model-generated clarification

Returns a model agnostic clarification prompt that may be sent to OpenAI, Claude, Gemini, Ollama, Mistral or internal models to generate a context-specific clarification question.

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

This is typically much smaller than invoking a full reasoning, retrieval or diagnostic workflow.

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

Areas currently under evaluation include:

- Clarification accuracy
- Agent workflow impact
- Retrieval quality improvements
- Tool call reduction
- Human preference testing
- Workflow repair and revalidation