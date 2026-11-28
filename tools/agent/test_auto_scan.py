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
        self.git('add','.'); self.git('commit','-qm','baseline'); self.sha=a.ref(self.root,'HEAD'); self.skill=b'test skill\n'
        self.args=dict(root=self.root,canonical_ref='HEAD',expected=self.sha,role='coordinate-team',skill_bytes=self.skill,skill_sha256=hashlib.sha256(self.skill).hexdigest(),target_root=self.root,target_ref='HEAD',target_sha=self.sha,task_id='QA-TEST')
    def git(self,*args): return a.git(self.root,*args)
    def run_scan(self,**kwargs): return a.scan(**(self.args|kwargs))
    def commit(self): self.git('add','-A'); self.git('commit','-qm','change'); return a.ref(self.root,'HEAD')
    def test_all_17_role_entries(self):
        for role in a.ROLES:
            with self.subTest(role=role):
                handoff=dict(task_id='QA-TEST',target_sha=self.sha,canonical_sha=self.sha,scope='fixture',redacted_content='rules',source_locator='fixture') if role in a.AUDITORS else None
                calls=[]; result=a.entry(self.args|dict(role=role,handoff=handoff),lambda: calls.append('probe'))
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

if __name__=='__main__': unittest.main(verbosity=2)
