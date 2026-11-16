# AI Memory Hub OSS

A **local-first, open-source memory toolkit** for organizing project decisions and notes across AI-assisted workflows. This repository is an independent starter implementation, not a release of any private or commercial codebase.

## Features (v0.1)
- Project-scoped memories stored locally in SQLite
- Add, search, and delete records
- Source labels and creation timestamps
- No cloud account, API key, or external dependencies required at runtime

## Quick start

```bash
python -m pip install -e .
python -c "from ai_memory_hub import MemoryStore; m=MemoryStore('memory.db'); m.add('demo','First project decision'); print(m.search('decision', project='demo'))"
```

## Run tests

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Roadmap
- Export/import JSON with provenance
- Better multilingual full-text search
- Optional local UI and consent-based integrations
- Encryption and retention controls before storing sensitive data

## Security and privacy
All data remains in the local SQLite file. **Do not commit database files, private conversations, credentials, or API tokens.** This starter has no encryption or multi-user access control; do not deploy it as a public service.

## Contributing
Issues and pull requests are welcome. Please add tests for changes and avoid sharing personal data in examples.

## License
MIT. See LICENSE.
