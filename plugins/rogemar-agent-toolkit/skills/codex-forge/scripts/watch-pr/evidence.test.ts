import {describe, expect, it} from 'bun:test';
import {allThreads, collectReviewEvidence, connection, restPages, type JsonQuery} from './evidence.ts';
import {GhGitHubReader, ChecksUnavailable, resolveChecks} from './github.ts';
import {fakeReader, passingCheck, failedCheck, pendingCheck} from './fakes.test-helper.ts';
import {readSnapshot, classifyPr, runSimple} from './policy.ts';
import {parsePrNumber} from './types.ts';
const c = {owner:'owner',repo:'repo',number:parsePrNumber(1)};
const page = (nodes: unknown[], next: string|null = null) => ({nodes,pageInfo:{hasNextPage:next !== null,endCursor:next}});
const snapshot = (reader: ReturnType<typeof fakeReader>) => readSnapshot({reader,context:c,pendingHistory:'include',allowDraft:false});

describe('complete evidence collection', () => {
  it('retains thread 101, all nested replies and resolved state', async () => {
    const query: JsonQuery = async args => {
      const query = args.find(a => a.startsWith('query=')) ?? '';
      const after = args.find(a => a.startsWith('after='));
      if (query.includes('query Threads(')) return {data:{repository:{pullRequest:{reviewThreads: after ? page([{id:'t101',isResolved:true}]) : page(Array.from({length:100},(_,i)=>({id:`t${i}`,isResolved:false})), 'outer2')}}}};
      if (query.includes('query ThreadComments(')) return {data:{node:{comments: after ? page([{body:'later blocker'}]) : page(Array.from({length:100},(_,i)=>({body:`reply${i}`})), 'inner2')}}};
      throw new Error('unexpected fixture request');
    };
    const result = await allThreads(query,c);
    expect(result).toHaveLength(101);
    expect(result[100].isResolved).toBe(true);
    expect(result[100].comments.nodes).toHaveLength(101);
    expect(result[100].comments.nodes[100].body).toBe('later blocker');
  });
  it('collects conversation, review, request and annotation pages at a pinned head', async () => {
    const query: JsonQuery = async args => {
      const path = args.at(-1) ?? '';
      if (args.includes('graphql')) return {data:{repository:{pullRequest:{reviewRequests:page([{requestedReviewer:{__typename:'User',login:'reviewer'}}])}}}};
      if (path.includes('/comments?')) return [[{id:1,body:'first',created_at:'2026-01-01'}],[{id:2,body:'later',created_at:'2026-01-02'}]];
      if (path.includes('/reviews?')) return [[{id:3,body:'fix this',state:'CHANGES_REQUESTED',commit_id:'head'}]];
      if (path.includes('/check-runs?')) return [{check_runs:[{id:1,head_sha:'head',conclusion:'failure'}]}];
      if (path.includes('/annotations?')) return [[{message:'first',path:'a',start_line:1}],[{message:'second',path:'a',start_line:2}]];
      throw new Error('unexpected fixture request');
    };
    const result = await collectReviewEvidence(query,c,'head');
    expect(result.complete).toBe(true); expect(result.comments).toHaveLength(2);
    expect(result.reviews).toHaveLength(1); expect(result.requests).toHaveLength(1);
    expect(result.annotations[0].annotations).toHaveLength(2);
  });
  it('does not cap open PR discovery at 300 or commit history at 50', async () => {
    const query: JsonQuery = async args => {
      if (args.includes('graphql')) return {data:{repository:{pullRequest:{commits: args.some(a=>a.startsWith('after=')) ? page([{commit:{oid:'old-pass',statusCheckRollup:{state:'SUCCESS'}}}]) : page(Array.from({length:100},(_,i)=>({commit:{oid:String(i),statusCheckRollup:null}})), 'next')}}}};
      return [Array.from({length:300},(_,i)=>({number:i+1,head:{ref:`b${i}`,repo:{full_name:'owner/repo'}},base:{ref:'main'}})),[{number:301,head:{ref:'last',repo:{full_name:'owner/repo'}},base:{ref:'main'}}]];
    };
    const reader = new GhGitHubReader(query);
    expect(await reader.openPullRequests(c)).toHaveLength(301);
    expect((await reader.commitRollups(c)).at(-1)).toEqual({oid:'old-pass',state:'SUCCESS'});
  });
  for (const variant of ['partial','missing','repeated','late-error']) it(`rejects ${variant} pagination evidence`, async () => {
    let calls=0;
    const query: JsonQuery = async () => {
      calls++;
      if(variant==='partial') return {data:{items:page([])},errors:[{message:'denied'}]};
      if(variant==='missing') return {data:{items:{nodes:[],pageInfo:{hasNextPage:true,endCursor:null}}}};
      if(variant==='late-error' && calls>1) throw new Error('page two unavailable');
      return {data:{items:page([1], 'same')}};
    };
    await expect(connection(query,'q',c,d=>d.items)).rejects.toThrow();
  });
  it('rejects malformed REST pagination rather than flattening a partial object',async()=>{
    await expect(restPages(async()=>[{message:'denied'}], 'p')).rejects.toThrow();
  });
});

