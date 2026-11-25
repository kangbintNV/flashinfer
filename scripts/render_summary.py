"""Render verified before/after results into a native Actions summary."""
import csv
import html
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'experiments/summary.json').read_text())
rows = manifest['results']
assert len(rows) == 50 and manifest['diff_audit_matches'] == 50
formal = 'Bot Run Request Check'
diagnostic = 'GPU Impact — no-reply scenario'


def clean(value):
    return html.escape(str(value or '')).replace('|', '\\|').replace('\n', ' ')[:400]


lines = [
    '# Bot Run Request Check — inventory-fix rerun of 50 PRs', '',
    'This experiment reruns the exact same frozen upstream source, diffs and comment evidence as [the original 50-PR demo](https://github.com/kangbintNV/flashinfer/actions/runs/45554184477).', '',
    '**Only checker behavior change:** validate requested evidence files against the full pinned regular-file tree (`blobs`) instead of the context-trimmed visible list (`visible_paths`).', '',
    '**Model:** `azure/anthropic/claude-opus-5`. Each new analysis uses fresh inference, so model output can vary independently of the fix. No prompts, policies or resource limits were changed.', '',
    '**Source audit:** 50/50 new demo PR diffs match the original PR file lists. Historical source is never executed. No GPU tests were run. Main and merge settings were not modified by this experiment.', '',
    'The formal Check honors historical real internal-bot replies. The extra no-reply scenario deliberately hides them to exercise GPU classification; its results are not historical production `/bot run` outcomes.', '',
    '## Before and after', '',
    '| Measurement | Original demo | Inventory fix |', '| --- | ---: | ---: |',
]
for title, before, after in manifest['comparisons']:
    lines.append(f'| {title} | {before} | {after} |')
lines += ['', '## Current formal Check outcomes', '', '| Reason | Count |', '| --- | ---: |']
for key, count in manifest['formal_counts'].items():
    lines.append(f'| {clean(key)} | {count} |')
lines += ['', '## Current unknown diagnostic reasons', '', '| Reason | Count |', '| --- | ---: |']
for key, count in manifest['unknown_reasons'].items():
    lines.append(f'| {clean(key)} | {count} |')
lines += ['', '## All 50 pairs', '',
          '| Upstream PR | Original demo | New demo / Checks | Formal before → after | GPU class before → after | Current diagnostic reason |',
          '| --- | --- | --- | --- | --- | --- |']
for row in rows:
    old = row['baseline']
    current = row['checks']
    old_impact = old['checks'][diagnostic].get('analysis') or {}
    new_impact = current[diagnostic].get('analysis') or {}
    before_formal = old['checks'][formal]['reason']
    after_formal = current[formal]['reason']
    lines.append(f"| [#{row['upstream_number']}]({row['upstream_url']}) | [#{old['demo_number']}]({old['demo_url']}/checks) | [#{row['demo_number']}]({row['demo_url']}/checks) | {clean(before_formal)} → {clean(after_formal)} | {clean(old_impact.get('classification'))} → {clean(new_impact.get('classification'))} | {clean(new_impact.get('reason'))} |")
lines += ['', 'Unknown means the analysis could not establish a result. It grants no CPU exemption. A GPU-required missing-command failure is an expected policy result. Any separate PR Labeler failures are excluded from this report. Full JSON and CSV are attached as the workflow artifact.']
Path(os.environ['GITHUB_STEP_SUMMARY']).write_text('\n'.join(lines) + '\n')
(ROOT / 'reports').mkdir(exist_ok=True)
(ROOT / 'reports/comparison.json').write_text(json.dumps(manifest, indent=2))
with (ROOT / 'reports/comparison.csv').open('w') as stream:
    writer = csv.writer(stream)
    writer.writerow(['upstream_pr', 'old_demo', 'new_demo', 'old_formal', 'new_formal', 'old_gpu_classification', 'new_gpu_classification', 'new_gpu_reason'])
    for row in rows:
        old = row['baseline']
        impact = row['checks'][diagnostic].get('analysis') or {}
        writer.writerow([row['upstream_url'], old['demo_url'], row['demo_url'], old['checks'][formal]['reason'], row['checks'][formal]['reason'], (old['checks'][diagnostic].get('analysis') or {}).get('classification'), impact.get('classification'), impact.get('reason')])
print('Rendered 50 audited before/after pairs from completed native Checks.')
