# notes-api

A small HTTP API for managing a list of notes.

## What it does

- `GET /` — service info
- `GET /healthz` — health check, returns `ok`
- `GET /notes` — returns the list of notes as JSON
- `POST /notes` — adds a new note, body: `{"text": "..."}`
- `DELETE /notes/<index>` — removes a note by its index

## How to run

```bash
./scripts/run.sh
```

The server listens on `$PORT` (defaults to `8080` if not set).

```bash
PORT=9000 ./scripts/run.sh
```

## How to test

```bash
./scripts/test.sh
```

## Port

Default port: `8080`. Override with the `PORT` environment variable.
