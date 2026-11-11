# CompileLab 0.1 reproduction evidence

November 10,2026. Local measurements below are from executed checks,not promises
about public CI. Native public source,feature/PR/main jobs,Pages,deployed assets,
behavior and all showcases must be separately verified before final completion.

| Check | Executed result |
|---|---|
| `python -m unittest discover -s tests -v` |15 tests;2048 exhaustive two-variable clause/keep configurations;180 seeded inputs;719 noninput primitive forgeries rejected |
| `python -m tools.check_assets` |12 controls and default example equal source |
| `python -m tools.check_installed` |Built wheel,five site-packages module origins,12 controls ×2 entry points;24 forged CLI reports fail;outside checkout |
| `node --test tests/test_engine.cjs` |102 complete native/JS reports,90 nonterminals,1394 trace rows;719 primitive forgeries rejected by browser replay |
| `python -m tools.check_reference` under Python 3.11 with dd 0.6.0 |574 input-built CNFs,340 full models,175 projected assignments;complete original/projected model sets;original/conditioned/projected counts and exact original/event/projected masses;no raw node-size comparison |
| `npm test` with actual Chrome |4 tests;48 control/width reports at 1440/768/390/320;144 graphs,924 complete assignment paths,128 fibers,160 extensions;all 120 boundary orders;12 trusted completed downloads native-verified |

Default paired-equality function has 4 models,mass 1/4,ordinary nonterminal sizes 6..9
across 24 orders. Boundary multiplexer has 16 models,mass 1/2,sizes 7..13 across 120 orders.
Projection control `x 0 OR x 1` yields 3 full models,mass 3/4,2 retained models,projected
mass 1. Zero-weight control retains 3 Boolean models and 2 projected models despite
zero full weighted mass. These are synthetic deterministic controls.

The 2048 exhaustive configurations are 512 subsets of nine non-tautological clauses
(including the empty clause),each crossed with four keep subsets. They are not
all syntactically possible CNFs. Seeded 180 inputs use at most 4 variables;developed
controls cover the 5 variable boundary. Cross-language 102 inputs are 12 controls plus
90 seeded inputs;most random CNFs are constant,so 90 nonterminals is not a large
structural benchmark. No causal,learning,latency,scalability or real-agent claim.

64 unmasked local screenshots captured across four controls,widths and sections.
Desktop hero,phone projection and 320 px boundary diagram actual pixels inspected.
Horizontal graph/table scrolling is intentional inside labelled bounded regions;
page-level overflow rejected. A graph can have both terminal display nodes even
when a terminal is unreachable;nonterminal size excludes both terminals.

Native checker independence is architectural separation plus tests,not formal
verification. It imports shared input validation. Same-engine browser replay is
not counted as an independent checker. Optional dd models come from its own
input-built formulas. License metadata says BSD;dd 0.6.0 needs Python>=3.11.
