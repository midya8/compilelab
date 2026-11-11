"""Shared strict input parsing only. No generation or checking algorithms."""
from fractions import Fraction

def validate(raw):
    if type(raw) is not dict or set(raw) != {'n','clauses','order','weights','evidence','keep'}:
        raise ValueError('exact input keys: n, clauses, order, weights, evidence, keep')
    n=raw['n']
    if type(n) is not int or not 0<=n<=5: raise ValueError('n must be integer 0..5')
    def indices(v):
        return type(v) is list and all(type(x) is int and 0<=x<n for x in v) and len(set(v))==len(v)
    if not indices(raw['order']) or len(raw['order'])!=n: raise ValueError('order must permute 0..n-1')
    if not indices(raw['keep']): raise ValueError('keep must be unique variable indices')
    e=raw['evidence']
    if type(e) is not list or len(e)!=n or any(type(x) is not int or x not in (-1,0,1) for x in e): raise ValueError('evidence entries -1,0,1')
    if any(e[x]!=-1 for x in raw['keep']): raise ValueError('keep cannot contain pinned variables')
    cs=raw['clauses']
    if type(cs) is not list or len(cs)>10: raise ValueError('at most10 CNF clauses')
    for c in cs:
        if type(c) is not list or len(c)>10 or any(type(x) is not int or x==0 or abs(x)>n for x in c): raise ValueError('signed1-based literals,clause length<=10')
    w=raw['weights']
    if type(w) is not list or len(w)!=n: raise ValueError('one false,true weight pair per variable')
    for pair in w:
        if type(pair) is not list or len(pair)!=2: raise ValueError('weight pair needed')
        for x in pair:
            if type(x) is not str or len(x)>10: raise ValueError('rational strings needed')
            try: f=Fraction(x)
            except (ValueError,ZeroDivisionError): raise ValueError('invalid rational') from None
            if f<0 or f.numerator>1000 or f.denominator>1000 or str(f)!=x: raise ValueError('canonical nonnegative rationals,numerator/denominator<=1000')
    return raw
