# Metadata Authority & Library Normalization System
## Comprehensive Architecture Specification (Monorepo, Updated)

---

# 0. CONTRACT SECTION (GLOBAL REQUIREMENTS)

## 0.1 MUST Requirements
- Backend implemented using **FastAPI** with **async** endpoints.
- Backend located under `/backend/app`.
- Frontend implemented using **React 18 + TypeScript + Vite** under `/frontend`.
- System supports **250,000+ files**.
- Python version MUST be **Python 3.14**.
- Docker base image MUST be **python:3.14-slim** for the backend.
- Mutagen version MUST be pinned to a version compatible with Python 3.14.
- FastAPI and Pydantic versions MUST be pinned for Python 3.14 compatibility.
- Scanner uses **two‑phase scanning** (light FS scan → deep scan for changed files).
- SQLite MUST run in **WAL mode**.
- Write queue MUST **serialize all writes**.
- Write queue MUST run as a **background task** started at application startup.
- Scanner MUST run as a **background task** and MUST NOT block startup.
- All authority edits MUST support **dry‑run mode**.
- External modifications MUST be detected via **partial hashing**.
- A bad‑file **quarantine subsystem** MUST exist.
- Automatic **OpenAPI schema** generation MUST be enabled.
- System MUST NOT load the entire library into memory.
- All large lists MUST use **server‑side pagination**.
- Frontend MUST use **virtualized lists** for large tables.
- All tag writes MUST enforce **ID3v2.3**.
- Original backups MUST be preserved before modification (one‑time backup per file).
- Plugin system MUST support sandboxing and timeouts.
- Blocking I/O (Mutagen, filesystem) MUST be executed via **asyncio.to_thread()**.
- Concurrency MUST use **asyncio.TaskGroup** where appropriate.
- A persistent **write‑queue journal** MUST be maintained.
- No deprecated typing constructs (e.g., `typing.List`) may be used.
- Modern Python 3.14 typing (`list[str]`, `dict[str, Any]`) MUST be used.
- All backend functionality MUST be accessible via HTTP endpoints (no frontend‑only logic).
- The backend MUST expose a stable, documented, versioned HTTP API suitable for:
  - custom API clients
  - automation scripts
  - CLI tools
  - external integrations
  - batch processing.

## 0.2 SHOULD Requirements
- Minimize memory usage.
- Avoid long DB write transactions.
- Compress rotated logs.
- Detect bulk modifications and throttle rescans.
- Provide clear UI feedback for long operations.
- Use Python 3.14 performance improvements where beneficial.
- Use efficient indexes and queries for large tables.

## 0.3 MUST NOT Requirements
- No UI blocking during scanning or writing.
- No assumption of multiple concurrent users.
- No full deep scan at startup.
- No file rewrites outside the write queue.
- Plugins must not block the scanner.
- No global state except caches.
- No event‑loop blocking operations.
- No WebSocket‑only functionality (all core operations must be available via HTTP).

---

# 1. SYSTEM OVERVIEW

This system is a **metadata authority and normalization engine** for large audio libraries (250k+ files). It provides:

- A **FastAPI** backend (Python 3.14, async, SQLite WAL).
- A **React 18 + TypeScript + Vite** frontend.
- A high‑performance **scanner**.
- A canonical **metadata authority**.
- A **conflict‑resolution engine**.
- A safe, serialized **write queue**.
- A **plugin system** for custom rules.
- A **quarantine subsystem** for bad files.
- **Dry‑run** and **rollback** capabilities.
- A stable, documented **HTTP API** suitable for custom clients.

The system is designed for **one human user**, but concurrency‑safe.

---

# 2. MONOREPO ARCHITECTURE OVERVIEW

## 2.1 Top‑Level Directory Layout

```text
/ (repo root)
  /backend
    /app
      main.py
      config.py
      logging.py
      /api
      /scanner
      /tokenizer
      /normalization
      /authority
      /conflicts
      /write_queue
      /encoding
      /quarantine
      /plugins
      /db
      /models
      /utils
    pyproject.toml
    Dockerfile
  /frontend
    index.html
    vite.config.ts
    tsconfig.json
    package.json
    /src
      main.tsx
      App.tsx
      /components
      /pages
      /api
      /hooks
      /state
      /utils
      /styles
    Dockerfile
  /docker
    docker-compose.yml
  /config
    app.example.env
    app.env.schema.md
  /scripts
    dev.sh
    migrate.sh
    seed.sh
  DESIGN.md
```

## 2.2 High‑Level Components

- Scanner  
- Tokenizer  
- Normalization Engine  
- Authority Engine  
- Conflict Engine  
- Write Queue  
- External Modification Detector  
- Quarantine System  
- Plugin System  
- API Layer  
- Frontend  
- Database  
- Logging System  

## 2.3 Data Flow

```text
Filesystem → Scanner → Tokenizer → Normalizer → Authority → Conflict Engine
→ Write Queue → Safe Write → Filesystem
```

Frontend and external clients interact only via the HTTP API:

```text
Frontend / Custom Client → HTTP API (FastAPI) → Backend Subsystems → DB / Filesystem
```

---

# 3. BACKEND ARCHITECTURE

## 3.1 Framework & Runtime

- FastAPI  
- Python 3.14  
- Uvicorn  
- Pydantic  
- SQLite WAL  
- asyncio.TaskGroup  
- asyncio.to_thread for blocking I/O  

