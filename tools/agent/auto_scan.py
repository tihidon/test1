"""Read-only local preflight candidate. Never authorizes work or proves comprehension."""
import hashlib
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
DIGEST = re.compile(r'[0-9a-f]{64}')
TEAM = 'plugins_6b07821ba2488191803130852db1560a'
AUDITOR = 'plugins_6b09efdf3dd88191a86ccd61374c07ae'


def skill_binding(role, data, digest, manifest):
    """Compare to a manifest acquired by the trusted coordinator, not task content."""
    if not isinstance(role,str) or role not in ROLES or not isinstance(manifest,dict):
        return False
    record = manifest.get(role)
    if not isinstance(record,dict): return False
    plugin = AUDITOR if role == 'snail-city-defensive-auditor' else TEAM
    release = record.get('release_id')
    return (record.get('plugin_id') == plugin and record.get('path') == 'skills/'+role+'/SKILL.md'
            and isinstance(release,str) and release.startswith('pluginrel_') and len(release)>10
            and isinstance(digest,str) and DIGEST.fullmatch(digest) is not None
            and record.get('sha256') == digest and isinstance(data,bytes)
            and type(record.get('bytes')) is int and record['bytes'] == len(data))


def handoff_binding(handoff, documents, plan, roots):
    """Verify exactly approved whole-line excerpts. Omitted lines remain omitted.
    Trusted coordinator chooses relevant ranges, redacts and authorizes disclosure.
    No semantic completeness or external authority claim is made here.
    """
    if not isinstance(plan,dict) or not isinstance(handoff,dict): return False
    supplied = handoff.get('sources')
    if not isinstance(supplied,dict): return False
    needed = {'canonical:'+p for p in documents}
    needed.update('target:'+p for p,d in documents.items() if not d['same'])
    if set(plan)!=needed or set(supplied)!=needed: return False
    excerpts=[]
    for key in sorted(needed):
        side,path = key.split(':',1)
        rec = supplied[key]; ranges = plan[key]; doc = documents[path][side]
        if not isinstance(rec,dict) or rec.get('blob')!=doc['blob'] or rec.get('ranges')!=ranges:
            return False
        if not isinstance(ranges,list) or not ranges: return False
        raw = git(roots[side],'cat-file','blob',doc['blob'])
        if hashlib.sha256(raw).hexdigest()!=doc['sha256']: return False
        lines = raw.decode('utf-8',errors='strict').splitlines(keepends=True)
        previous=0; parts=[]
        for pair in ranges:
            if not isinstance(pair,list) or len(pair)!=2 or any(type(n) is not int for n in pair): return False
            start,end=pair
            if not previous<start<=end<=len(lines): return False
            parts.append(''.join(lines[start-1:end])); previous=end
        excerpt=''.join(parts)
        if not excerpt.strip() or rec.get('text')!=excerpt: return False
        excerpts.append(excerpt)
    return handoff.get('redacted_content')==''.join(excerpts)

def git(root, *args):
    return subprocess.check_output(['git','--no-replace-objects','--literal-pathspecs','-C',str(root),*args], stderr=subprocess.DEVNULL, timeout=15)

def ref(root, name):
    return git(root,'rev-parse','--verify','--end-of-options',name+'^{commit}').decode().strip()

