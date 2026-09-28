#!/usr/bin/env python3
"""Read-only metadata lint and impact traversal for optional knowledge maintenance.

No ingestion, persistence, network access, ACL enforcement, or semantic truth claim.
Navigation links may cycle; derivation dependencies must retain acyclic source lineage.
"""
from __future__ import annotations
import argparse
import json
import math
import unicodedata
import sys
from copy import deepcopy
from typing import Any

MAX_BYTES = 1024 * 1024


class KnowledgeError(ValueError):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise KnowledgeError(message)


def _strings(value: Any, label: str, *, empty: bool = True) -> set[str]:
    require(isinstance(value, list) and len(value) <= 1000 and (empty or bool(value)), label + ' must be a bounded array')
    require(all(isinstance(x, str) and bool(x.strip()) and len(x) <= 500 for x in value), label + ' contains invalid text')
    require(len(value) == len(set(value)), 'duplicate ' + label)
    for item in value:
        _identity(item)
    if label.endswith('audience'):
        require('*' not in value or value == ['*'], 'public audience marker must stand alone')
    return set(value)


def _identity(value: Any) -> str:
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= 500, 'invalid identity or revision')
    require(not any(unicodedata.category(c) in {'Cc', 'Cf', 'Cs'} for c in value), 'unsafe metadata text')
    return value


def _index(values: Any, label: str) -> dict[str, dict[str, Any]]:
    require(isinstance(values, list) and len(values) <= 1000, label + ' must be a bounded array')
    result = {}
    for item in values:
        require(isinstance(item, dict), label + ' item must be an object')
        ident = _identity(item.get('id'))
        require(ident not in result, 'duplicate ' + label + ' identity')
        result[ident] = item
    return result


def _audience_allowed(child: set[str], parent: set[str]) -> bool:
    return parent == {'*'} or child <= parent


def inspect(record: Any, changed_sources: list[str] | None = None) -> dict[str, Any]:
    require(isinstance(record, dict) and type(record.get('schema_version')) is int and record['schema_version'] == 1,
            'unsupported knowledge record')
    require(set(record) == {'schema_version', 'sources', 'pages'}, 'unknown knowledge fields')
    sources = _index(record.get('sources'), 'source')
    pages = _index(record.get('pages'), 'page')
    require(not set(sources) & set(pages), 'source and page identities must be distinct')
    for source in sources.values():
        require(set(source) == {'id', 'revision', 'namespace', 'root_id', 'locator', 'available', 'audience'}, 'unexpected source fields')
        for key in ('revision', 'namespace', 'root_id', 'locator'):
            _identity(source.get(key))
        require(type(source.get('available')) is bool, 'source availability must be explicit')
        _strings(source.get('audience'), 'source audience', empty=False)
    dependencies = {}
    for ident, page in pages.items():
        require(set(page) <= {'id', 'namespace', 'audience', 'kind', 'sources', 'depends_on', 'evidence_roots', 'links'}, 'unexpected derived-page fields')
        _identity(page.get('namespace'))
        _strings(page.get('audience'), 'page audience', empty=False)
        require(isinstance(page.get('kind'), str) and page.get('kind') in {'summary', 'topic', 'comparison', 'synthesis', 'index'}, 'derived pages cannot declare policy authority')
        deps = _strings(page.get('depends_on', []), 'derivation dependencies')
        require(deps <= set(pages) and ident not in deps, 'unknown or self derivation dependency')
        dependencies[ident] = deps
        _strings(page.get('evidence_roots'), 'evidence roots')
        refs = page.get('sources')
        require(isinstance(refs, list) and len(refs) <= 1000, 'page sources must be a bounded array')
        seen = set()
        for ref in refs:
            require(isinstance(ref, dict) and set(ref) == {'id', 'revision'}, 'invalid source reference')
            _identity(ref['id']); _identity(ref['revision'])
            require(ref['id'] in sources and ref['id'] not in seen, 'unknown or duplicate source reference')
            seen.add(ref['id'])
        links = _strings(page.get('links', []), 'navigation links')
        require(links <= set(pages), 'unresolved navigation link')
    remaining = {key: set(value) for key, value in dependencies.items()}
    order = []
    while remaining:
        ready = sorted(key for key, value in remaining.items() if not value)
        require(bool(ready), 'circular evidence derivation')
        order.extend(ready)
        for key in ready:
            del remaining[key]
        for value in remaining.values():
            value.difference_update(ready)
    roots: dict[str, set[str]] = {}
    stale: set[str] = set()
    unavailable: set[str] = set()
    require(changed_sources is None or isinstance(changed_sources, list), 'changed sources must be a list')
    changed = _strings(changed_sources or [], 'changed sources')
    require(changed <= set(sources), 'unknown changed source')
    impacted: set[str] = set()
    for ident in order:
        page = pages[ident]
        audience = set(page['audience'])
        roots[ident] = set()
        for ref in page['sources']:
            source = sources[ref['id']]
            require(source['namespace'] == page['namespace'] or set(source['audience']) == {'*'},
                    'cross-namespace private derivation needs an explicitly reviewed minimized source')
            require(_audience_allowed(audience, set(source['audience'])), 'derived audience exceeds source audience')
            roots[ident].add(source['root_id'])
            if ref['revision'] != source['revision']:
                stale.add(ident)
            if not source['available']:
                unavailable.add(ident)
            if ref['id'] in changed:
                impacted.add(ident)
        for dep in dependencies[ident]:
            parent = pages[dep]
            require(parent['namespace'] == page['namespace'] or set(parent['audience']) == {'*'},
                    'cross-namespace private page derivation')
            require(_audience_allowed(audience, set(parent['audience'])), 'derived audience exceeds dependency audience')
            roots[ident].update(roots[dep])
            if dep in stale: stale.add(ident)
            if dep in unavailable: unavailable.add(ident)
            if dep in impacted: impacted.add(ident)
        require(set(page['evidence_roots']) == roots[ident], 'declared evidence roots do not match derivation')
    return {'status': 'metadata-valid', 'review_required': bool(stale or unavailable), 'stale_pages': sorted(stale), 'unavailable_pages': sorted(unavailable),
            'affected_pages': sorted(impacted), 'declared_root_counts': {key: len(roots[key]) for key in order},
            'limitations': 'Does not establish citation entailment, independent witnesses, live source freshness, ACL enforcement, or completed erasure.'}


