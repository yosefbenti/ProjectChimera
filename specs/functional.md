# Functional Specification — Project Chimera

User stories

1. As a Planner Agent, I need to fetch trending topics from social platforms so that Worker Agents can produce timely content.

2. As a Worker Agent, I need to request context (tone, brand rules, campaign tags) from the Planner so I can generate content that matches brand policy.

3. As a Worker Agent, I need to upload generated assets (meta + object path) to object storage so the Judge Agent and analytics can access them.

4. As a Judge Agent, I need to validate generated content against safety and brand rules and return one of: APPROVE, QUEUE_FOR_REVIEW, REJECT.

5. As a Human SME, I need to review queued items and provide a final decision so the system can publish or discard the content.

6. As a Billing/Finance system, I need reconciled delivery and payment events with clear audit trails so we can invoice accurately.

7. As an Integrator, I need agents to publish availability/status into the OpenClaw network so downstream systems can discover Chimera services.

Acceptance criteria
- Each user story must have a minimal happy-path example (API call + expected response).
- For data-sensitive flows (payments, refunds), a reconciliation workflow must produce exportable CSVs and a 1-page findings report.

Workflows (high-level)
- Content creation: Planner → Worker(s) → Judge → (Human if needed) → Publish
- Reconciliation: Ingest payments + delivery events → reconcile by `order_id` → classify mismatches → report
