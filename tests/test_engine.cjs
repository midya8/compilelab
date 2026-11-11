const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),cp=require('node:child_process');
test('complete Python and JavaScript evidence reports agree',async()=>{
 const {analyze,replay}=await import('../docs/engine.js');
 const script=`import json,random
from tools.make_cases import controls,base
from compilelab import analyze
r=random.Random(813)
xs=[x for _,x in controls()]
for i in range(90):
 n=r.randrange(4);cs=[[r.choice((-1,1))*r.randrange(1,n+1) for j in range(r.randrange(4))] for k in range(r.randrange(5))] if n else []
 e=[r.choice((-1,-1,0,1)) for j in range(n)]
 xs.append(base(n,cs,evidence=e,keep=[v for v in range(n) if e[v]==-1 and r.randrange(2)]))
print(json.dumps([{'input':x,'report':analyze(x)} for x in xs]))`;
 const rows=JSON.parse(cp.execFileSync('python',['-c',script],{encoding:'utf8',maxBuffer:32*1024*1024}));let nodes=0,traces=0;
 for(const row of rows){const report=analyze(row.input);assert.deepEqual(report,row.report);assert.equal(replay(report),true);for(const k of ['original','conditioned','projected']){nodes+=report[k].nodes.length;traces+=report[k].trace.length}}
 console.log('CROSS_REPORTS',rows.length,'NODES',nodes,'TRACE_ROWS',traces);
});
test('every primitive noninput report field rejects a forged value',async()=>{
 const {analyze,replay}=await import('../docs/engine.js'),x=JSON.parse(fs.readFileSync('docs/example.json')),r=analyze(x);let count=0;
 const visit=(v,path=[])=>{if(v&&typeof v==='object'){for(const key of Object.keys(v)){if(!path.length&&key==='input')continue;visit(v[key],[...path,key])}}else{const f=structuredClone(r);let cur=f;for(const key of path.slice(0,-1))cur=cur[key];cur[path.at(-1)]=typeof v==='boolean'?!v:typeof v==='number'?v+1:typeof v==='string'?'forged':'not-null';assert.throws(()=>replay(f));count++}};visit(r);assert.ok(count>500);console.log('BROWSER_NONINPUT_FORGERIES',count)
});
test('strict input rejects invalid bounds and rational strings',async()=>{const {analyze}=await import('../docs/engine.js'),x=JSON.parse(fs.readFileSync('docs/example.json'));for(const [key,value]of [['n',true],['n',6],['weights',Array(4).fill(['0.5','1/2'])],['order',[0,0,2,3]],['clauses',[[0]]],['keep',[true]]])assert.throws(()=>analyze({...x,[key]:value}))});
