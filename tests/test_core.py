import copy,importlib,inspect,itertools,json,random,subprocess,sys,tempfile,unittest
from pathlib import Path
from fractions import Fraction
from compilelab import analyze,verify
from compilelab.input import validate
from tools.make_cases import base,controls

class EvidenceTests(unittest.TestCase):
 def test_controls(self):
  for name,x in controls():
   with self.subTest(name=name):self.assertTrue(verify(analyze(x)))
 def test_exhaustive_two_variables(self):
  # All512 CNFs drawn from9 non-tautological signed clauses,including empty.
  clauses=[[],[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]]
  count=0
  for mask in range(1<<len(clauses)):
   cs=[c for j,c in enumerate(clauses) if mask>>j&1]
   for keep in ([],[0],[1],[0,1]):
    x=base(2,cs,keep=keep);self.assertTrue(verify(analyze(x)));count+=1
  self.assertEqual(count,2048)
 def test_seeded(self):
  r=random.Random(20261110)
  for i in range(180):
   n=r.randrange(5);cs=[[r.choice((-1,1))*r.randrange(1,n+1) for _ in range(r.randrange(5))] for _ in range(r.randrange(7))] if n else ([] if i%2 else [[]])
   e=[r.choice((-1,-1,-1,0,1)) for _ in range(n)];order=list(range(n));r.shuffle(order)
   x=base(n,cs,evidence=e,order=order,keep=[v for v in range(n) if e[v]==-1 and r.randrange(2)],weights=[[r.choice(('0','1/3','2/3','1','2')) for _ in range(2)] for _ in range(n)])
   self.assertTrue(verify(analyze(x)))
 def test_order_changes_size_not_count(self):
  x=controls()[0][1];r=analyze(x);self.assertEqual((r['summary']['best_nodes'],r['summary']['worst_nodes']),(6,9))
  for row in r['atlas']:
   q=analyze({**x,'order':row['order']});self.assertEqual(q['summary']['models'],4);self.assertEqual(q['original']['mass'],'1/4');self.assertEqual(len(q['original']['nodes']),row['nodes'])
 def test_projection_not_marginal(self):
  r=analyze(controls()[1][1]);self.assertEqual([f['count'] for f in r['fibers']],[1,2]);self.assertEqual(r['summary']['models'],3);self.assertEqual(r['summary']['projected_models'],2);self.assertEqual(r['summary']['mass'],'3/4');self.assertEqual(r['summary']['projected_mass'],'1')
 def test_zero_mass_extensions_survive(self):
  r=analyze(controls()[3][1]);self.assertEqual(r['summary']['mass'],'0');self.assertEqual(r['summary']['projected_models'],2);self.assertEqual(r['summary']['projected_mass'],'1')
 def test_absent_variable_gap(self):
  r=analyze(controls()[2][1]);self.assertEqual(len(r['original']['nodes']),1);self.assertEqual(r['original']['count'],4);self.assertEqual(r['original']['mass'],'40')
 def test_empty_universe(self):
  for cs,count in (([],1),([[]],0)):
   r=analyze(base(0,cs));verify(r);self.assertEqual(r['original']['count'],count);self.assertEqual(len(r['atlas']),1)
 def test_pinned_event_factor(self):
  r=analyze(controls()[6][1]);self.assertEqual(r['conditioned']['mass'],'1');self.assertEqual(r['summary']['evidence_mass'],'1/4');self.assertEqual(r['projected']['count'],1)
 def test_permuted_syntax_canonical(self):
  x=controls()[0][1];r=analyze(x);y=copy.deepcopy(x);y['clauses']=list(reversed(y['clauses']))+[x['clauses'][0]];self.assertEqual(r['original'],analyze(y)['original'])
 def test_reject_noninput_forgeries(self):
  r=analyze(controls()[0][1]);count=0
  def leaves(v,path=()):
   if isinstance(v,dict):
    for k,c in v.items():
     if not path and k=='input':continue
     yield from leaves(c,path+(k,))
   elif isinstance(v,list):
    for i,c in enumerate(v):yield from leaves(c,path+(i,))
   else:yield path,v
  for path,value in leaves(r):
   f=copy.deepcopy(r);cur=f
   for key in path[:-1]:cur=cur[key]
   cur[path[-1]]=not value if type(value) is bool else value+1 if type(value) is int else 'forged' if type(value) is str else 'not-null'
   with self.assertRaises(ValueError):verify(f)
   count+=1
  self.assertGreater(count,500);print('NONINPUT_FORGERIES',count)
 def test_strict_evidence_types(self):
  r=analyze(base(0,[]));r['summary']['models']=True
  with self.assertRaises(ValueError):verify(r)
 def test_input_rejections(self):
  good=controls()[0][1]
  changes=[('n',True),('n',6),('clauses',[[0]]),('clauses',[[5]]),('clauses',[[]]*11),('order',[0,0,2,3]),('weights',[['-1','2']]*4),('weights',[['0.5','1/2']]*4),('weights',[['1/0','1']]*4),('weights',[['1001','0']]*4),('evidence',[1]*4),('keep',[0,0]),('keep',[True]),('extra',1)]
  for key,value in changes:
   x=copy.deepcopy(good);x[key]=value
   with self.assertRaises(ValueError):analyze(x)
 def test_checker_import_boundary(self):
  source=inspect.getsource(importlib.import_module('compilelab.verify'));self.assertNotIn('from .core',source);self.assertNotIn('analyze(',source);self.assertNotIn('diagram(',source)
 def test_cli_atomic(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'bad.json').write_text('{}');(p/'out').write_text('preserve')
   q=subprocess.run([sys.executable,'-m','compilelab',str(p/'bad.json'),'--output',str(p/'out')],capture_output=True)
   self.assertEqual(q.returncode,2);self.assertEqual((p/'out').read_text(),'preserve')
if __name__=='__main__':unittest.main()
