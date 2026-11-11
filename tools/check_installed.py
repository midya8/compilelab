"""Build wheel,install outside checkout,check both CLI entry points."""
import json,os,subprocess,sys,tempfile,venv
from pathlib import Path
from tools.make_cases import controls
root=Path(__file__).resolve().parents[1]
def run(args,**kw):return subprocess.run(args,check=True,capture_output=True,text=True,**kw)
with tempfile.TemporaryDirectory() as td:
 p=Path(td);run([sys.executable,'-m','pip','wheel','--no-deps','-w',str(p),str(root)])
 venv.EnvBuilder(with_pip=True).create(p/'venv');python=str(p/'venv/bin/python');run([python,'-m','pip','install','--no-deps',str(next(p.glob('*.whl')))],cwd=p)
 env={k:v for k,v in os.environ.items() if k!='PYTHONPATH'};env['PYTHONNOUSERSITE']='1';origins=json.loads(run([python,'-c','import compilelab,compilelab.core,compilelab.verify,compilelab.input,compilelab.__main__,json;print(json.dumps([m.__file__ for m in (compilelab,compilelab.core,__import__("compilelab.verify",fromlist=["x"]),compilelab.input,compilelab.__main__)]))'],cwd=p,env=env).stdout)
 assert all('site-packages' in v and str(root) not in v for v in origins)
 for name,x in controls():
  (p/'input.json').write_text(json.dumps(x))
  for cmd in ([python,'-m','compilelab'],[str(p/'venv/bin/compilelab')]):
   run(cmd+['input.json','--output','report.json'],cwd=p,env=env);run(cmd+['report.json','--verify'],cwd=p,env=env)
   report=json.loads((p/'report.json').read_text());report['summary']['models']+=1;(p/'forged.json').write_text(json.dumps(report))
   q=subprocess.run(cmd+['forged.json','--verify'],cwd=p,env=env,capture_output=True);assert q.returncode==2
 print(json.dumps({'module_origins':origins,'controls':len(controls()),'entry_points':2,'forgery_rejections':len(controls())*2}))