## 3.2 Backend Directory Layout

```text
/backend/app
  main.py
  config.py
  logging.py
  /api
  /scanner
  /tokenizer
  /normalization
  /authority
  /conflicts
  /write_queue
  /encoding
  /quarantine
  /plugins
  /db
  /models
  /utils
```

---

# 4. SCANNER SUBSYSTEM

## MUST
- Two‑phase scanning  
- Detect new/deleted/modified/unchanged files  
- Partial hashing (head, tail, size, mtime)  
- Memory‑mapped reads  
- Thread pool or asyncio.to_thread for hashing  
- Skip tag parsing for unchanged files  
- Run as background task  
- Must not block startup  

## SHOULD
- Batch DB writes  
- Avoid long transactions  

---

# 5. TOKENIZER SUBSYSTEM

## MUST
- Split creators on: feat., featuring, with, and, &  
- Normalize whitespace  
- Detect suspicious patterns  
- Expose plugin hooks  

## SHOULD
- Allow plugin overrides  

---

# 6. NORMALIZATION SUBSYSTEM

## MUST
- Canonical casing  
- Normalize punctuation  
- Normalize whitespace  
- Apply authority mappings  
- Deterministic and idempotent  

## SHOULD
- Plugin‑defined rules  

---

# 7. AUTHORITY SUBSYSTEM

## MUST
- Store canonical creators/albums/genres  
- Apply cascades  
- Support dry‑run  
- Support rollback  
- Detect conflicts  

## SHOULD
- Bulk edits  
- History/audit  

---

# 8. CONFLICT ENGINE

## MUST
- Detect mismatches  
- Classify conflicts  
- Expose conflict details via API  

## SHOULD
- Provide previews  
- Support bulk resolution  

---

# 9. WRITE QUEUE

## MUST
- Serialize writes  
- Persistent queue + journal  
- Prioritization  
- Backpressure  
- Safe‑write semantics  
- Enforce ID3v2.3  
- Background task  
- Mutagen via asyncio.to_thread  

## SHOULD
- Warn when queue grows large  
- Expose metrics  

---

# 10. EXTERNAL MODIFICATION DETECTION

## MUST
- Partial hashing  
- Detect mtime/size/hash changes  
- Trigger deep rescan only when needed  

---

# 11. BAD‑FILE QUARANTINE

## MUST
- Isolate unreadable/corrupt files  
- Store reason + timestamps  
- Allow rescan, mark non‑audio, open location, delete  

---

# 12. PLUGIN SYSTEM

## MUST
- Sandbox execution  
- Enforce timeouts  
- Isolate heavy plugins  
- Hook points for tokenizer, normalization, suspicious detection, scanner  

---

# 13. DATABASE DESIGN

## MUST
- SQLite WAL  
- Tables for files, creators, albums, genres, authority, conflicts, write_queue, quarantine, plugins  
- Indexes on path, hash, last scanned, conflict status, creator_id, sort_key  
- Batched writes  
- Use Python 3.14 sqlite improvements  

---

# 14. LOGGING SYSTEM

## MUST
- Rotating logs  
- Compressed archives  
- Separate scanner/write‑queue/API logs  

---

# 15. FRONTEND ARCHITECTURE (REACT + TYPESCRIPT + VITE)

## Stack
- React 18  
- TypeScript (strict)  
- Vite  
- React Query (S3)  
- Local component state for UI state  
- No global state library  

## Directory Layout

```text
/frontend/src
  main.tsx
  App.tsx
  /components
  /pages
  /api
  /hooks
  /state
  /utils
  /styles
```

## MUST
- React Query for all server state  
- Virtualized lists  
- Server‑side pagination  
- Debounced filters  
- Explicit loading/error states  
- TypeScript strict mode  
- API calls centralized in /api  
- No fetching entire datasets  
- No UI blocking  

## SHOULD
- Consistent table component  
- Error boundaries  
- Progress indicators  

---

# 16. API DESIGN & EXTERNAL CLIENTS

## MUST
- Endpoints for scanner, write queue, conflicts, authority, quarantine, plugins  
- Complete OpenAPI schema  
- Pydantic models  
- Stable URL patterns  
- All functionality accessible via HTTP  
- OpenAPI at `/openapi.json`  

## SHOULD
- API versioning  
- Consistent error responses  

---

# 17. DEPLOYMENT MODEL

## MUST
- Backend: Uvicorn + python:3.14-slim  
- Frontend: Vite build → static assets  
- docker-compose for combined deployment  

---

# 18. CODING CONVENTIONS FOR COPILOT

## Backend
- async/await  
- Modern Python typing  
- Pydantic models  
- Strict module boundaries  
- Dependency injection  
- No global mutable state  
- asyncio.to_thread for blocking I/O  
- asyncio.TaskGroup for concurrency  

## Frontend
- TypeScript strict  
- React Query  
- Functional components + hooks  
- No unnecessary global state  
- Virtualized lists  
- Explicit loading/error states  

---

# 19. SUMMARY

This document defines the **complete monorepo architecture**, **backend and frontend structure**, **environment**, **API contracts**, and **behavioral constraints** for the Metadata Authority System.

GitHub Copilot MUST treat this document as the **single source of truth** for all code generation across:

- `/backend`
- `/frontend`
- external API clients.
