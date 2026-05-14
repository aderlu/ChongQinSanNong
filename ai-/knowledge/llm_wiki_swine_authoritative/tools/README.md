# Swine Wiki Tools

This directory contains active tooling for the swine authoritative wiki and the wiki-first data pipeline.

## Functional groups

- `pipeline/`: wiki-first sample planning, generation, evaluation, arbitration, and export pipeline
- `wiki_ops/`: wiki maintenance, update, normalization, and runtime build tools
- `audit/`: readiness, governance, encoding, and runtime audit tools
- `graph/`: graph rendering and graph-specific helpers
- `archive/`: superseded tools kept only for traceability

## Compatibility

Some scripts may remain at the top level temporarily as compatibility entrypoints while the project is being cleaned up. New development should prefer the grouped directories.
