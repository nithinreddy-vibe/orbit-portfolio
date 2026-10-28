# Orbit Personal AI System - Architecture and Safety Design

Status: Phase 1 design  
Updated: October 24, 2026  
Deployment target: one owner-controlled home server, initially the existing Orbit WSL/Docker host

## Product goal

Orbit is a local-first personal assistant that accepts chat and voice requests, delegates work to specialist agents, remembers user-approved context across days, and runs scheduled tasks. Model inference, memory, orchestration, and operational data stay on the home server. Network adapters are isolated and disabled until configured.

The original brief names Chief of Staff, Finance, Home, Comms/Calls, and Research. These are five product divisions. The current Orbit installation has a local OpenClaw-based control console and four local-model agent profiles. Those are the current foundation, not completion of the target architecture. The target uses a LangGraph supervisor and explicit MCP tool boundaries.

## Design choices

| Area | Choice | Safety and privacy tradeoff |
|---|---|---|
| Orchestration | LangGraph supervisor with Postgres checkpoints | Durable retries and approval interrupts add local state that needs tested backups. |
| Inference | Ollama with pinned local model tags and no remote fallback | Local models may be less capable than hosted services; privacy takes priority. |
| Specialist tools | Separate MCP servers and per-agent allowlists | More services to operate, with narrower credentials and blast radius. |
| Records and memory | PostgreSQL with pgvector; embeddings produced by local Ollama | One database simplifies operations but concentrates backup responsibility. |
| Interfaces | Local web console, remotely reachable only on the owner's Tailscale network | No public service ports; remote use requires an authenticated tailnet device. |
| External traffic | Explicit adapters for approved web search, mail transport, and SIP/carrier calls; Telegram only if separately enabled | Each adapter sends only the minimum data required for its function. |
| Backups | Encrypted restic repository on independent external media | A second partition on the same physical disk is not an independent backup. |

## Component diagram

    Owner: local web chat or voice
             |
       Orbit Console -- Tailscale owner devices
             |
       LangGraph Supervisor <----> Postgres checkpoints and job queue
          |       |       |
          |       |       +---- Local Markdown and pgvector memory
          |       +------------ Policy, approvals, append-only audit
          +-------------------- Local model router ---- Ollama
                                                   |-- Qwen tool model
                                                   |-- small local router
                                                   |-- nomic-embed-text
                                                   |-- faster-whisper
                                                   +-- Piper TTS
             |
       Five specialists
       Chief of Staff | Finance | Home | Comms/Calls | Research
             |
       MCP tool broker with isolated server identities
       Calendar/tasks | Firefly III | Home Assistant | Asterisk
       Mail | approved web search
             |
       External boundary only where required:
       mail server | SIP/carrier | owner-approved public web sources

A global pause switch controls the scheduler, worker claims, policy gate, and MCP mutations. Read-only health and audit views remain available during a pause.

## Data flow

1. The owner submits a request through the local console or an enabled chat/voice adapter. The ingress layer records its source and treats its content as untrusted.
2. LangGraph creates a durable run and attaches only relevant, approved memory. A local router selects a specialist.
3. The specialist may use only its allowlisted MCP tools. Models cannot read credentials, call arbitrary endpoints, or access an unrestricted shell or filesystem.
4. Read-only work and local drafts can return directly. A consequential tool request is normalized, checked by server-side policy, and held at a durable approval interrupt.
5. The console displays the exact proposed action, destination/payee, amount and cap, arguments, expiry, and digest. Approval is bound to those exact fields; any change requires a new approval.
6. On approval, the executor revalidates the policy and digest, records an append-only audit event, invokes the narrow tool, and records its outcome. It never blindly retries an external action with uncertain completion.
7. Scheduled runs use the same graph and policy path. The scheduler cannot bypass approvals. The global pause stops new job claims and external calls.
8. Memory writes are local, attributed, and inspectable. Sensitive content is excluded by default.

## Approval gate and audit

Transfers, bill payments, outbound calls, and sent messages require a fresh action-specific approval unless the owner creates a narrowly scoped standing permission naming the action type, destination/payee, amount or frequency cap, and expiry. Broad permissions such as "handle my finances" are not accepted.

Each approval records the canonical action and arguments, destination, amount when relevant, policy version, creation and expiry times, requesting run, and SHA-256 digest. The approver is the owner authenticated on Tailscale. Decisions are single-use and rechecked immediately before execution. Rejection, expiry, cancellation, policy changes, and failures are audited.

The application role may append but not edit or delete audit records. Each event contains the previous event hash and its own hash; periodic signed exports go to the encrypted backup repository. Record actor/run IDs, model and prompt version, redacted arguments, approval identity and decision, outcome, and timestamps. Do not store credentials or unrelated personal message bodies in the audit trail.

The independent pause switch stops scheduler enqueueing, worker claims, MCP mutations, and all external calls/sends/payments. It does not stop read-only status or audit access and requires explicit owner action to resume.

## Specialist boundaries

| Specialist | Allowed work | Approval boundary |
|---|---|---|
| Chief of Staff | Calendar, reminders, tasks, email triage/drafts, morning briefings | Sending mail, inviting attendees, or changing calendar events requires action-specific approval. Email content is untrusted. |
| Finance | Firefly III recurring-bill records, local bank-statement imports, reconciliation, variance and due-date alerts | No bank-transfer tool is exposed. Any future payment integration requires exact approval and idempotency. |
| Home | Read sensors and control explicitly allowlisted Home Assistant entities | Locks, garage doors, alarms, presence actions, and safety-sensitive controls require explicit approval. |
| Comms/Calls | Local transcription, screening summaries, approved call drafts | Carrier/SIP calls require fresh exact approval. No impersonation, emergency calls, or hidden recording. |
| Research | Search and summarize public information after the owner approves the query | No private memory is sent with a query unless the owner approves that specific disclosure. Retrieved pages remain untrusted. |

