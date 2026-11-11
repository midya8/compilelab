"""Optional independent dd0.6.0 comparison. No dd source is vendored.

Complemented-edge node counts intentionally NOT compared to ordinary ROBDDs.
All functions are built from input CNF, not from CompileLab diagrams.
"""
import importlib.metadata,itertools,json,random
from fractions import Fraction as F
from math import prod
from dd.autoref import BDD
from compilelab import analyze
from tools.make_cases import base,controls
assert importlib.metadata.version('dd')=='0.6.0'
r=random.Random(836);xs=[x for _,x in controls()]
clauses=[[],[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]]
for i in range(1<<len(clauses)):xs.append(base(2,[c for j,c in enumerate(clauses) if i>>j&1],keep=[0]))
for i in range(50):
 n=r.randrange(1,5);e=[r.choice((-1,-1,0,1)) for _ in range(n)]
 xs.append(base(n,[[r.choice((-1,1))*r.randrange(1,n+1) for _ in range(r.randrange(4))] for _ in range(r.randrange(6))],evidence=e,keep=[v for v in range(n) if e[v]==-1 and r.randrange(2)]))
assignments=projections=0
for x in xs:
 b=BDD();names=['x'+str(v) for v in range(x['n'])];b.declare(*[names[v] for v in x['order']]);u=b.true
 for clause in x['clauses']:
  c=b.false
  for l in clause:c=c | (b.var(names[abs(l)-1]) if l>0 else ~b.var(names[abs(l)-1]))
  u=u&c
 report=analyze(x);assert int(b.count(u,nvars=x['n']))==report['summary']['models']
 expected={r['bits'] for r in report['truth'] if r['satisfies']}
 got={''.join(str(int(a[name])) for name in names) for a in b.pick_iter(u,care_vars=set(names))};assert got==expected;assignments+=len(got)
 mass=lambda words,order:sum((prod((F(x['weights'][v][int(word[j])]) for j,v in enumerate(order)),start=F(1)) for word in words),start=F(0))
 assert str(mass(got,list(range(x['n']))))==report['summary']['mass']
 fixed={names[v]:bool(e) for v,e in enumerate(x['evidence']) if e!=-1};free=[v for v in x['order'] if x['evidence'][v]==-1];keep=[v for v in free if v in x['keep']]
 c=b.let(fixed,u);q=b.exist([names[v] for v in free if v not in keep],c)
 assert int(b.count(c,nvars=len(free)))==report['summary']['evidence_models'];assert int(b.count(q,nvars=len(keep)))==report['summary']['projected_models']
 got={''.join(str(int(a[names[v]])) for v in keep) for a in b.pick_iter(q,care_vars={names[v] for v in keep})};expected={row['bits'] for row in report['fibers'] if row['count']};assert got==expected;projections+=len(got)
 assert str(mass(got,keep))==report['summary']['projected_mass']
 got_ev={''.join(str(int(a[name])) for name in names) for a in b.pick_iter(u,care_vars=set(names)) if all(a[k]==v for k,v in fixed.items())}
 assert str(mass(got_ev,list(range(x['n']))))==report['summary']['evidence_mass']
 # Drop all Function references before discarding manager.
 del u,c,q
 if x['clauses']:del clause
 b.collect_garbage()
print(json.dumps({'reference':'dd0.6.0 autoref','inputs':len(xs),'models':assignments,'projected_assignments':projections,'raw_node_counts_compared':False}))
