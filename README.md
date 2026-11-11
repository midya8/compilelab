# CompileLab

**One function. Many shapes.** Exact finite ROBDD knowledge compilation,
variable-order atlases and existential-projection evidence.

[Interactive workbench](https://midya8.github.io/compilelab/) ·
[Exact contract](CONTRACT.md) · [Prior-work ledger](SOURCES.md) ·
[Reproduction evidence](EVIDENCE.md)

Two paired equalities have the same four models under every variable order,
but their ordinary reduced diagram uses six to nine nonterminals. CompileLab
shows all 24 orders,each selected graph's complete reduction decisions,per-node
suffix counts,exact gap-aware literal-weight masses,and every assignment path.
The five-variable multiplexer control spans seven to 13 nonterminals over 120 orders.
These are exact bounded graph counts,not timing or scalability benchmarks.

## Exists is not sum

For `x 0 OR x 1`,keepingx 0 gives two projected models but three full models.
With every literal weighted 1/2,full mass is 3/4 while retained-only projected mass
is 1. The two retained assignments have one and two hidden extensions. Inspect
all extensions,the lexicographically first full witness and both distinct masses.
A zero-weight satisfying extension still establishes logical existence.

## Reproduce

Python 3.10+;no runtime dependencies:

```sh
git clone https://github.com/midya8/compilelab.git
cd compilelab
python -m compilelab docs/example.json --output evidence.json
python -m compilelab evidence.json --verify
python -m unittest discover -s tests -v
python -m tools.check_assets
python -m tools.check_installed
```

Install with `python -m pip install .`,then use `compilelab` with the same flags.
`check_installed` builds a wheel in an isolated build environment (may download
build tooling),installs it in a temporary environment,and checks both entry
points outside the checkout. Node 22+ and local Chrome: `npm test`.
Serve `docs` with `python -m http.server --directory docs 8000`.

Optional reference,Python 3.11+ in a separate environment:

```sh
python -m pip install dd==0.6.0
python -m tools.check_reference
```

The actual BSD-licensed dd distribution uses complemented edges. Compare
functions,model sets and masses,not its raw node counts to our ordinary graph.
No reference source vendored. Classical ROBDD and projected-compilation work is
credited in [SOURCES.md](SOURCES.md);no new theory claim.

## What is checked

Separate native producer and truth-function checker share input parsing only.
The checker does not invoke the recursive builder or graph counting recurrence.
JavaScript is a separate implementation;browser replay itself is same-engine.
Exports become independently checked only after native replay succeeds.

Local 0.1 checks:15 Python tests,2048 exhaustive two-variable clause/keep settings,
180 seeded inputs,719 primitive noninput forgeries rejected per engine,and 102 complete
cross-language reports(90 nonterminals,1394 trace rows). Installed wheel:five module
origins,twelve controls,two entry points and 24 CLI forgery failures. Optional
actual dd 0.6.0 comparison:574 inputs,340 full models and 175 projected assignments,
including exact original/event/projected masses. See EVIDENCE for command scope.

Chrome checks 48 responsive control/width views,144 diagrams,924 assignment paths,
128 fiber selections,160 displayed extensions,all 120 orders of the five-variable
control,and 12 trusted completed exports independently verified by native Python.
Invalid edits clear stale results and disable export. Actual desktop,phone,
narrow-boundary graph and projection pixels inspected. Public CI/deployment
verification is separate from these local claims.

## Bounded and explicit

0..5 declared variables;≤10 CNFclauses,≤10 signed literals each;exact nonnegative
rational weights;n!≤120 orders. Evidence pins values;keep selects unpinned
variables. Declared-but-absent and skipped variables remain part of their
counting universe. Empty/no-model/no-variable/all-pinned/zero-weight cases
have explicit controls. Fixed-order canonicity only. Not a scalable compiler,
a formally verified proof system,a trained model,or a calibrated probability
estimate. No private data,no paid APIs,no network inference.
