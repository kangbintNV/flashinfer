from common import *
from concurrent.futures import ThreadPoolExecutor
import shutil,hashlib

def run_one(m):
 n=m['upstream_number'];out=ROOT/f'local-results/{n}.json'
 if out.exists():return json.loads(out.read_text())
 work=ROOT/f'runners/{n}';scripts=work/'scripts/infra/pr_checks';scripts.mkdir(parents=True,exist_ok=True)
 for name in ['check_bot_run_request.py','ai_test_scope.py','gpu_impact.py','scope_evidence.py','merged_source.py']:
  shutil.copyfile(CODE/'scripts/infra/pr_checks'/name,scripts/name)
 s=(ROOT/'replay.py').read_text()
 a=s.index(' def begin(self,pr,check_id=None):');b=s.index(' def get_pr_merge_commit',a)
 s=s[:a]+''' def begin(self,pr,check_id=None):
  context=gate.CHECK_NAME
  r=self.out.request(f"repos/{DEST}/statuses/{self.target['head']['sha']}",'POST',{'state':'pending','context':context,'description':'Evaluating frozen original evidence with pinned actual run_pr entry.'})
  self.check_id=r['id'];return self.check_id
 def publish(self,pr,result,check_id=None,base_sha=None):
  self.result=asdict(result)
  link=f"https://github.com/{DEST}/blob/codex/bot-run-fresh50-20261126/results/results/{self.m['upstream_number']}.json"
  r=self.out.request(f"repos/{DEST}/statuses/{self.target['head']['sha']}",'POST',{'state':'success' if result.conclusion=='success' else 'failure','context':gate.CHECK_NAME,'description':result.title[:140],'target_url':link})
  self.check_id=r['id']
'''+s[b:]
 a=s.index(' def get_repository_tree(');b=s.index(' def close_merge_snapshot',a)
 s=s[:a]+''' def get_repository_tree(self,repository,sha):
  assert sha==self.m['comparison_head_tree']
  p=Path(os.environ['EXPERIMENT_CACHE'])/('tree-'+sha+'.json')
  if p.exists():return json.loads(p.read_text())
  result=self.out.request(f"repos/{DEST}/git/trees/{sha}?recursive=1")
  if result.get('truncated'):raise gate.TargetSelectionError('Pinned source tree truncated')
  temp=p.with_suffix('.'+str(os.getpid())+'.tmp');temp.write_text(json.dumps(result));temp.replace(p)
  return result
 def get_repository_blob(self,repository,sha,max_bytes):
  if not __import__('re').fullmatch('[0-9a-f]{40}',sha):raise gate.TargetSelectionError('Invalid evidence blob')
  p=Path(os.environ['EXPERIMENT_CACHE'])/('blob-'+sha)
  if p.exists():raw=p.read_bytes()
  else:
   data=self.out.request(f"repos/{DEST}/git/blobs/{sha}")
   raw=base64.b64decode(data['content'])
   temp=p.with_suffix('.'+str(os.getpid())+'.tmp');temp.write_bytes(raw);temp.replace(p)
  if len(raw)>max_bytes:raise gate.TargetSelectionError('Evidence blob exceeds limit')
  return raw.decode('utf-8')
'''+s[b:]
 (scripts/'fresh50_replay.py').write_text(s)
 dest=work/'experiments';dest.mkdir(exist_ok=True);(dest/'source.json').write_text(json.dumps(m))
 (ROOT/'cache').mkdir(exist_ok=True)
 env=dict(ENV)
 values={}
 for line in Path('/Users/kangbint/agent_skills/_shared/.env').read_text().splitlines():
  if '=' in line and not line.lstrip().startswith('#'):
   k,v=line.split('=',1);values[k.strip().removeprefix('export ')]=v.strip().strip('\"\'')
 env.update(INFERENCE_API_KEY=values.get('INFERENCE_API_KEY') or values['OPENAI_API_KEY'],INFERENCE_BASE_URL='https://inference-api.nvidia.com/v1',CI_BOT_TARGET_MODEL='azure/anthropic/claude-opus-5',CI_BOT_TARGET_TIMEOUT_SECONDS='360',GITHUB_REF_NAME=m['experiment_head_branch'],GITHUB_SHA=m['experiment_head'],EXPERIMENT_CACHE=str(ROOT/'cache'))
 log=ROOT/f'logs/{n}.log';log.parent.mkdir(exist_ok=True)
 with log.open('w') as f:r=subprocess.run(['python3',str(scripts/'fresh50_replay.py')],env=env,stdout=f,stderr=f,timeout=1200)
 if r.returncode:
  save(f'local-results/{n}-infra.json',{'upstream_number':n,'exit_code':r.returncode,'log':str(log)})
  print('INFRA',n,r.returncode,flush=True);return None
 result=json.loads((work/'reports/result.json').read_text());result['publication_type']='GitHub commit status (Actions unavailable; not native Check Run)'
 save(f'local-results/{n}.json',result)
 print('DONE',n,result['results']['formal']['reason'],(result['results']['diagnostic'].get('analysis') or {}).get('classification'),'calls',len(result['calls']),flush=True)
 return result

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--pr',type=int);p.add_argument('--workers',type=int,default=5);a=p.parse_args()
 rows=[json.loads(x.read_text()) for x in (ROOT/'published').glob('*.json') if '-state' not in x.name]
 if a.pr:rows=[r for r in rows if r['upstream_number']==a.pr]
 with ThreadPoolExecutor(max_workers=a.workers) as ex:list(ex.map(run_one,rows))