def blob(root, commit, path):
    if not SHA.fullmatch(commit): raise ValueError('invalid commit')
    if not path or Path(path).is_absolute() or '..' in Path(path).parts or ':' in path:
        raise ValueError('invalid path')
    entry = git(root,'ls-tree','-z',commit,'--',path)
    metadata, sep, name = entry.rstrip(b'\0').partition(b'\t')
    if not sep or name != path.encode('utf-8') or not metadata.startswith((b'100644 blob ', b'100755 blob ')):
        raise ValueError('document must be regular file')
    oid = git(root,'rev-parse','--verify','--end-of-options',commit+':'+path).decode().strip()
    if metadata.split()[-1].decode() != oid: raise ValueError('tree/blob mismatch')
    data = git(root,'cat-file','blob',oid)
    actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if oid != actual or not data.strip(): raise ValueError('invalid or empty blob')
    decoded = data.decode('utf-8',errors='strict')
    if '\0' in decoded or not decoded.strip(): raise ValueError('invalid or empty text')
    return {'blob':oid,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def scan(root, canonical_ref, expected, role, skill_bytes, skill_sha256, *, target_root=None,
         target_ref=None, target_sha=None, task_id='', handoff=None, extra_docs=(),
         resolved_conflicts=None, skill_manifest=None, handoff_plan=None):
    """Expected refs, manifest and handoff plan come from a trusted coordinator.
    A local ref is not proof of remote freshness; caller must recheck remote release/refs.
    This runs in the coordinator, never in the restricted auditor role.
    """
    result={'status':'BLOCKED','task_id':task_id,'role':role,'documents':{},'issues':[],
            'authorization':False,'comprehension_verified':False,'remote_freshness_verified':False}
    issues=result['issues']; resolved_conflicts={} if resolved_conflicts is None else resolved_conflicts
    if not isinstance(task_id,str) or not task_id.strip(): issues.append('MISSING_TASK_ID')
    if not isinstance(role,str) or role not in ROLES: issues.append('UNKNOWN_ROLE')
    if not isinstance(skill_bytes,bytes) or not skill_bytes.strip() or hashlib.sha256(skill_bytes).hexdigest()!=skill_sha256:
        issues.append('MISSING_OR_MISMATCHED_SKILL')
    if not skill_binding(role,skill_bytes,skill_sha256,skill_manifest):
        issues.append('UNVERIFIED_ROLE_SKILL_BINDING')
    else:
        result['skill_identity']={k:skill_manifest[role][k] for k in ('plugin_id','release_id','path','sha256','bytes')}
    if isinstance(role,str) and role in AUDITORS:
        # Only validate redacted handoff metadata here; no claim of authentic review.
        required=('task_id','target_sha','canonical_sha','scope','redacted_content','source_locator')
        if not isinstance(handoff,dict) or any(not isinstance(handoff.get(k),str) or not handoff[k].strip() for k in required):
            issues.append('MISSING_AUDITOR_HANDOFF')
        elif (handoff['task_id'],handoff['target_sha'],handoff['canonical_sha'])!=(task_id,target_sha,expected):
            issues.append('STALE_AUDITOR_HANDOFF')
    try:
        if git(root,'for-each-ref','--format=%(refname)','refs/replace/'):
            issues.append('CANONICAL_REPLACEMENT_REFS'); return result
        if not isinstance(expected,str) or not SHA.fullmatch(expected) or ref(root,canonical_ref)!=expected:
            issues.append('CANONICAL_REF_CHANGED'); return result
        if target_root is None or not isinstance(target_ref,str) or not target_ref or not isinstance(target_sha,str) or not SHA.fullmatch(target_sha):
            issues.append('MISSING_TARGET'); return result
        if git(target_root,'for-each-ref','--format=%(refname)','refs/replace/'):
            issues.append('TARGET_REPLACEMENT_REFS'); return result
        if ref(target_root,target_ref)!=target_sha: issues.append('TARGET_REF_CHANGED'); return result
        if not isinstance(extra_docs,(tuple,list)) or any(not isinstance(p,str) or not p for p in extra_docs) or not isinstance(resolved_conflicts,dict):
            issues.append('INVALID_INPUT_CONTRACT'); return result
        for p in dict.fromkeys((*DOCS,*extra_docs)):
            try:
                a=blob(root,expected,p); b=blob(target_root,target_sha,p)
                result['documents'][p]={'canonical':a,'target':b,'same':a['blob']==b['blob']}
                if a['blob']!=b['blob'] and resolved_conflicts.get(p)!=(a['blob'],b['blob']):
                    issues.append('UNRESOLVED_DIFFERENCE:'+p)
            except (ValueError,subprocess.SubprocessError,OSError): issues.append('MISSING_OR_INVALID:'+p)
        if isinstance(role,str) and role in AUDITORS and not issues:
            if not handoff_binding(handoff,result['documents'],handoff_plan,{'canonical':root,'target':target_root}):
                issues.append('UNVERIFIED_HANDOFF_SOURCES')
        if git(root,'for-each-ref','--format=%(refname)','refs/replace/') or git(target_root,'for-each-ref','--format=%(refname)','refs/replace/'):
            issues.append('REPLACEMENT_REFS_DURING_SCAN')
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
    try:
        result=scan(**scan_inputs)
    except (TypeError,ValueError,AttributeError):
        return {'status':'BLOCKED','issues':['INVALID_INPUT_CONTRACT'],'probe_called':False,
                'authorization':False,'comprehension_verified':False,'remote_freshness_verified':False}
    result['probe_called']=False
    if result['status']=='LOCAL_INPUTS_VERIFIED':
        try:
            for root_key, ref_key, sha_key in (('root','canonical_ref','expected'),('target_root','target_ref','target_sha')):
                root=scan_inputs[root_key]
                if git(root,'for-each-ref','--format=%(refname)','refs/replace/') or ref(root,scan_inputs[ref_key])!=scan_inputs[sha_key]:
                    result['issues'].append('IDENTITY_CHANGED_BEFORE_PROBE')
        except (ValueError,TypeError,subprocess.SubprocessError,OSError,KeyError):
            result['issues'].append('IDENTITY_RECHECK_FAILED')
        if result['issues']:
            result['status']='BLOCKED'; return result
        result['probe_called']=True
        try:
            result['probe_result']=approved_read_only_probe()
        except Exception as exc:
            result['status']='PROBE_FAILED'
            result['issues'].append('PROBE_EXCEPTION:'+type(exc).__name__)
    return result


def run_bundle(bundle, canonical_root, target_root):
    """Invoke existing entry() for a fixed, pinned, read-only identity probe.

    The caller must acquire trusted inputs and approve the task. This local
    command does not fetch remote data or act as a ChatGPT host hook.
    """
    try:
        if not isinstance(bundle, dict):
            raise ValueError("expected object")
        allowed = {"canonical_ref", "expected", "role", "skill_text", "skill_sha256",
                   "target_ref", "target_sha", "task_id", "handoff", "extra_docs",
                   "resolved_conflicts", "skill_manifest", "handoff_plan"}
        if set(bundle) - allowed:
            raise ValueError("unknown fields")
        params = dict(bundle)
        params["skill_bytes"] = params.pop("skill_text").encode("utf-8")
        params["root"] = canonical_root
        params["target_root"] = target_root
        if "resolved_conflicts" in params:
            conflicts = params["resolved_conflicts"]
            if not isinstance(conflicts, dict) or any(
                not isinstance(pair, list) or len(pair) != 2 or
                any(not isinstance(x, str) or not SHA.fullmatch(x) for x in pair)
                for pair in conflicts.values()
            ):
                raise ValueError("invalid conflict identities")
            params["resolved_conflicts"] = {k: tuple(v) for k, v in conflicts.items()}
        return entry(params, lambda: blob(target_root, params["target_sha"],
                                          "tools/agent/auto_scan.py"))
    except (KeyError, AttributeError, TypeError, ValueError, OSError):
        return {"status": "BLOCKED", "issues": ["INVALID_BUNDLE"],
                "probe_called": False, "authorization": False,
                "comprehension_verified": False, "remote_freshness_verified": False}


def main(argv=None):
    import argparse
    import json

    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result

    parser = argparse.ArgumentParser(description="Local AUTO SCAN pilot: fixed read-only identity probe")
    parser.add_argument("--canonical-root", required=True, type=Path)
    parser.add_argument("--target-root", required=True, type=Path)
    parser.add_argument("--bundle", required=True, type=Path,
                        help="Trusted coordinator's local UTF-8 JSON input")
    args = parser.parse_args(argv)
    try:
        bundle = json.loads(args.bundle.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)
        result = run_bundle(bundle, args.canonical_root, args.target_root)
    except (OSError, ValueError, TypeError):
        result = {"status": "BLOCKED", "issues": ["INVALID_BUNDLE"],
                  "probe_called": False, "authorization": False,
                  "comprehension_verified": False, "remote_freshness_verified": False}
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0 if result["status"] == "LOCAL_INPUTS_VERIFIED" and result.get("probe_called") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
