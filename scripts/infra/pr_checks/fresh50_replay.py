"""I/O-only historical adapter around the unmodified pinned run_pr entry."""
import base64,copy,hashlib,io,json,os,subprocess,sys,time,urllib.request,urllib.error
from dataclasses import asdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(Path(__file__).resolve().parent))
import check_bot_run_request as gate
import ai_test_scope as scope
OUT=ROOT/'reports';OUT.mkdir(exist_ok=True)
DEST='kangbintNV/flashinfer'
MANIFEST=json.loads((ROOT/'experiments/source.json').read_text())
CALLS=[]
real_urlopen=urllib.request.urlopen

def clean(value):
 text=json.dumps(value,ensure_ascii=False)
 for secret in (os.getenv('INFERENCE_API_KEY'),os.getenv('GH_TOKEN')):
  if secret:text=text.replace(secret,'[redacted]')
 return json.loads(text)

def dump(name,value):
 (OUT/name).write_text(json.dumps(clean(value),indent=2,ensure_ascii=False))

def recorded_open(request,*args,**kwargs):
 if not getattr(request,'full_url','').endswith('/chat/completions'):return real_urlopen(request,*args,**kwargs)
 payload=json.loads(request.data);i=len(CALLS)+1
 row={'index':i,'effort':payload.get('reasoning_effort','default'),'context_sha256':hashlib.sha256(payload['messages'][-1]['content'].encode()).hexdigest()}
 CALLS.append(row);dump(f'call-{i}-request.json',payload)
 start=time.monotonic()
 try:
  with real_urlopen(request,*args,**kwargs) as response:raw=response.read(100001)
  data=json.loads(raw);row['finish_reason']=(data.get('choices') or [{}])[0].get('finish_reason');row['usage']=data.get('usage');row['http_status']=200
  dump(f'call-{i}-response.json',data)
  return io.BytesIO(raw)
 except urllib.error.HTTPError as e:
  row['http_status']=e.code
  dump(f'call-{i}-response.json',{'status':e.code,'note':'Response left unread for the actual checker error handler.'})
  raise
 except Exception as e:
  row['transport_error']=type(e).__name__;raise
 finally:row['seconds']=round(time.monotonic()-start,3)

urllib.request.urlopen=recorded_open

class HistoricalClient(gate.Client):
 def __init__(self,m,target,diagnostic=False):
  super().__init__(DEST,timeout=540)
  self.m=m;self.target=target;self.diagnostic=diagnostic;self.result=None;self.check_id=None
  self.pr=copy.deepcopy(m['pr']);self.pr.update(state='open',changed_files=len(m['files']))
  self.pr['head']['sha']=m['comparison_head_sha'];self.pr['base']['sha']=m['comparison_base_sha'];self.pr['base']['ref']='main';self.pr['base']['repo']['full_name']=DEST
  self.out=gate.Client(DEST,timeout=660)
 def get_pr_details(self,n):
  assert n==self.pr['number'];return copy.deepcopy(self.pr)
 def get_current_base_sha(self,pr):return self.m['comparison_base_sha']
 def get_pr_files_at(self,pr,base_sha):
  assert base_sha==self.m['comparison_base_sha'] and pr['head']['sha']==self.m['comparison_head_sha']
  return copy.deepcopy(self.m['files'])
 def get_pr_files(self,n):
  assert n==self.pr['number'];return copy.deepcopy(self.m['files'])
 def comments(self,n):return [] if self.diagnostic else copy.deepcopy(self.m['comments'])
 def checks(self,sha):return [] # New experiment: never reuse another trial's cached verdict.
 def begin(self,pr,check_id=None):
  self.check_id=self.out.begin(self.target);return self.check_id
 def publish(self,pr,result,check_id=None,base_sha=None):
  self.result=asdict(result)
  self.out.publish(self.target,result,check_id,base_sha)
 def get_pr_merge_commit(self,repository,number,base_sha,head_sha):
  commit=self.out.request(f"repos/{DEST}/git/commits/{self.m['snapshot_sha']}")
  assert [p['sha'] for p in commit['parents']]==[base_sha,head_sha]
  assert commit['tree']['sha']==self.m['comparison_head_tree']
  return commit
 def get_repository_tree(self,repository,sha):
  assert sha==self.m['comparison_head_tree']
  cache=Path(os.getenv('EXPERIMENT_CACHE',str(ROOT/'cache')));cache.mkdir(parents=True,exist_ok=True)
  p=cache/('tree-'+sha+'.json')
  if p.exists():return json.loads(p.read_text())
  result=self.out.request(f"repos/{DEST}/git/trees/{sha}?recursive=1")
  if result.get('truncated'):raise gate.TargetSelectionError('Pinned source tree truncated')
  temp=p.with_suffix('.'+str(os.getpid())+'.tmp');temp.write_text(json.dumps(result));temp.replace(p)
  return result
 def get_repository_blob(self,repository,sha,max_bytes):
  if not __import__('re').fullmatch('[0-9a-f]{40}',sha):raise gate.TargetSelectionError('Invalid evidence blob')
  cache=Path(os.getenv('EXPERIMENT_CACHE',str(ROOT/'cache')));cache.mkdir(parents=True,exist_ok=True)
  p=cache/('blob-'+sha)
  if p.exists():raw=p.read_bytes()
  else:
   data=self.out.request(f"repos/{DEST}/git/blobs/{sha}")
   raw=base64.b64decode(data['content'])
   temp=p.with_suffix('.'+str(os.getpid())+'.tmp');temp.write_bytes(raw);temp.replace(p)
  if len(raw)>max_bytes:raise gate.TargetSelectionError('Evidence blob exceeds limit')
  return raw.decode('utf-8')
 def close_merge_snapshot(self):pass

