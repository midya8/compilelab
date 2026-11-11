import {readFileSync} from 'node:fs';import {analyze} from '../docs/engine.js';const xs=JSON.parse(readFileSync(0,'utf8'));console.log(JSON.stringify(xs.map(analyze)));
