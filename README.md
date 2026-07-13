# link-rep

Parse and serialize the textual link-representation format used by the TopLink pipeline.

## Installation

```bash
pip install linkrep
```

## Quick start

Create `link_rep.LinkRep()` and call `deserialize(text)` or `serialize()`.

PD codes are lists of four-entry crossings. Each arc label must occur exactly twice. Functions validate their inputs and do not mutate caller-owned PD-code lists unless explicitly documented.

## Development

Use Python 3.10 or newer for Python packages. Build distributions with `poetry build`. Run the package's tests or examples before publishing. C++ projects require a modern standards-compliant compiler.

## License

MIT. See `LICENSE`.