def target_pr():
 c=gate.Client(DEST,timeout=120)
 for attempt in range(12):
  rows=c.request(f"repos/{DEST}/pulls?state=open&head=kangbintNV:{os.environ['GITHUB_REF_NAME']}&per_page=100")
  if len(rows)==1:break
  time.sleep(3)
 if len(rows)!=1:raise ValueError('Expected exactly one experiment PR for this branch')
 pr=rows[0]
 assert pr['head']['sha']==os.environ['GITHUB_SHA']
 return {'number':pr['number'],'head':{'sha':pr['head']['sha']}}

def main():
 # Materialize trusted CI evidence only at runtime, so no upstream workflow is registered or triggered.
 for path in ('.github/workflows/pr-test.yml','scripts/infra/pr_checks/targeted_lane_scope.py'):
  if path in MANIFEST.get('trusted_ci',{}):
   target=ROOT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(MANIFEST['trusted_ci'][path])
 for path,expected in MANIFEST['checker_sha256'].items():
  if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=expected:raise ValueError('Checker file hash mismatch: '+path)
 if MANIFEST.get('mode')=='preflight':
  model=scope.InferenceHub();result=model.complete({},'Return exactly {"ok":true} as JSON.')
  assert result.get('ok') is True
  dump('preflight.json',{'ok':True,'model':model.model,'version':MANIFEST['checker_version'],'calls':CALLS});print('Preflight passed');return
 target=target_pr();results={}
 for diagnostic in [False,True]:
  if diagnostic and results['formal']['reason']!='bot_response_found':
   results['diagnostic']={**results['formal'],'same_as_formal':True,'note':'No response shortcut: formal analysis already supplies this classification.'}
   continue
  name='GPU Impact Diagnostic (no original replies)' if diagnostic else 'Bot Run Request Check'
  gate.CHECK_NAME=name
  before=len(CALLS);client=HistoricalClient(MANIFEST,target,diagnostic)
  result=gate.run_pr(client,MANIFEST['upstream_number'])
  if result is None:raise ValueError('Actual run_pr did not return a verdict')
  results['diagnostic' if diagnostic else 'formal']={**asdict(result),'check_id':client.check_id,'model_call_indices':list(range(before+1,len(CALLS)+1))}
 dump('result.json',{'upstream_number':MANIFEST['upstream_number'],'experiment_pr':target['number'],'experiment_head':target['head']['sha'],'checker_version':MANIFEST['checker_version'],'comparison_base_sha':MANIFEST['comparison_base_sha'],'comparison_head_sha':MANIFEST['comparison_head_sha'],'comment_snapshot_sha256':MANIFEST['comment_snapshot_sha256'],'calls':CALLS,'results':results})
 print(json.dumps({'upstream':MANIFEST['upstream_number'],'formal':results['formal']['reason'],'diagnostic':results['diagnostic']['reason']}))

if __name__=='__main__':
 try:main()
 except Exception as e:
  dump('infrastructure-error.json',{'error':type(e).__name__+': '+str(e),'calls':CALLS});raise