describe('current-head readiness',()=>{
  it('does not trust an incomplete fast success hiding a later failure',async()=>{
    const reader=fakeReader({fastPath:{kind:'checks',checks:[passingCheck()]},rollupPages:[{checks:[passingCheck()],endCursor:'later'},{checks:[failedCheck()],endCursor:null}]});
    expect(classifyPr(await snapshot(reader)).kind).toBe('blocker');
  });
  it('blocks UNKNOWN, BLOCKED and REVIEW_REQUIRED', async()=>{
    for(const facts of [{mergeable:'UNKNOWN' as const},{mergeStateStatus:'UNKNOWN' as const},{mergeStateStatus:'BLOCKED' as const},{reviewDecision:'REVIEW_REQUIRED' as const}])
      expect(classifyPr(await snapshot(fakeReader({facts}))).kind).toBe('blocker');
  });
  it('rejects missing heads and changed head/base evidence',async()=>{
    await expect(snapshot(fakeReader({facts:{headRefOid:null}}))).rejects.toThrow('missing current head SHA');
    for (const change of [{headRefOid:'new'},{baseRefName:'new-base'},{baseRefOid:'new-base-sha'},{mergeable:'UNKNOWN' as const},{isDraft:true}]) {
      const base=fakeReader(); let n=0;
      const reader={...base, async pullRequest(ctx:typeof c){const f=await base.pullRequest(ctx);return ++n>1 ? {...f,...change}:f;}};
      await expect(snapshot(reader)).rejects.toThrow('changed during');
    }
  });
  it('keeps a pending Code Review Gate non-ready',async()=>{
    const reader=fakeReader({fastPath:{kind:'checks',checks:[pendingCheck('Code Review Gate')]}});
    expect(classifyPr(await snapshot(reader)).kind).toBe('waiting');
  });
  it('rejects repeated check cursors',async()=>{
    await expect(resolveChecks(fakeReader({rollupPages:[{checks:[passingCheck()],endCursor:'same'},{checks:[passingCheck()],endCursor:'same'}]}),c)).rejects.toThrow('repeated');
  });
});

it('rejects missing commit or rollup on a later check page', async()=>{
  for (const missing of ['commit','rollup']) {
    let n=0;
    const reader=new GhGitHubReader(async()=>{
      n++;
      const commits=n===1 ? [{commit:{oid:'head',statusCheckRollup:{contexts:page([{__typename:'CheckRun',name:'ci',status:'COMPLETED',conclusion:'SUCCESS'}],'next')}}}] : missing==='commit' ? [] : [{commit:{oid:'head',statusCheckRollup:null}}];
      return {data:{repository:{pullRequest:{commits:{nodes:commits}}}}};
    });
    await expect(resolveChecks(reader,c,'head')).rejects.toThrow(ChecksUnavailable);
  }
});

it('rejects null review surfaces instead of calling them complete',async()=>{
  for(const surface of ['comments','reviews','requests']) {
    const q:JsonQuery=async args=>{
      if(args.includes('graphql'))return {data:{repository:{pullRequest:{reviewRequests:page(surface==='requests'?[null]:[])}}}};
      const path=args.at(-1)??'';
      if(path.includes('/comments?'))return [surface==='comments'?[null]:[]];
      if(path.includes('/reviews?'))return [surface==='reviews'?[null]:[]];
      if(path.includes('/check-runs?'))return [{check_runs:[]}];
      throw new Error('unexpected fixture');
    };
    await expect(collectReviewEvidence(q,c,'head')).rejects.toThrow();
  }
});

it('rechecks draft and mergeability immediately before READY',async()=>{
 for(const change of [{isDraft:true},{mergeable:'UNKNOWN' as const}]){
  const base=fakeReader();let reads=0;
  const reader={...base, async pullRequest(ctx:typeof c){const f=await base.pullRequest(ctx);return ++reads===3?{...f,...change}:f;}};
  const verdict=await runSimple({mode:'single',statusOnly:false,contexts:[c],options:{interval:1,sweepInterval:1,timeout:1,maxQueryErrors:1,allowDraft:false},dependencies:{reader,emit(){},clock:{now:()=>0,observedAt:()=> '2026-01-01',async sleep(){throw new Error('unexpected sleep');}}}});
  expect(verdict.kind).toBe('BLOCKER');expect(verdict.exitCode).toBe(7);
 }
});
