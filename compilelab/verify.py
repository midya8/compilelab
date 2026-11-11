"""Independent checker: bitmask census and residual truth-vector quotient.

Imports only shared input validation. Never invokes the Shannon generator,
its diagram builder, graph dynamic program or analysis function.
"""
import json
from fractions import Fraction as F

def exact(a,b):
    return json.dumps(a,sort_keys=True,separators=(',',':'))==json.dumps(b,sort_keys=True,separators=(',',':'))

from itertools import permutations
from math import prod
from .input import validate

def verify(report):
    try:
        x=validate(report['input']);n=x['n'];w=[[F(s) for s in pair] for pair in x['weights']];vs=list(range(n))
        rows=[];satset=[];evset=[]
        def weight(bits,variables):return prod((w[v][bits[v]] for v in variables),start=F(1))
        def fmt(bits):return ''.join(map(str,bits))
        for mask in range(1<<n):
            bits=[(mask>>(n-v-1))&1 for v in vs]
            satisfied=all(sum(int(bits[abs(l)-1]==(1 if l>0 else 0)) for l in clause)>0 for clause in x['clauses'])
            matched=all(e==-1 or bits[v]==e for v,e in enumerate(x['evidence']))
            rows.append({'bits':fmt(bits),'satisfies':satisfied,'matches_evidence':matched,'weight':str(weight(bits,vs))})
            if satisfied:satset.append(bits)
            if satisfied and matched:evset.append(bits)
        assert report['format']=='compilelab/1' and exact(report['truth'],rows)
        free=[v for v in x['order'] if x['evidence'][v]==-1];keep=[v for v in free if v in x['keep']]
        def census(order,models):
            # Distinct Boolean residual truth vectors at each level. Constant
            # residuals are terminals. Equal adjacent cofactors skip a level.
            signatures={}; trace=[]; pending={}; nextid=2
            for depth in range(len(order),-1,-1):
                for prefmask in range(1<<depth):
                    pref=tuple((prefmask>>(depth-j-1))&1 for j in range(depth))
                    residual=[]
                    for tailmask in range(1<<(len(order)-depth)):
                        tail=tuple((tailmask>>(len(order)-depth-j-1))&1 for j in range(len(order)-depth))
                        values=pref+tail
                        residual.append(int(any(all(m[v]==values[j] for j,v in enumerate(order)) for m in models)))
                    signatures[pref]=tuple(residual)
            # ID convention is low-first postorder. Construct with an explicit
            # prefix sorting pass, then classify using residual truth functions.
            prefixes=sorted(signatures,key=lambda a: tuple(list(a)+[2]))
            unique={};node_for={};spec={}
            for pref in prefixes:
                depth=len(pref);sig=signatures[pref]
                if depth==len(order):node=sig[0];action='terminal'
                elif signatures[pref+(0,)]==signatures[pref+(1,)]:node=node_for[pref+(0,)];action='skip'
                else:
                    key=(depth,sig)
                    if key in unique:node=unique[key];action='merge'
                    else:
                        node=nextid;nextid+=1;unique[key]=node;action='new'
                        spec[node]=(order[depth],node_for[pref+(0,)],node_for[pref+(1,)],pref)
                node_for[pref]=node;trace.append({'prefix':''.join(map(str,pref)),'node':node,'action':action})
            nodes=[]
            for k,(v,lo,hi,pref) in spec.items():
                d=len(pref);r={'id':k,'variable':v,'low':lo,'high':hi};counts=[];masses=[]
                for b in (0,1):
                    valid=[]
                    for mask in range(1<<(len(order)-d-1)):
                        tail=[(mask>>(len(order)-d-2-j))&1 for j in range(len(order)-d-1)]
                        value=list(pref)+[b]+tail
                        if any(all(m[z]==value[j] for j,z in enumerate(order)) for m in models):
                            a={z:value[j] for j,z in enumerate(order)};valid.append(weight(a,order[d:]))
                    counts.append(len(valid));masses.append(str(sum(valid,start=F(0))))
                r.update(count=sum(counts),mass=str(sum(map(F,masses),start=F(0))),edge_counts=counts,edge_masses=masses);nodes.append(r)
            unique_models={tuple(m[v] for v in order) for m in models}
            mass=sum((prod((w[v][values[j]] for j,v in enumerate(order)),start=F(1)) for values in unique_models),start=F(0))
            return {'order':order,'root':node_for[()],'nodes':nodes,'trace':trace,'count':len(unique_models),'mass':str(mass)}
        orig=census(x['order'],satset);cond=census(free,evset);proj=census(keep,evset)
        assert exact(report['original'],orig) and exact(report['conditioned'],cond) and exact(report['projected'],proj)
        fibers=[]
        for mask in range(1<<len(keep)):
            vals=[(mask>>(len(keep)-j-1))&1 for j in range(len(keep))]
            matching=[m for m in evset if all(m[v]==vals[j] for j,v in enumerate(keep))];words=list(map(fmt,matching))
            retained=prod((w[v][vals[j]] for j,v in enumerate(keep)),start=F(1))
            fibers.append({'bits':fmt(vals),'models':words,'witness':words[0] if words else None,'count':len(words),'projected_mass':str(retained if words else F(0)),'marginal_mass':str(sum((weight(m,vs) for m in matching),start=F(0)))})
        assert exact(report['fibers'],fibers)
        atlas=[{'order':list(o),'nodes':len(census(list(o),satset)['nodes'])} for o in permutations(vs)]
        assert exact(report['atlas'],atlas)
        sizes=[r['nodes'] for r in atlas];summary={'models':len(satset),'mass':str(sum((weight(m,vs) for m in satset),start=F(0))),'evidence_models':len(evset),'evidence_mass':str(sum((weight(m,vs) for m in evset),start=F(0))),'projected_models':len({tuple(m[v] for v in keep) for m in evset}),'projected_mass':proj['mass'],'best_nodes':min(sizes),'worst_nodes':max(sizes),'best_orders':[r['order'] for r in atlas if r['nodes']==min(sizes)],'worst_orders':[r['order'] for r in atlas if r['nodes']==max(sizes)]}
        assert exact(report['summary'],summary)
        assert set(report)=={'format','input','truth','original','conditioned','projected','fibers','atlas','summary'}
        return True
    except (KeyError,TypeError,ValueError,AssertionError,IndexError,OverflowError) as exc:
        raise ValueError('evidence mismatch or invalid input') from exc
