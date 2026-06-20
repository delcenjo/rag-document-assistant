# Nimbus Notes — Developer API

Nimbus Notes exposes a REST API for automating notes and notebooks.

## Authentication

All requests are sent to `https://api.nimbusnotes.com/v1` and authenticated with
an API key passed as a Bearer token in the `Authorization` header. API keys are
created in Settings under Developer.

## Endpoints

- `/notes` — create, read, update and delete notes.
- `/notebooks` — manage notebooks.
- `/search` — full-text search across the workspace.

Responses are JSON and lists use cursor-based pagination.

## Rate limits

- Free plan: 60 requests per minute.
- Pro and Team plans: 600 requests per minute.

## Webhooks and SDKs

Webhooks can notify your server of events such as `note.created` and
`note.updated`. Official SDKs are available for Python and JavaScript.
