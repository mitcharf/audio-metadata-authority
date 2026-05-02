# Metadata Authority & Library Normalization System

This repository is a monorepo for a high-performance audio metadata authority and normalization engine. It includes:
- Async FastAPI backend (Python 3.14)
- React 18 + TypeScript + Vite frontend
- SQLite WAL database
- Batch scanning, safe write queue, authority/normalizer core, plugin & quarantine support

See DESIGN.md for architecture, requirements, and subsystem breakdown. The system is GPL-3.0 licensed.

## Directory Structure
See DESIGN.md for canonical directory and file layout. Below is the high-level structure.

```text
/backend   # FastAPI backend
/frontend  # React frontend
/docker    # Compose, ops
/config    # Environment and schemas
/scripts   # Development and DB scripts
```

## License
GPL-3.0; see LICENSE for details.
