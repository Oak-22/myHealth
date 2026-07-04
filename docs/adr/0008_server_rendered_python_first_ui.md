# ADR 0008: Adopt A Python-First Server-Rendered UI Stack

## Status

Accepted

## Context

`myHealth` is primarily a backend, data, privacy, and inference
platform. The frontend should support user interaction without becoming
the center of the system or requiring a separate JavaScript/TypeScript
application skill set.

The project needs enough UI capability for:

- clinical and molecular analytics dashboards
- drill-down detail pages
- upload registration and ingestion status views
- provenance and audit views
- hardened LLM query forms
- operator/admin workflows

At the same time, the developer wants the implementation to remain
defensible in interviews as a Python/backend project. Custom
JavaScript/TypeScript, React, Next.js, and frontend state-management
frameworks are intentionally out of scope for now.

## Decision

Use a Python-first, server-rendered UI stack for the core application:

- **FastAPI** owns routes, authentication boundaries, orchestration, and
  state transitions.
- **Jinja2** renders server-side HTML templates.
- **HTML forms and links** are the default interaction model.
- **CSS** handles presentation.
- **HTMX** is allowed only as declarative progressive enhancement for
  server-owned partial page updates.
- **No authored custom JavaScript or TypeScript** should be introduced
  unless a future ADR documents the need.
- **No React, Next.js, Node.js frontend runtime, or SPA architecture**.

Streamlit remains allowed for internal experiments, analytical
prototypes, and research cockpit workflows. Streamlit is not the
durable patient/provider product shell.

## Consequences

### Positive

- keeps frontend behavior aligned with backend-owned privacy and audit
  boundaries
- avoids a separate JavaScript application layer and client-side state
  model
- supports useful dashboards, drill-down pages, forms, and LLM query
  workflows with Python-owned behavior
- gives HTMX a narrow role as progressive enhancement rather than
  application logic
- keeps Streamlit useful for fast experiments without making it the
  product UI foundation

### Negative

- less fluid than a rich SPA for highly interactive visual exploration
- some dashboard interactions may require full-page requests unless HTMX
  fragments are added
- advanced client-side charting, drag/drop, offline behavior, and
  complex browser state are intentionally deferred
- server-rendered views require careful template organization as the app
  grows

## Implementation Guidance

- Prefer classic routes such as `/dashboard`, `/dashboard/labs`,
  `/ingestions/{manifest_id}`, `/documents/{document_id}`, and
  `/ask`.
- Use query parameters and form posts for filters, drill-downs, and LLM
  questions before adding HTMX.
- Use HTMX only when a server-rendered fragment clearly improves
  workflow ergonomics, such as status refresh, table pagination,
  expandable provenance panels, or answer/result updates.
- Keep all privacy-sensitive state transitions in backend services.
- Render charts server-side with Python-generated images, SVG, tables,
  or static artifacts before introducing browser-side chart code.
- Do not add custom JavaScript files, TypeScript, React, Next.js, or npm
  tooling without a new ADR.

## Evidence

- [system_architecture.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/system_architecture.md)
- [technology_stack.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/architecture/technology_stack.md)
- [0005_fastapi_for_mvp_application_framework.md](/Users/julianbuccat/Projects/Dev/myHealth/docs/adr/0005_fastapi_for_mvp_application_framework.md)
