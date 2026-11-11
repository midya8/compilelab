# CompileLab 0.1 exact contract

## Input and counting spaces

Strict six-key JSON object: `n`, `clauses`, `order`, `weights`, `evidence`, `keep`.
`n` is an integer 0..5. CNF has at most 10 clauses,each at most 10 signed 1-based
integer literals. Zero invalid;duplicates and tautologies permitted. Empty clause
is false. Empty conjunction true. `order` permutes indices 0..n-1. Literal weights
are pairs `[false,true]` of canonical nonnegative rational strings. Numerator and
denominator at most 1000,strings at most 10 characters. No floats,booleans as
integers,missing/extra keys,negative weights or noncanonical fractions.

Evidence has n entries:-1 means free,0/1 pins a value. `keep` is a unique subset
of unpinned variable indices. Its input order does not define the projected
universe order: that follows the selected original order restricted to kept
variables. Every truth row and full witness uses x 0..x(n-1),regardless of diagram
order. A zero-variable assignment is the empty string,not no assignment.

The original function uses every declared variable,including absent variables.
Conditioning substitutes pinned values and counts the remaining free universe.
The evidence-event weighted mass additionally multiplies pinned literal weights.
Projection existentially hides free variables outside keep. Each retained
assignment is a model iff at least one full satisfying,evidence-compatible
extension exists. Projected mass uses retained literal weights once. Fiber
completion mass sums full products,including pinned and hidden literals.

Example:`x 0 OR x 1`,keepx 0,all literal weights 1/2. Three full models have total
mass 3/4. Two retained assignments have projected mass 1. Their extension counts
are 1 and 2,completion masses 1/4 and 1/2. These are different universes,not
contradictory probability estimates. Zero-weight models still count logically.
Weights need not be normalized. Probability interpretation requires normalized
independent per-variable literal-weight pairs;no such independence is learned.

## Graph and trace

Ordinary noncomplemented ROBDD with terminals 0/1. Terminal IDs remain available
for display even if unreachable;size counts only reachable nonterminals.
Variables increase along paths in the declared order. Equal children remove a
test;equal `(variable,low,high)` triples merge. Low-first postorder IDs are
presentation labels. Canonical means unique up to isomorphism for a fixed
variable order,not across different orders. Original,conditioned and projected
graphs have separate ID spaces. Trace covers all 2^(k+1)-1 full-tree prefixes,
including constant residuals;terminal trace entries occur only at full depth.

Per-node count/mass covers its suffix universe from that node's variable level.
Each edge includes its branch literal and every gap variable before the child.
Every skipped variable multiplies count by 2 and mass by(w_false+w_true).
Root total additionally includes variables skipped before the root. Terminal
base count/mass are 0/0 and 1/1 over the empty suffix universe.

Atlas enumerates n! original-variable orders,including the one empty order.
All minima/maxima and all tied orders are returned. Node sizes are not runtime
or memory measurements;no heuristic/scalability conclusion follows.

## Independence and limits

Producer uses Shannon recursion,unique triples and graph-DP counts. Separate
native checker imports shared strict validation only. It builds residual
truth-vector classes from a bitmask CNF census and independently enumerates all
suffix assignments for node/edge weights. It checks all primitive fields,
canonical labels,full reductions,atlas ties,fibers,witnesses and exact rational
results. Canonical JSON comparison preserves boolean/integer distinctions.
The checker is independent code,not a formally verified soundness theorem.

JavaScript uses a separate row-partition graph builder and BigInt rational
arithmetic. Browser replay reconstructs with that same engine;it is not an
independent check. Download and native verification are separate steps.
The optional actual dd 0.6.0 reference builds functions directly from CNF,and
checks complete original/projected model sets,counts,conditioning and weighted
masses by enumerating dd's models. It uses complemented edges,so raw graph node
counts are intentionally not compared. Its Python>=3.11 requirement does not
change core Python>=3.10 support.

This is a bounded exhaustive educational implementation of classical theory,
not a new BDD algorithm,a general projected compiler,a formal proof system,
a trained model,a calibrated estimate or an agent-reliability benchmark.
No private data,paid API or model calls. All controls synthetic.
