import hashlib, subprocess, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import auto_scan as a

class AutoScanTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name); self.git('init','-q'); self.git('config','user.name','Fixture'); self.git('config','user.email','fixture@example.invalid')
        for p in a.DOCS:
            f=self.root/p; f.parent.mkdir(parents=True,exist_ok=True); f.write_text('fixture '+p+'\n')
        self.git('add','.'); self.git('commit','-qm','baseline'); self.sha=a.ref(self.root,'HEAD'); self.skill=b'test skill\n'; self.manifest={role:dict(plugin_id=a.AUDITOR if role=='snail-city-defensive-auditor' else a.TEAM,release_id='pluginrel_fixture',path='skills/'+role+'/SKILL.md',sha256=hashlib.sha256(self.skill).hexdigest(),bytes=len(self.skill)) for role in a.ROLES}
        self.args=dict(root=self.root,canonical_ref='HEAD',expected=self.sha,role='coordinate-team',skill_bytes=self.skill,skill_sha256=hashlib.sha256(self.skill).hexdigest(),target_root=self.root,target_ref='HEAD',target_sha=self.sha,task_id='QA-TEST',skill_manifest=self.manifest)
    def git(self,*args): return a.git(self.root,*args)
    def run_scan(self,**kwargs): return a.scan(**(self.args|kwargs))
    def commit(self): self.git('add','-A'); self.git('commit','-qm','change'); return a.ref(self.root,'HEAD')
    def handoff(self):
        plan={'canonical:'+p:[[1,1]] for p in a.DOCS}
        sources={k:dict(blob=a.blob(self.root,self.sha,k.split(':',1)[1])['blob'],ranges=v,text=(self.root/k.split(':',1)[1]).read_text()) for k,v in plan.items()}
        return dict(task_id='QA-TEST',target_sha=self.sha,canonical_sha=self.sha,scope='fixture',redacted_content=''.join(sources[k]['text'] for k in sorted(sources)),source_locator='fixture',sources=sources),plan
    def test_all_17_role_entries(self):
        for role in a.ROLES:
            with self.subTest(role=role):
                handoff,plan=self.handoff() if role in a.AUDITORS else (None,None)
                calls=[]; result=a.entry(self.args|dict(role=role,handoff=handoff,handoff_plan=plan),lambda: calls.append('probe'))
                self.assertEqual(result['status'],'LOCAL_INPUTS_VERIFIED'); self.assertEqual(calls,['probe']); self.assertFalse(result['authorization']); self.assertFalse(result['remote_freshness_verified'])
    def test_missing_skill(self): self.assertIn('MISSING_OR_MISMATCHED_SKILL',self.run_scan(skill_bytes=b'')['issues'])
    def test_wrong_skill_digest(self): self.assertIn('MISSING_OR_MISMATCHED_SKILL',self.run_scan(skill_bytes=b'changed')['issues'])
    def test_unknown_role(self): self.assertIn('UNKNOWN_ROLE',self.run_scan(role='invented')['issues'])
    def test_missing_task(self): self.assertIn('MISSING_TASK_ID',self.run_scan(task_id='')['issues'])
    def test_missing_target(self): self.assertIn('MISSING_TARGET',self.run_scan(target_sha=None)['issues'])
    def test_auditor_without_handoff(self): self.assertIn('MISSING_AUDITOR_HANDOFF',self.run_scan(role='snail-city-defensive-auditor')['issues'])
    def test_auditor_stale_handoff(self):
        h=dict(task_id='wrong',target_sha=self.sha,canonical_sha=self.sha,scope='fixture',redacted_content='rules',source_locator='fixture'); self.assertIn('STALE_AUDITOR_HANDOFF',self.run_scan(role='team-defensive-auditor',handoff=h)['issues'])
    def test_blocked_entry_does_not_invoke_probe(self):
        calls=[]; result=a.entry(self.args|dict(skill_bytes=b''),lambda: calls.append('wrong')); self.assertFalse(result['probe_called']); self.assertEqual(calls,[])
    def test_canonical_changed(self):
        (self.root/'AGENTS.md').write_text('changed'); self.commit(); self.assertIn('CANONICAL_REF_CHANGED',self.run_scan()['issues'])
    def test_missing_doc(self):
        (self.root/'AGENTS.md').unlink(); new=self.commit(); self.assertIn('MISSING_OR_INVALID:AGENTS.md',self.run_scan(expected=new,target_sha=new)['issues'])
    def test_empty_doc(self):
        (self.root/'AGENTS.md').write_text(''); new=self.commit(); self.assertIn('MISSING_OR_INVALID:AGENTS.md',self.run_scan(expected=new,target_sha=new)['issues'])
    def test_target_changed(self): self.assertIn('TARGET_REF_CHANGED',self.run_scan(target_sha='1'*40)['issues'])
    def test_ref_moves_mid_scan(self):
        original=a.blob; moved=False
        def move(*args):
            nonlocal moved
            if not moved:
                moved=True; (self.root/'AGENTS.md').write_text('changed'); self.commit()
            return original(*args)
        with patch.object(a,'blob',side_effect=move): result=self.run_scan()
        self.assertIn('CANONICAL_REF_CHANGED_DURING_SCAN',result['issues'])
    def test_different_target_and_exact_resolution(self):
        self.git('branch','frozen',self.sha); (self.root/'AGENTS.md').write_text('target specific'); new=self.commit(); args=dict(canonical_ref='frozen',target_sha=new)
        r=self.run_scan(**args); self.assertIn('UNRESOLVED_DIFFERENCE:AGENTS.md',r['issues']); d=r['documents']['AGENTS.md']; self.assertEqual(self.run_scan(**args,resolved_conflicts={'AGENTS.md':(d['canonical']['blob'],d['target']['blob'])})['status'],'LOCAL_INPUTS_VERIFIED')
    def test_truncated_blob(self):
        original=a.git
        def truncate(root,*args):
            b=original(root,*args); return b[:-1] if args[:2]==('cat-file','blob') else b
        with patch.object(a,'git',side_effect=truncate): self.assertIn('MISSING_OR_INVALID:AGENTS.md',self.run_scan()['issues'])
    def test_extra_required_doc(self): self.assertIn('MISSING_OR_INVALID:extra.md',self.run_scan(extra_docs=('extra.md',))['issues'])

    def test_symlink_document(self):
        p=self.root/'AGENTS.md'; p.unlink(); p.symlink_to('missing.md'); new=self.commit(); self.assertIn('MISSING_OR_INVALID:AGENTS.md',self.run_scan(expected=new,target_sha=new)['issues'])
    def test_binary_document(self):
        (self.root/'AGENTS.md').write_bytes(b'\xff\x00'); new=self.commit(); self.assertIn('MISSING_OR_INVALID:AGENTS.md',self.run_scan(expected=new,target_sha=new)['issues'])
    def test_whitespace_handoff(self):
        h,p=self.handoff(); h['scope']=' '; self.assertIn('MISSING_AUDITOR_HANDOFF',self.run_scan(role='snail-city-defensive-auditor',handoff=h,handoff_plan=p)['issues'])
    def test_wrong_handoff_type(self):
        h,p=self.handoff(); h['scope']=True; self.assertIn('MISSING_AUDITOR_HANDOFF',self.run_scan(role='team-defensive-auditor',handoff=h,handoff_plan=p)['issues'])
    def test_null_task(self): self.assertIn('MISSING_TASK_ID',self.run_scan(task_id=None)['issues'])
    def test_malformed_role(self): self.assertIn('UNKNOWN_ROLE',self.run_scan(role=[])['issues'])
    def test_replacement(self):
        (self.root/'AGENTS.md').write_text('replacement'); other=self.commit(); self.git('reset','--hard',self.sha); self.git('replace',self.sha,other); self.assertIn('CANONICAL_REPLACEMENT_REFS',self.run_scan()['issues'])
    def test_ref_change_before_probe(self):
        scan=a.scan
        def move(**kw):
            r=scan(**kw); (self.root/'AGENTS.md').write_text('changed'); self.commit(); return r
        with patch.object(a,'scan',side_effect=move): r=a.entry(self.args,lambda:self.fail('probe must not run'))
        self.assertEqual(r['status'],'BLOCKED'); self.assertIn('IDENTITY_CHANGED_BEFORE_PROBE',r['issues'])
    def test_fragment_handoff(self):
        h,p=self.handoff(); h['redacted_content']='unrelated fragment'; self.assertIn('UNVERIFIED_HANDOFF_SOURCES',self.run_scan(role='snail-city-defensive-auditor',handoff=h,handoff_plan=p)['issues'])
    def test_wrong_role_skill(self):
        b=b'visual-design skill'; self.assertIn('UNVERIFIED_ROLE_SKILL_BINDING',self.run_scan(role='team-engineering',skill_bytes=b,skill_sha256=hashlib.sha256(b).hexdigest())['issues'])
    def test_missing_manifest(self): self.assertIn('UNVERIFIED_ROLE_SKILL_BINDING',self.run_scan(skill_manifest=None)['issues'])
    def test_missing_handoff_source(self):
        h,p=self.handoff(); del h['sources']['canonical:AGENTS.md']; self.assertIn('UNVERIFIED_HANDOFF_SOURCES',self.run_scan(role='team-defensive-auditor',handoff=h,handoff_plan=p)['issues'])
    def test_tampered_handoff_excerpt(self):
        h,p=self.handoff(); h['sources']['canonical:AGENTS.md']['text']='different'; self.assertIn('UNVERIFIED_HANDOFF_SOURCES',self.run_scan(role='team-defensive-auditor',handoff=h,handoff_plan=p)['issues'])
    def test_wrong_handoff_range(self):
        h,p=self.handoff(); p['canonical:AGENTS.md']=[[2,2]]; h['sources']['canonical:AGENTS.md']['ranges']=[[2,2]]; self.assertIn('UNVERIFIED_HANDOFF_SOURCES',self.run_scan(role='team-defensive-auditor',handoff=h,handoff_plan=p)['issues'])
    def test_wrong_manifest_path(self):
        self.manifest['coordinate-team']['path']='skills/team-engineering/SKILL.md'; self.assertIn('UNVERIFIED_ROLE_SKILL_BINDING',self.run_scan()['issues'])
    def test_wrong_manifest_plugin(self):
        self.manifest['coordinate-team']['plugin_id']=a.AUDITOR; self.assertIn('UNVERIFIED_ROLE_SKILL_BINDING',self.run_scan()['issues'])
    def test_probe_error(self):
        def fail(): raise RuntimeError('fixture')
        r=a.entry(self.args,fail); self.assertTrue(r['probe_called']); self.assertEqual(r['status'],'PROBE_FAILED'); self.assertIn('PROBE_EXCEPTION:RuntimeError',r['issues'])
    def test_dirty_worktree_commit_only(self):
        (self.root/'AGENTS.md').write_text('uncommitted'); r=self.run_scan(); self.assertEqual(r['status'],'LOCAL_INPUTS_VERIFIED'); self.assertFalse(r['authorization'])


    def cli_fixture(self):
        import json
        f=self.root/'tools/agent/auto_scan.py'
        f.parent.mkdir(parents=True,exist_ok=True)
        f.write_text('fixed read-only fixture\n')
        new=self.commit()
        bundle={k:v for k,v in self.args.items() if k not in ('root','target_root','skill_bytes')}
        bundle.update(expected=new,target_sha=new,skill_text=self.skill.decode())
        return bundle, new

    def call_cli(self,bundle):
        import json,sys
        f=self.root/'bundle.json'
        f.write_text(bundle if isinstance(bundle,str) else json.dumps(bundle))
        r=subprocess.run([sys.executable,a.__file__,'--canonical-root',str(self.root),
                          '--target-root',str(self.root),'--bundle',str(f)],
                         capture_output=True,text=True,timeout=30)
        return r.returncode,json.loads(r.stdout)

    def test_cli_executes_fixed_probe(self):
        bundle,new=self.cli_fixture()
        code,r=self.call_cli(bundle)
        self.assertEqual(code,0)
        self.assertTrue(r['probe_called'])
        self.assertEqual(r['probe_result'],a.blob(self.root,new,'tools/agent/auto_scan.py'))
        self.assertFalse(r['authorization'])
        self.assertFalse(r['remote_freshness_verified'])

    def test_cli_blocks_missing_skill_and_document(self):
        bundle,new=self.cli_fixture()
        code,r=self.call_cli(bundle|{'skill_text':''})
        self.assertEqual(code,1)
        self.assertFalse(r['probe_called'])
        self.assertIn('MISSING_OR_MISMATCHED_SKILL',r['issues'])
        (self.root/'bundle.json').unlink()
        (self.root/'AGENTS.md').unlink()
        new=self.commit()
        code,r=self.call_cli(bundle|{'expected':new,'target_sha':new})
        self.assertEqual(code,1)
        self.assertFalse(r['probe_called'])
        self.assertIn('MISSING_OR_INVALID:AGENTS.md',r['issues'])

    def test_cli_blocks_duplicate_keys_and_extra_fields(self):
        bundle,new=self.cli_fixture()
        for bad in ('{"role":"a","role":"b"}',bundle|{'command':'not allowed'}):
            with self.subTest(bad=type(bad).__name__):
                code,r=self.call_cli(bad)
                self.assertEqual(code,1)
                self.assertFalse(r['probe_called'])
                self.assertIn('INVALID_BUNDLE',r['issues'])

    def test_cli_probe_failure_is_nonzero(self):
        bundle,new=self.cli_fixture()
        (self.root/'bundle.json').unlink(missing_ok=True)
        (self.root/'tools/agent/auto_scan.py').unlink()
        new=self.commit()
        code,r=self.call_cli(bundle|{'expected':new,'target_sha':new})
        self.assertEqual(code,1)
        self.assertEqual(r['status'],'PROBE_FAILED')


if __name__=='__main__': unittest.main(verbosity=2)
