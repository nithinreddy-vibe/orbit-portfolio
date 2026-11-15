> Historical design/deployment note. This portfolio does not include the full deployment, referenced services, or all scripts. These notes are not a current security certification or runnable setup guide.

# Orbit local AI orchestrator

Orbit's local console now lists four specialist OpenClaw agents and lets the user assign one-time or recurring tasks. Open `http://127.0.0.1:18082/console` and use the **Orbit AI agents** panel. The runner checks the local OpenClaw Gateway and Ollama before claiming work, then records each result in the local Orbit database.

Every specialist is pinned to `ollama/qwen3:8b`. Its model policy permits only that exact local model, the task runner requests the same model explicitly, and no cloud fallback or web-search tool is configured for these agents.

| Agent | Scope | Available tools |
|---|---|---|
| Orbit Monitor | Summarize the latest read-only PC health snapshot and execution pause | Read-only local health status |
| Orbit Bill Pay | Track manually entered payees, USD amounts, and due dates; prepare a checklist | Read and add local bill records |
| Orbit Real Estate | Compare buying and renting in Raleigh from supplied assumptions | Local Raleigh calculator; no live listings |
| Orbit Home Assistant | Plan routines and troubleshoot from user-provided details | No connected home devices or control tools |

Schedules support run-now, one-time at a selected local time, and hourly, daily, or weekly repeats. Recurring jobs can be paused, resumed, run immediately, or removed from the console. The local systemd runner is `orbit-agent-runner.service`; queued work waits until both OpenClaw and Ollama are reachable.

Bill records stay in the local database. Orbit does not connect to a bank, request payment credentials, initiate or schedule payments, contact billers, or mark bills paid through an agent. The user completes payments in their bank and may mark the record manually in the console.

Home Assistant Container 2026.10.3 is installed at http://127.0.0.1:18123 and uses a private Docker bridge with IP masquerading disabled. Its initial account onboarding is pending. No device/entity permissions are configured; Orbit Home Assistant remains planning-only and cannot read sensors or operate devices. Remote Tailscale access awaits owner account setup and the trusted-proxy setting in Home Assistant. See docs/home-assistant.md. The global approval outbox remains held and the general execution pause stays enabled; local AI tasks only invoke the specialist's explicitly listed local tool, if any.

Health snapshot status is based on `/srv/orbit/operations/health/health-*.log`; evidence older than eleven minutes is displayed as stale. Failed or missing evidence must be treated as unknown, not healthy.
