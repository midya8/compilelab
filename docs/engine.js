const gcd=(a,b)=>b?gcd(b,a%b):a;
export class Rational {
 constructor(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error('zero denominator');if(b<0n){a=-a;b=-b}const g=gcd(a<0n?-a:a,b);this.a=a/g;this.b=b/g}
 static parse(s){if(typeof s!=='string'||s.length>10||!/^\d+(\/\d+)?$/.test(s))throw Error('canonical nonnegative rational strings required');const [a,b='1']=s.split('/'),r=new Rational(a,b);if(r.a>1000n||r.b>1000n||r.toString()!==s)throw Error('rational bounds or form');return r}
 add(v){return new Rational(this.a*v.b+v.a*this.b,this.b*v.b)}
 mul(v){return new Rational(this.a*v.a,this.b*v.b)}
 toString(){return this.b===1n?String(this.a):`${this.a}/${this.b}`}
}
const one=()=>new Rational(1),zero=()=>new Rational(0),multiply=xs=>xs.reduce((a,b)=>a.mul(b),one());
export function validate(x){
 const fail=()=>{throw Error('Expected strict compilelab input: n0..5, CNF, full order, rational weight pairs, evidence and keep subset')};
 if(!x||Array.isArray(x)||typeof x!=='object'||Object.keys(x).sort().join()!==['n','clauses','order','weights','evidence','keep'].sort().join())fail();
 const n=x.n,indices=a=>Array.isArray(a)&&a.every(v=>Number.isInteger(v)&&v>=0&&v<n)&&new Set(a).size===a.length;
 if(!Number.isInteger(n)||n<0||n>5||!indices(x.order)||x.order.length!==n||!indices(x.keep))fail();
 if(!Array.isArray(x.evidence)||x.evidence.length!==n||x.evidence.some(v=>!Number.isInteger(v)||![-1,0,1].includes(v))||x.keep.some(v=>x.evidence[v]!==-1))fail();
 if(!Array.isArray(x.clauses)||x.clauses.length>10||x.clauses.some(c=>!Array.isArray(c)||c.length>10||c.some(l=>!Number.isInteger(l)||!l||Math.abs(l)>n)))fail();
 if(!Array.isArray(x.weights)||x.weights.length!==n||x.weights.some(p=>!Array.isArray(p)||p.length!==2))fail();x.weights.forEach(p=>p.forEach(Rational.parse));return x;
}
const words=n=>Array.from({length:2**n},(_,i)=>Array.from({length:n},(_,j)=>(i>>(n-j-1))&1));
const perms=a=>a.length?a.flatMap((v,i)=>perms(a.filter((_,j)=>j!==i)).map(p=>[v,...p])):[[]];
// Browser construction groups truth rows at each prefix, then uses a unique
// triple table. Exact rational masses propagate over graph gaps, not floats.
function graph(order,models,w){
 const nodes=[],trace=[],table=new Map();
 const branch=(depth,rows,prefix)=>{
  if(depth===order.length){const id=rows.length?1:0;trace.push({prefix,node:id,action:'terminal'});return id}
  const v=order[depth],low=branch(depth+1,rows.filter(r=>r[v]===0),prefix+'0'),high=branch(depth+1,rows.filter(r=>r[v]===1),prefix+'1'),key=[v,low,high].join(',');let id,action;
  if(low===high){id=low;action='skip'}else if(table.has(key)){id=table.get(key);action='merge'}else{id=nodes.length+2;table.set(key,id);nodes.push({id,variable:v,low,high});action='new'}
  trace.push({prefix,node:id,action});return id;
 };
 const root=branch(0,models,''),level=new Map(order.map((v,i)=>[v,i])),by=new Map(nodes.map(r=>[r.id,r])),lv=id=>id<2?order.length:level.get(by.get(id).variable),counts=new Map([[0,0],[1,1]]),masses=new Map([[0,zero()],[1,one()]]);
 for(const row of nodes){const i=level.get(row.variable),edge_counts=[],edge_masses=[];
  [row.low,row.high].forEach((child,b)=>{const gap=order.slice(i+1,lv(child));edge_counts.push(2**gap.length*counts.get(child));edge_masses.push(w[row.variable][b].mul(multiply(gap.map(v=>w[v][0].add(w[v][1])))).mul(masses.get(child)))});
  const count=edge_counts.reduce((a,b)=>a+b,0),mass=edge_masses.reduce((a,b)=>a.add(b),zero());counts.set(row.id,count);masses.set(row.id,mass);Object.assign(row,{count,mass:String(mass),edge_counts,edge_masses:edge_masses.map(String)});
 }
 const gap=order.slice(0,lv(root));return {order,root,nodes,trace,count:2**gap.length*counts.get(root),mass:String(multiply(gap.map(v=>w[v][0].add(w[v][1]))).mul(masses.get(root)))};
}
export function analyze(raw){
 const x=validate(raw),vs=Array.from({length:x.n},(_,i)=>i),w=x.weights.map(p=>p.map(Rational.parse)),wt=(bits,variables=vs)=>multiply(variables.map(v=>w[v][bits[v]]));
 const full=words(x.n),truth=full.map(a=>({bits:a.join(''),satisfies:x.clauses.every(c=>c.some(l=>a[Math.abs(l)-1]===Number(l>0))),matches_evidence:x.evidence.every((b,v)=>b===-1||a[v]===b),weight:String(wt(a))}));
 const models=full.filter((_,i)=>truth[i].satisfies),evmodels=full.filter((_,i)=>truth[i].satisfies&&truth[i].matches_evidence),free=x.order.filter(v=>x.evidence[v]===-1),keep=free.filter(v=>x.keep.includes(v));
 const fibers=words(keep.length).map(a=>{const ms=evmodels.filter(m=>keep.every((v,j)=>m[v]===a[j])),models=ms.map(m=>m.join('')),retained=multiply(keep.map((v,j)=>w[v][a[j]]));return {bits:a.join(''),models,witness:models[0]??null,count:models.length,projected_mass:String(ms.length?retained:zero()),marginal_mass:String(ms.reduce((s,m)=>s.add(wt(m)),zero()))}});
 const original=graph(x.order,models,w),conditioned=graph(free,evmodels,w),projected=graph(keep,evmodels,w),atlas=perms(vs).map(order=>({order,nodes:graph(order,models,w).nodes.length})),sizes=atlas.map(r=>r.nodes),best_nodes=Math.min(...sizes),worst_nodes=Math.max(...sizes);
 return {format:'compilelab/1',input:x,truth,original,conditioned,projected,fibers,atlas,summary:{models:models.length,mass:original.mass,evidence_models:evmodels.length,evidence_mass:String(evmodels.reduce((s,m)=>s.add(wt(m)),zero())),projected_models:projected.count,projected_mass:projected.mass,best_nodes,worst_nodes,best_orders:atlas.filter(r=>r.nodes===best_nodes).map(r=>r.order),worst_orders:atlas.filter(r=>r.nodes===worst_nodes).map(r=>r.order)}};
}
export function replay(report){const expected=analyze(report.input),stable=v=>Array.isArray(v)?'['+v.map(stable).join(',')+']':v&&typeof v==='object'?'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+stable(v[k])).join(',')+'}':JSON.stringify(v);if(stable(expected)!==stable(report))throw Error('evidence mismatch');return true}
