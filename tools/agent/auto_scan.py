"""Read-only local preflight candidate. Never authorizes work or proves comprehension."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

DOCS = ('AGENTS.md','docs/README.md', *('docs/tehnika/standardi/'+p for p in (
 'SC-RAD-01-POSTAVKA-IZMENA-BRISANJE.md','SC-AGENT-01-OBAVEZNI-STANDARD-AGENATA.md',
 'SC-BEH-01-PONASANJE-AGENATA.md','SC-DEC-01-LANAC-ODLUCIVANJA.md',
 'SC-INTEGRITY-01-ZASTITA-INTEGRITETA-PROJEKTA.md','SC-REL-01-AGENT-RELIABILITY.md',
 'SC-PMV-01-POST-MERGE-VERIFICATION-STANDARD.md')))
ROLES = ('coordinate-team', *('team-'+r for r in (
 'agent-conduct','architecture','chromium-qa','defensive-auditor','engineering','handoff','legal','marketing',
 'qa-assurance','qa-planning','qa-release','reliability','rendering','stress-test','visual-design')),
 'snail-city-defensive-auditor')
AUDITORS = {'team-defensive-auditor','snail-city-defensive-auditor'}
SHA = re.compile(r'[0-9a-f]{40}')

def git(root, *args):
    return subprocess.check_output(['git','-C',str(root),*args], stderr=subprocess.DEVNULL, timeout=15)

def ref(root, name):
    return git(root,'rev-parse','--verify',name+'^{commit}').decode().strip()

def blob(root, commit, path):
    if not SHA.fullmatch(commit): raise ValueError('invalid commit')
    if not path or Path(path).is_absolute() or '..' in Path(path).parts or ':' in path:
        raise ValueError('invalid path')
    oid = git(root,'rev-parse','--verify',commit+':'+path).decode().strip()
    data = git(root,'cat-file','blob',oid)
    actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if oid != actual or not data.strip(): raise ValueError('invalid or empty blob')
    return {'blob':oid,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def scan(root, canonical_ref, expected, role, skill_bytes, skill_sha256, *, target_root=None,
         target_ref=None, target_sha=None, task_id='', handoff=None, extra_docs=(),
         resolved_conflicts=None):
    """Expected refs and skill digest come from a trusted coordinator, never candidate data.
    A local ref is not proof of remote freshness; caller must recheck remote release/refs.
    This runs in the coordinator, never in the restricted auditor role.
    """
    result={'status':'BLOCKED','task_id':task_id,'role':role,'documents':{},'issues':[],
            'authorization':False,'comprehension_verified':False,'remote_freshness_verified':False}
    issues=result['issues']; resolved_conflicts=resolved_conflicts or {}
    if not task_id.strip(): issues.append('MISSING_TASK_ID')
    if role not in ROLES: issues.append('UNKNOWN_ROLE')
    if not isinstance(skill_bytes,bytes) or not skill_bytes.strip() or hashlib.sha256(skill_bytes).hexdigest()!=skill_sha256:
        issues.append('MISSING_OR_MISMATCHED_SKILL')
    if role in AUDITORS:
        # Only validate redacted handoff metadata here; no claim of authentic review.
        required=('task_id','target_sha','canonical_sha','scope','redacted_content','source_locator')
        if not isinstance(handoff,dict) or any(not handoff.get(k) for k in required):
            issues.append('MISSING_AUDITOR_HANDOFF')
        elif (handoff['task_id'],handoff['target_sha'],handoff['canonical_sha'])!=(task_id,target_sha,expected):
            issues.append('STALE_AUDITOR_HANDOFF')
    try:
        if not SHA.fullmatch(expected) or ref(root,canonical_ref)!=expected:
            issues.append('CANONICAL_REF_CHANGED'); return result
        if target_root is None or not target_ref or not target_sha or not SHA.fullmatch(target_sha):
            issues.append('MISSING_TARGET'); return result
        if ref(target_root,target_ref)!=target_sha: issues.append('TARGET_REF_CHANGED'); return result
        for p in dict.fromkeys((*DOCS,*extra_docs)):
            try:
                a=blob(root,expected,p); b=blob(target_root,target_sha,p)
                result['documents'][p]={'canonical':a,'target':b,'same':a['blob']==b['blob']}
                if a['blob']!=b['blob'] and resolved_conflicts.get(p)!=(a['blob'],b['blob']):
                    issues.append('UNRESOLVED_DIFFERENCE:'+p)
            except (ValueError,subprocess.SubprocessError,OSError): issues.append('MISSING_OR_INVALID:'+p)
        if ref(root,canonical_ref)!=expected: issues.append('CANONICAL_REF_CHANGED_DURING_SCAN')
        if ref(target_root,target_ref)!=target_sha: issues.append('TARGET_REF_CHANGED_DURING_SCAN')
    except (ValueError,TypeError,subprocess.SubprocessError,OSError): issues.append('REF_OR_IO_FAILURE')
    if not issues: result['status']='LOCAL_INPUTS_VERIFIED'
    return result

def entry(scan_inputs, approved_read_only_probe):
    """Controlled local entry: no probe invocation unless input verification succeeds.
    Probe must already be approved, read-only and supplied by the trusted caller.
    Not a general command runner or host-tool security boundary.
    """
    result=scan(**scan_inputs)
    result['probe_called']=False
    if result['status']=='LOCAL_INPUTS_VERIFIED':
        result['probe_called']=True
        result['probe_result']=approved_read_only_probe()
    return result
