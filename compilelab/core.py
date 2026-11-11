"""Generator: Shannon recursion, unique table, graph dynamic programming."""
from fractions import Fraction as F
from itertools import product, permutations
from math import prod
from .input import validate

def assignments(vs):
    return [dict(zip(vs,b)) for b in product((0,1),repeat=len(vs))]

def diagram(order, predicate, weights):
    nodes=[]; unique={}; trace=[]
    def build(i,a,prefix):
        if i==len(order):
            value=int(predicate(a)); trace.append({'prefix':prefix,'node':value,'action':'terminal'})
            return value
        v=order[i]; lo=build(i+1,{**a,v:0},prefix+'0'); hi=build(i+1,{**a,v:1},prefix+'1')
        key=(v,lo,hi)
        if lo==hi: node=lo; action='skip'
        elif key in unique: node=unique[key]; action='merge'
        else:
            node=len(nodes)+2;unique[key]=node;nodes.append({'id':node,'variable':v,'low':lo,'high':hi});action='new'
        trace.append({'prefix':prefix,'node':node,'action':action})
        return node
    root=build(0,{},'');level={v:i for i,v in enumerate(order)}
    count={0:0,1:1};mass={0:F(0),1:F(1)};by={r['id']:r for r in nodes}
    def lev(k):return level[by[k]['variable']] if k>=2 else len(order)
    for r in nodes:
        i=level[r['variable']];cs=[];ms=[]
        for b,k in enumerate((r['low'],r['high'])):
            gap=order[i+1:lev(k)]
            cs.append(2**len(gap)*count[k]);ms.append(weights[r['variable']][b]*prod((sum(weights[v]) for v in gap),start=F(1))*mass[k])
        count[r['id']]=sum(cs);mass[r['id']]=sum(ms)
        r.update(count=count[r['id']],mass=str(mass[r['id']]),edge_counts=cs,edge_masses=list(map(str,ms)))
    gap=order[:lev(root)]
    return {'order':order,'root':root,'nodes':nodes,'trace':trace,'count':2**len(gap)*count[root],'mass':str(prod((sum(weights[v]) for v in gap),start=F(1))*mass[root])}

def analyze(raw):
    x=validate(raw);n=x['n'];vs=list(range(n));w=[[F(s) for s in p] for p in x['weights']]
    def sat(a):return all(any(a[abs(l)-1]==int(l>0) for l in c) for c in x['clauses'])
    fixed={v:b for v,b in enumerate(x['evidence']) if b!=-1};free=[v for v in x['order'] if v not in fixed];keep=[v for v in free if v in x['keep']];hidden=[v for v in free if v not in keep]
    evmass=prod((w[v][b] for v,b in fixed.items()),start=F(1))
    truth=[]
    for a in assignments(vs):
        truth.append({'bits':''.join(str(a[v]) for v in vs),'satisfies':sat(a),'matches_evidence':all(a[v]==b for v,b in fixed.items()),'weight':str(prod((w[v][a[v]] for v in vs),start=F(1)))})
    fibers=[]
    for a in assignments(keep):
        models=[{**fixed,**a,**b} for b in assignments(hidden) if sat({**fixed,**a,**b})]
        words=sorted(''.join(str(m[v]) for v in vs) for m in models)
        retained=prod((w[v][a[v]] for v in keep),start=F(1))
        fibers.append({'bits':''.join(str(a[v]) for v in keep),'models':words,'witness':words[0] if words else None,'count':len(models),'projected_mass':str(retained if words else F(0)),'marginal_mass':str(sum((prod((w[v][m[v]] for v in vs),start=F(1)) for m in models),start=F(0)))})
    def projected(a):return any(sat({**fixed,**a,**b}) for b in assignments(hidden))
    original=diagram(x['order'],sat,w);conditioned=diagram(free,lambda a:sat({**fixed,**a}),w);projected_graph=diagram(keep,projected,w)
    atlas=[]
    for order in permutations(vs):
        g=diagram(list(order),sat,w);atlas.append({'order':list(order),'nodes':len(g['nodes'])})
    sizes=[r['nodes'] for r in atlas]
    return {'format':'compilelab/1','input':x,'truth':truth,'original':original,'conditioned':conditioned,'projected':projected_graph,'fibers':fibers,'atlas':atlas,'summary':{'models':original['count'],'mass':original['mass'],'evidence_models':conditioned['count'],'evidence_mass':str(evmass*F(conditioned['mass'])),'projected_models':projected_graph['count'],'projected_mass':projected_graph['mass'],'best_nodes':min(sizes),'worst_nodes':max(sizes),'best_orders':[r['order'] for r in atlas if r['nodes']==min(sizes)],'worst_orders':[r['order'] for r in atlas if r['nodes']==max(sizes)]}}
