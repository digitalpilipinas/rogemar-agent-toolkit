import type { PrContext } from './types.ts';

export type JsonQuery = (args: readonly [string, ...string[]]) => Promise<unknown>;
export interface ReviewEvidence {
  readonly head: string;
  readonly capturedAt: string;
  readonly complete: true;
  readonly comments: readonly unknown[];
  readonly reviews: readonly unknown[];
  readonly requests: readonly unknown[];
  readonly annotations: readonly {run: unknown; annotations: readonly unknown[]}[];
}
export function object(value: unknown): Record<string, any> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Expected evidence object');
  return value as Record<string, any>;
}
export async function restPages(query: JsonQuery, path: string): Promise<any[]> {
  const pages = await query(['gh', 'api', '--method', 'GET', '--paginate', '--slurp', path]);
  if (!Array.isArray(pages) || !pages.every(Array.isArray)) throw new Error('Expected complete REST page arrays');
  return pages.flat();
}
export async function connection(query: JsonQuery, document: string, context: PrContext,
  select: (data: any) => unknown, extra: readonly string[] = []): Promise<any[]> {
  const nodes: any[] = [], seen = new Set<string>();
  let after: string | null = null;
  do {
    const args: [string, ...string[]] = ['gh', 'api', 'graphql', '-f', `query=${document}`,
      '-f', `owner=${context.owner}`, '-f', `repo=${context.repo}`, '-F', `pr=${context.number}`, ...extra];
    if (after !== null) args.push('-f', `after=${after}`);
    const raw = object(await query(args));
    if (raw.errors && (!Array.isArray(raw.errors) || raw.errors.length)) throw new Error('Partial GraphQL evidence');
    const page = object(select(raw.data));
    if (!Array.isArray(page.nodes)) throw new Error('Missing connection nodes');
    const info = object(page.pageInfo);
    if (typeof info.hasNextPage !== 'boolean') throw new Error('Missing pagination flag');
    nodes.push(...page.nodes);
    if (!info.hasNextPage) break;
    if (typeof info.endCursor !== 'string' || !info.endCursor || seen.has(info.endCursor)) throw new Error('Missing or repeated pagination cursor');
    seen.add(info.endCursor); after = info.endCursor;
  } while (true);
  return nodes;
}
export const THREADS = `query Threads($owner:String!,$repo:String!,$pr:Int!,$after:String) {
 repository(owner:$owner,name:$repo) {pullRequest(number:$pr) {reviewThreads(first:100,after:$after) {
 nodes {id isResolved} pageInfo {hasNextPage endCursor}}}}}`;
export const COMMENTS = `query ThreadComments($id:ID!,$after:String) {
 node(id:$id) {... on PullRequestReviewThread {comments(first:100,after:$after) {
 nodes {id body createdAt path line author {login}} pageInfo {hasNextPage endCursor}}}}}`;
export async function allThreads(query: JsonQuery, context: PrContext): Promise<any[]> {
  const threads = await connection(query, THREADS, context, d => d?.repository?.pullRequest?.reviewThreads);
  const result: any[] = [];
  for (const raw of threads) {
    const t = object(raw);
    if (typeof t.id !== 'string' || typeof t.isResolved !== 'boolean') throw new Error('Invalid review thread');
    const comments = await connection(query, COMMENTS, context, d => d?.node?.comments, ['-f', `id=${t.id}`]);
    result.push({...t, comments: {nodes: comments}});
  }
  return result;
}
export const COMMITS = `query Commits($owner:String!,$repo:String!,$pr:Int!,$after:String) {
 repository(owner:$owner,name:$repo) {pullRequest(number:$pr) {commits(first:100,after:$after) {
 nodes {commit {oid statusCheckRollup {state}}} pageInfo {hasNextPage endCursor}}}}}`;
export const REQUESTS = `query Requests($owner:String!,$repo:String!,$pr:Int!,$after:String) {
 repository(owner:$owner,name:$repo) {pullRequest(number:$pr) {reviewRequests(first:100,after:$after) {
 nodes {requestedReviewer {__typename ... on User {login} ... on Team {name slug}}} pageInfo {hasNextPage endCursor}}}}}`;
function textField(value: unknown, label: string): void {
  if (typeof value !== 'string') throw new Error(`Missing evidence ${label}`);
}
function identity(value: unknown): void {
  const v=object(value);
  if (!Number.isSafeInteger(v.id) || v.id <= 0) throw new Error('Missing evidence identity');
}
export async function collectReviewEvidence(query: JsonQuery, c: PrContext, head: string): Promise<ReviewEvidence> {
  const root = `repos/${c.owner}/${c.repo}`;
  const comments = await restPages(query, `${root}/issues/${c.number}/comments?per_page=100`);
  const reviews = await restPages(query, `${root}/pulls/${c.number}/reviews?per_page=100`);
  const requests = await connection(query, REQUESTS, c, d => d?.repository?.pullRequest?.reviewRequests);
  for (const v of comments) { identity(v); textField(v.body,'comment.body'); textField(v.created_at,'comment.created_at'); }
  for (const v of reviews) {
    identity(v); textField(v.body,'review.body'); textField(v.commit_id,'review.commit_id');
    if (!['APPROVED','CHANGES_REQUESTED','COMMENTED','DISMISSED','PENDING'].includes(v.state)) throw new Error('Unknown review state');
  }
  for (const v of requests) {
    const reviewer=object(object(v).requestedReviewer);
    if (reviewer.__typename==='User') textField(reviewer.login,'reviewer.login');
    else if (reviewer.__typename==='Team') textField(reviewer.slug,'reviewer.slug');
    else throw new Error('Unknown requested reviewer type');
  }
  const raw = await query(['gh','api','--method','GET','--paginate','--slurp',`${root}/commits/${head}/check-runs?per_page=100&filter=all`]);
  if (!Array.isArray(raw) || !raw.every(p => Array.isArray(object(p).check_runs))) throw new Error('Invalid check-run pages');
  const runs = raw.flatMap(p => object(p).check_runs);
  const annotations: {run: unknown; annotations: readonly unknown[]}[] = [];
  for (const value of runs) {
    const run = object(value);
    if (!Number.isSafeInteger(run.id) || run.head_sha !== head) throw new Error('Missing or stale check-run identity');
    const items=await restPages(query, `${root}/check-runs/${run.id}/annotations?per_page=100`);
    for (const v of items) {const item=object(v);textField(item.message,'annotation.message');textField(item.path,'annotation.path');if(!Number.isSafeInteger(item.start_line))throw new Error('Missing annotation line');}
    annotations.push({run, annotations: items});
  }
  return {head, capturedAt: new Date().toISOString(), complete: true, comments, reviews, requests, annotations};
}
