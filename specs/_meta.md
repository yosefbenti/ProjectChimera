# Project Chimera — Master Specification (Meta)

Vision
-------
Project Chimera is an autonomous content-generation and publishing platform composed of orchestrated AI agents (Planner, Worker, Judge) that produce, validate, and publish multimedia content at scale while preserving human oversight for safety-sensitive decisions.

Primary constraints
- Fast time-to-insight for stakeholders (low-latency reporting)
- Auditability and tamper-evidence for billing and compliance
- Operate within limited engineering staffing (favor time-boxed, incremental work)
- Integrate with external agent networks (OpenClaw / Agent Social Network) without exposing sensitive credentials

Success criteria
- Reconciled financial and delivery data within a defined window (e.g., rolling 30 days)
- Automated gating for low-risk content and human review for medium/high-risk items
- Clear API contracts for interoperable agents

Operational assumptions
- Data sources are imperfect and require ingestion normalization
- Business rules (what is billable/publishable) will be defined by SMEs and codified in the Judge Agent

Deliverables of this spec set
- Functional user stories (`specs/functional.md`)
- Technical API contracts and DB schema (`specs/technical.md`)
- Integration notes for OpenClaw (`specs/openclaw_integration.md`)
