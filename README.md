# link-rep

Parse, validate, and serialize TopLink composite-link representation documents.

## Installation

```bash
pip install link-rep
```

## Usage example

```python
from link_rep import LinkRep

text = """K3a1: [[1,5,2,4],[3,1,4,6],[5,3,6,2]]
[K3a1, K3a1]
L[1, 1]#L[2, 1]
"""
rep = LinkRep()
rep.deserialize(text)
print(rep.serialize())
print(rep.json_serialize())
```

## Algorithm

The parser separates four grammatical objects: comments, named PD-code definitions, the ordered factor set, and component-join terms. Each object has matching text and JSON serializers. Link identifiers are decomposed into mirror, knot/link, crossing, alternating, and table-index fields, which gives the rest of the toolchain a structured representation instead of ad-hoc string handling. Reused parser objects reset all identifier state, definitions must be unique and contain structurally valid PD codes, and factor/component references use positive one-based indices.

## Input conventions

A PD code is represented as a list of four-entry crossings. Arc labels normally occur exactly twice. Public functions validate inputs and return new values rather than mutating caller-owned data unless their API explicitly says otherwise.

## External software

No external software is required.

## Development

Python 3.10 or newer is required. Run the parser and round-trip tests with:

```bash
python -m unittest discover -s tests -v
```

No PyPI publication is performed as part of repository maintenance.

## License

MIT. See `LICENSE`.
