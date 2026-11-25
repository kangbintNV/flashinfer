import csv
import html
import json
import os
from pathlib import Path

root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'experiments/summary.json').read_text())
rows=manifest['results']
assert len(rows)==50
assert all(row['checks'].get(name,{}).get('status')=='completed' for row in rows for name in ('Bot Run Request Check','GPU Impact — no-reply scenario'))
native='Bot Run Request Check';diagnostic='GPU Impact — no-reply scenario'
lines=['# Bot Run Request Check — 50 merged PR replay experiments','',
       'These are isolated historical replays in kangbintNV/flashinfer. Original merged source and real original bot-comment identities were used. No GPU tests were executed; main and merge requirements were not changed.','',
       '**Gate version:** `'+manifest['gate_version']+'`  ',
       '**Inference route:** `azure/anthropic/claude-opus-5`  ',
       '**Source-file audit:** '+str(manifest['diff_audit_matches'])+'/50 matched the original PR file list.','',
       'The formal check follows the agreed policy: any genuine internal /bot run response qualifies, including advice/errors; historical replies remain valid. The diagnostic scenario supplies no comment history to expose the GPU-impact analysis independently.','',
       '## Formal gate outcomes','', '| Reason | Count |','| --- | ---: |']
for key,value in manifest['formal_counts'].items():lines.append(f'| {key} | {value} |')
lines+=['','## Diagnostic GPU-impact outcomes','','| Classification | Count |','| --- | ---: |']
for key,value in manifest['classification_counts'].items():lines.append(f'| {key} | {value} |')
lines+=['','Unknown is an analysis failure/abstention, not evidence that a change is GPU-related or CPU-only. See the individual Check for its exact error. The existing fork PR Labeler can fail because its own token is absent; that separate result is excluded from these counts.','',
        '## All 50 experiments','', '| # | Original PR | Demo PR / Checks | Formal result | Diagnostic classification | Diagnostic reason |', '| ---: | --- | --- | --- | --- | --- |']
def clean(value):return html.escape(str(value)).replace('|','\\|').replace('\n',' ')[:280]
for row in rows:
    actual=row['checks'][native];shadow=row['checks'][diagnostic];impact=shadow.get('analysis') or {}
    diagnostic_kind=impact.get('classification') or shadow['reason']
    lines.append(f"| {row['index']} | [#{row['upstream_number']}]({row['upstream_url']}) | [#{row['demo_number']}]({row['demo_url']}/checks) | {clean(actual['conclusion'])}: {clean(actual['reason'])} | {clean(diagnostic_kind)} | {clean(impact.get('reason',''))} |")
Path(os.environ['GITHUB_STEP_SUMMARY']).write_text('\n'.join(lines)+'\n')
(root/'reports').mkdir(exist_ok=True)
(root/'reports/results.json').write_text(json.dumps(manifest,indent=2))
with (root/'reports/results.csv').open('w') as stream:
    writer=csv.writer(stream);writer.writerow(['index','original_pr','demo_checks','formal_conclusion','formal_reason','diagnostic_classification','diagnostic_reason'])
    for row in rows:
        a=row['checks'][native];s=row['checks'][diagnostic];i=s.get('analysis') or {}
        writer.writerow([row['index'],row['upstream_url'],row['demo_url']+'/checks',a['conclusion'],a['reason'],i.get('classification'),i.get('reason')])
print('Rendered 50 complete experiments; all counters derive from the actual GitHub Check outputs.')