Agent delegation passes a short task record, never another agent's credentials or unrelated private context. No agent gets shell access, unrestricted filesystem access, Docker socket access, or raw database access.

## Memory

Markdown files store owner-authored preferences, durable decisions, and dated diary notes in the private workspace. PostgreSQL stores metadata and local pgvector embeddings created by Ollama's nomic-embed-text. Search remains on-device and returns source/date labels. The supervisor attaches only relevant, authorized snippets. Voice transcripts are local and deleted after a configured retention period unless the owner asks to retain them. Email, bank statements, call audio, and smart-home history are not automatically copied into long-term memory.

## Threat model

| Threat | Defense | Verification |
|---|---|---|
| Prompt injection in pages, emails, transcripts, or files | Treat content as data; tool allowlists and server-side checks | Adversarial fixtures for every ingress |
| Unsafe or hallucinated tool calls | Typed MCP schemas, approval digest, per-tool authorization | Deny malformed args, wrong destination, changed amount, expired approval |
| Compromised agent or prompt | Separate MCP identities and limited tool sets | Cross-agent access tests |
| Stolen remote device | Tailscale-only access, device revocation, owner identity check | Revoke a test device and verify denial |
| Duplicate side effect after retry | Idempotency keys and durable intents; no blind retries | Simulate timeout after external submission |
| Host/disk loss | Encrypted independent restic backups and restore drills | Restore into an isolated target |
| Malicious dependency/update | Pinned dependencies and images, reviewable updates, rollback image | Safe update and rollback acceptance |
| Secret leakage | Secret files or Docker secrets, redaction, no model access to credentials | Canary scan of logs and rendered output |
| Host privilege escalation | Unprivileged services, constrained mounts, no host socket | Compose capability and mount audit |

## Exact target repository structure

    orbit/
      README.md
      LICENSE
      .env.example
      .gitignore
      compose/orbit-compose.yml
      config/policy.yaml
      config/agents.yaml
      config/model-routing.yaml
      orchestrator/
        Dockerfile
        pyproject.toml
        orbit_graph/graph.py
        orbit_graph/supervisor.py
        orbit_graph/state.py
        orbit_graph/policy.py
        orbit_graph/approvals.py
        orbit_graph/audit.py
        orbit_graph/scheduler.py
        orbit_graph/memory.py
        orbit_graph/settings.py
        tests/
      agents/
        chief_of_staff/{prompts,tools.py}
        finance/{prompts,tools.py,reconciliation.py}
        home/{prompts,tools.py}
        comms/{prompts,tools.py}
        research/{prompts,tools.py}
        market/                 existing paper-only simulator
        property/               existing assumption calculator
        smart-home/             existing entity validator
      mcp/
        calendar/ firefly/ home_assistant/ asterisk/ mail/ research/
      interfaces/
        console/                 existing Orbit Control UI
        chat/
        voice/
      memory/README.md
      task-api/                  existing local API and records
      monitoring/                existing Prometheus/Grafana config
      scripts/{backup,restore,health,release-check}/
      systemd/
      adapters/                  existing compatibility adapters
      docs/{architecture,threat-model,operations,backup-restore}.md
      tests/{integration,security}/

Secrets are injected at runtime from owner-managed ignored files. Example configuration contains safe sample values only. Compose must not mount the Docker socket into an agent, publish public ports, or mount Windows user folders by default.

## Delivery phases and acceptance

1. Architecture and design: this document and privacy boundary reviewed.
2. Secure scaffold: pinned dependencies, Compose, LangGraph supervisor, durable checkpoints, approval interrupt, append-only audit, global pause. Acceptance: clean local install, graph resume, digest mismatch denied, pause blocks scheduler claims and mutations.
3. Chief of Staff and Home: calendar/tasks/drafts and allowlisted Home Assistant MCP. Acceptance: injection tests pass and no send/control action runs before approval.
4. Finance: local Firefly III and bank statement import/reconciliation, due-date and amount-variance alerts. Acceptance: local fixture reconciliation succeeds and no transfer tool is exposed.
5. Comms and Calls: isolated Asterisk/SIP, local faster-whisper and Piper. Acceptance: test extension only, local audio retention policy verified, calls require exact approval.
6. Voice, memory, and hardening: local voice interface, Markdown plus pgvector memory, encrypted restic, safe rollback and release checklist. Acceptance: egress test, restore drill, cold boot, global pause, secret scan, and specialist safety tests pass.

The current Orbit installation has not passed these acceptance checks as a whole. LangGraph, Firefly III, Asterisk/SIP, faster-whisper, Piper, pgvector memory, and the five target MCP adapters are absent from the current source tree. Do not call the system production-complete until implementation and release checks pass.

## Current operating state and owner-controlled integrations

The current deployment is a local-first foundation: OpenClaw is the live agent runtime, Task API and PostgreSQL hold local control records, Ollama serves qwen3:8b, and Prometheus/Grafana monitor services. Four current agent profiles are pinned to the local model. The bill tracker is manual, the Raleigh calculator uses editable assumptions, and Home Assistant is planning-only because the service is absent. The approval queue is held and execution remains paused.

The owner selected Tailscale remote access and Telegram outage alerts. Tailscale access is configured; the owner must still pair and verify a phone. Telegram/Healthchecks requires the owner's private ping URL and explicit local configuration. Only the minimum heartbeat data may cross that integration. External backup media, cold-boot verification, rollback acceptance, and a full restore remain outstanding.
