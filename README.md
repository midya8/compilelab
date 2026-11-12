# CompileLab

Build a small ordinary reduced ordered binary decision diagram and inspect
how its shape changes with variable order. CompileLab retains the complete
reduction decisions, assignment paths, model counts and rational masses.
Existential projection has a separate counting universe and extension ledger.

[Interactive workbench](https://midya8.github.io/compilelab/) ·
[Exact contract](CONTRACT.md) · [Prior-work ledger](SOURCES.md) ·
[Reproduction evidence](EVIDENCE.md)

Two paired equalities have the same four models under every variable order,
but their ordinary reduced diagram uses six to nine nonterminals. CompileLab
shows all 24 orders, each selected graph's complete reduction decisions, per-node
suffix counts, exact gap-aware literal-weight masses, and every assignment path.
The five-variable multiplexer control spans seven to 13 nonterminals over 120 orders.
These are exact bounded graph counts, not timing or scalability benchmarks.

## Existence and summed mass answer different questions

For `x0 OR x1`, keeping `x0` gives two projected models but three full models.
With every literal weighted 1/2, full mass is 3/4 while retained-only projected mass
is 1. The two retained assignments have one and two hidden extensions. Inspect
all extensions, the lexicographically first full witness and both distinct masses.
A zero-weight satisfying extension still establishes logical existence.

## Where to start

- Compare graph sizes in the variable-order atlas. Select an order, then follow
  an assignment through the original, conditioned and projected diagrams.
- Use the projection view to see why a retained assignment can have several
  hidden extensions. Its marginal mass and retained-only mass need not match.
- Read [CONTRACT.md](CONTRACT.md) for the exact input rules and report fields,
  or [EVIDENCE.md](EVIDENCE.md) for the exhaustive checks and historical run counts.

## Reproduce

Python 3.10+; no runtime dependencies:

```sh
git clone https://github.com/midya8/compilelab.git
cd compilelab
python -m venv .venv
. .venv/bin/activate
python -m pip install .
python -m compilelab docs/example.json --output evidence.json
python -m compilelab evidence.json --verify
python -m unittest discover -s tests -v
python -m tools.check_assets
python -m tools.check_installed
```

Install with `python -m pip install .`, then use `compilelab` with the same flags.
`check_installed` builds a wheel in an isolated build environment (may download
build tooling), installs it in a temporary environment, and checks both entry
points outside the checkout. Node 22+ and local Chrome: `npm test`.
Serve `docs` with `python -m http.server --directory docs 8000`.

Optional reference, Python 3.11+ in a separate environment:

```sh
python -m pip install dd==0.6.0
python -m tools.check_reference
```

The actual BSD-licensed dd distribution uses complemented edges. Compare
functions, model sets and masses, not its raw node counts to our ordinary graph.
No reference source vendored. Classical ROBDD and projected-compilation work is
credited in [SOURCES.md](SOURCES.md); no new theory claim.

## What is checked

Separate native producer and truth-function checker share input parsing only.
The checker does not invoke the recursive builder or graph counting recurrence.
JavaScript is a separate implementation; browser replay itself is same-engine.
Exports become independently checked only after native replay succeeds.

The Python tests compare exhaustive and seeded inputs with truth-function
results, reject altered reports, and compare complete reports across Python
and JavaScript. The installed check verifies module origins and runs all twelve
controls through both CLI entry points outside the checkout, including altered
reports that must fail verification.

The four Node tests include actual Chrome interaction. They compare displayed
graphs, assignment paths, projection extensions and the order atlas with native
reports at four widths. All 120 orders of the five-variable control are selected.
Completed browser exports are replayed through native Python; invalid edits must
clear stale results and disable export. See [EVIDENCE.md](EVIDENCE.md) for the
individual counts and the separate optional dd comparison. Those counts describe
bounded fixtures, not performance or an independent proof of the implementation.

## Bounded and explicit

Zero to five declared variables, at most ten CNF clauses and ten signed literals
per clause, exact nonnegative rational weights, and at most 120 variable orders.
Evidence pins values; `keep` selects unpinned
variables. Declared-but-absent and skipped variables remain part of their
counting universe. Empty/no-model/no-variable/all-pinned/zero-weight cases
have explicit controls. Fixed-order canonicity only. Not a scalable compiler,
a formally verified proof system, a trained model, or a calibrated probability
estimate. No private data, no paid APIs, no network inference.
