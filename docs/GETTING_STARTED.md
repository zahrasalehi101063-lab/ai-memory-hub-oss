# Getting Started

AI Memory Hub OSS is an early-stage, MIT-licensed,
local-first Python memory library using SQLite.

## Installation

Clone the repository:

```bash
git clone https://github.com/zahrasalehi101063-lab/ai-memory-hub-oss.git
cd ai-memory-hub-oss
python -m pip install -e .
```

## Testing

```bash
python -m pip install pytest
python -m pytest -q
```

## Current capabilities

- Local SQLite memory storage
- Project-scoped memory management and search
- Memory deletion
- JSON export and import
- Automated Python tests

## Important notes

This is an early-stage library, not yet a hosted
cross-account AI memory service.

Review the repository source and tests for the
current Python API before integrating it.

Keep private memory databases and sensitive exports
out of public repositories.

## Support

Use GitHub Issues for reproducible bugs and feature
requests. Never include credentials or private data.
