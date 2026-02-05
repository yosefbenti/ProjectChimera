# OpenClaw Integration (Agent Social Network)

Overview
--------
OpenClaw is an agent-discovery and social protocol layer allowing agents to advertise availability, subscribe to topics, and request services from other agents.

How Chimera publishes availability
- Chimera exposes a lightweight `/.well-known/chimera-status` HTTP endpoint signed by the Orchestrator token. The endpoint returns a JSON object with service name, capabilities, and public metadata.

Example availability payload
```json
{
  "service": "chimera-content-generator",
  "capabilities": ["generate:short_video","analyze:trends"],
  "endpoint": "https://chimera.example.org/agents/worker",
  "version": "0.1.0",
  "ttl_seconds": 300
}
```

Social Protocols required
------------------------
1. Capability Advertising — agents must declare their capabilities and supported media types.
2. Negotiation Protocol — a small request/offer handshake (task proposal → bid → accept) to distribute work across networks.
3. Provenance Header — every inter-agent message should carry provenance metadata (origin_agent, signature, timestamp) to enable trust and auditing.
4. Rate & Quota Discovery — expose current load indicator to avoid overload.

Security & Privacy
- Sign availability payloads with the Orchestrator’s private key; OpenClaw participants validate via published public key.
- Do not expose business-sensitive identifiers (e.g., customer PII) in public adverts; use capability tokens for access control.

Integration flow (high-level)
1. Chimera registers to OpenClaw directory and begins periodic heartbeat publishing availability.
2. External agent requests a capability; Chimera returns an authentication challenge.
3. If challenge accepted, a scoped token is minted and the requesting agent can submit tasks.

Notes
- OpenClaw integration is optional for initial phase; enable once internal chimera flows are stable and security policies agreed.
