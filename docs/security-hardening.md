# Orbit security hardening - October 24, 2026

## Applied and verified

- Docker-published service ports remain bound to Windows/WSL loopback only. The corresponding Windows listeners are owned by wslrelay.exe and bound to 127.0.0.1 / ::1; inspected Orbit, Ollama, and OpenClaw ports are not LAN-bound.
- Tailscale Serve routes for Orbit, OpenClaw, Grafana, n8n, and Firefly are marked tailnet only. Home Assistant has no remote Serve route while its proxy onboarding is incomplete.
- Orbit Task API runs as UID/GID 65532, with the Orbit supplementary group, all Linux capabilities dropped, and no-new-privileges enabled. Workspace directories remain writable only by the Orbit group. The API Postgres password file is mode 0440, owned by root:orbit.
- Firefly trusted proxy is restricted to 172.26.0.1, verified as the source address in its container access logs.
- The agent job claim endpoint checks the global execution pause under a database row lock and returns no job while paused. The pause gate was tested. The four one-time sample tasks completed with the switch temporarily enabled, then it was restored to paused. A later separate monitor task is queued and remains paused.
- All eight Compose services were healthy after the changes. The task API /readyz reports the database and LangGraph orchestrator ready. A fresh post-change health snapshot passed.
- Local one-time sample tasks completed for Monitoring, Bill Pay, Real Estate, and Home Assistant using the local Qwen model. The monitoring agent was rerun after its first response cited stale context; its verified response uses the live snapshot.
- The Real Estate agent profile now covers supplied or explicitly approved market data, listing drafts, and relaunch plans. Live search and marketplace publishing are not connected; no listing is published.
- The seven-day health soak baseline was reset after these changes. Earliest possible seven-day review is October 31, 2026 at 13:29:03 EDT.
- A local backup completed and format-validated for Orbit and Firefly databases, configuration, n8n workflows, and Firefly uploads. Backup files are restricted to root. Backups are stored in the WSL distribution under D:, while C: and D: share the same physical NVMe, so they cannot protect against whole-drive loss.

## Remaining owner actions

- Finish first-owner account setup in Firefly and n8n. These setup screens are reachable only through private tailnet routes, but enrollment has not been completed.
- Finish Home Assistant onboarding and configure trusted proxy settings in its UI before adding a remote route. No devices or entities have been authorized yet.
- Add the external drive later and copy/verify a backup there. Current backups are local to this machine and cannot survive whole-drive loss.
- Review who is authorized in the Tailscale tailnet; tailnet membership is the remote access boundary for these services.
