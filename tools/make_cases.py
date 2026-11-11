"""Developed synthetic controls, no real/private data."""
import json
from pathlib import Path

def base(n,clauses,**kw):
    x={'n':n,'clauses':clauses,'order':list(range(n)),'weights':[['1/2','1/2'] for _ in range(n)],'evidence':[-1]*n,'keep':list(range(n))};x.update(kw);return x

def controls():
    return [
        ('paired equality',base(4,[[1,-3],[-1,3],[2,-4],[-2,4]],keep=[0,1])),
        ('unequal extension fibers',base(2,[[1,2]],keep=[0])),
        ('declared absent variable',base(3,[[1]],weights=[['1','2'],['2','3'],['0','4']],keep=[0,2])),
        ('zero mass is not false',base(2,[[1,2]],weights=[['1','0'],['1','0']],keep=[0])),
        ('contradiction',base(3,[[1],[-1]],keep=[2])),
        ('tautology and duplicates',base(3,[[1,-1],[2,2]],keep=[])),
        ('all variables pinned',base(2,[[1,2]],evidence=[1,0],keep=[])),
        ('unsatisfied evidence',base(2,[[1]],evidence=[0,-1],keep=[1])),
        ('empty universe true',base(0,[])),
        ('empty universe false',base(0,[[]])),
        ('five variable multiplexer',base(5,[[-1,-2,4],[-1,2,-4],[1,-3,5],[1,3,-5]],keep=[0,3,4])),
        ('weighted evidence',base(4,[[1,2],[-2,3],[3,-4]],evidence=[-1,1,-1,-1],keep=[0,3],weights=[['2/3','1/3'],['1/4','3/4'],['1/5','4/5'],['1/2','1/2']])),
    ]
if __name__=='__main__':
    p=Path(__file__).resolve().parents[1]/'docs'
    cases=[{'name':name,'input':x} for name,x in controls()];(p/'cases.json').write_text(json.dumps(cases,indent=2)+'\n');(p/'example.json').write_text(json.dumps(cases[0]['input'],indent=2)+'\n')