def query_page(record, page_id, principal, *, observe_source, authorize_page, read_page):
    """Optional host adapter: recheck transitive sources before reading a view.

    Trusted host callbacks must use live access/revision observations. The host
    must also enforce access during reads to close revocation races. No supplied
    audience string is treated as authentication and no cached answer is fallback.
    """
    inspect(record)
    pages = {p['id']: p for p in record['pages']}
    require(page_id in pages, 'Unknown page')
    needed, source_ids = set(), set()
    def visit(ident):
        if ident in needed:
            return
        needed.add(ident)
        source_ids.update(x['id'] for x in pages[ident]['sources'])
        for dep in pages[ident].get('depends_on', []):
            visit(dep)
    visit(page_id)
    live = deepcopy(record)
    for ident in needed:
        require(authorize_page(ident, principal) is True, 'Page unavailable or access denied')
    for source in live['sources']:
        if source['id'] not in source_ids:
            continue
        observed = observe_source(source['id'], principal)
        require(isinstance(observed, dict) and observed.get('allowed') is True
                and observed.get('available') is True, 'Source unavailable or access revoked')
        source['revision'] = _identity(observed.get('revision'))
    result = inspect(live)
    require(page_id not in result['stale_pages'] and page_id not in result['unavailable_pages'], 'View needs source refresh')
    content = read_page(page_id, principal)
    require(isinstance(content, str) and len(content) <= 20000, 'View exceeds bounded retrieval')
    return {'page_id': page_id, 'content': content, 'sources_checked': sorted(source_ids),
            'authority': 'derived-context-only'}


def remove_source(record, source_id, *, block, erase):
    """Block source, dependent pages and caches before idempotent host erasure.

    block(ids) must durably deny both queries and cache reads before returning.
    erase(id) must remove all host copies/index/cache entries or raise. On any
    failure the block stays in place; retries resume safe idempotent erasure.
    """
    result = inspect(record, [source_id])
    ids = [source_id] + result['affected_pages']
    require(block(ids) is True, 'Durable query/cache block was not confirmed')
    receipts = []
    for ident in ids:
        receipt = erase(ident)
        require(isinstance(receipt, str) and bool(receipt.strip()), 'Erasure receipt missing')
        receipts.append({'id': ident, 'receipt': receipt})
    return {'status': 'host-erasure-reported', 'receipts': receipts,
            'limitations': 'Host receipts require independent verification for external backups and stores.'}


def _pairs(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'duplicate JSON key')
        out[key] = value
    return out


def _nonfinite(_):
    raise KnowledgeError('non-finite JSON number')


def parse_input(raw: bytes) -> Any:
    require(len(raw) <= MAX_BYTES, 'input exceeds 1 MiB')
    value = json.loads(raw.decode('utf-8'), object_pairs_hook=_pairs, parse_constant=_nonfinite)
    stack = [(value, 0)]
    count = 0
    while stack:
        item, depth = stack.pop()
        count += 1
        require(depth <= 32 and count <= 50_000, 'input structure exceeds bounds')
        if isinstance(item, dict):
            stack.extend((child, depth + 1) for child in item.values())
            stack.extend((key, depth + 1) for key in item)
        elif isinstance(item, list):
            stack.extend((child, depth + 1) for child in item)
        elif isinstance(item, float):
            require(math.isfinite(item), 'non-finite JSON number')
        elif isinstance(item, str):
            try:
                item.encode('utf-8')
            except UnicodeError as exc:
                raise KnowledgeError('invalid Unicode scalar') from exc
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--changed-source', action='append', default=[])
    args = parser.parse_args()
    try:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        require(len(raw) <= MAX_BYTES, 'input exceeds 1 MiB')
        obj = parse_input(raw)
        result = inspect(obj, args.changed_source)
        print(json.dumps(result, sort_keys=True, ensure_ascii=True))
        return 2 if result['review_required'] else 0
    except (KnowledgeError, ValueError, TypeError, KeyError, UnicodeError, RecursionError) as exc:
        print(json.dumps({'status': 'invalid', 'error': str(exc)}, ensure_ascii=True))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
