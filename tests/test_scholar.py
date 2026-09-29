"""Regression checks for the citation sync, especially unavailable vs zero counts."""
from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import sync_scholar as sync

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'tests/fixtures/scholar-profile.html').read_text()
ALL_PAPERS = json.loads((ROOT / 'data/publications.json').read_text())
PAPERS = [p for p in ALL_PAPERS if p['id'] in {'m4human', 'mmpred', 'mmdiff', 'distillation', 'iomt'}]
CHECKED = '2026-09-29T00:00:00Z'


class ScholarTests(unittest.TestCase):
    def test_full_catalog_and_pending_preprint(self):
        citations, _ = sync.parse_profile(HTML, ALL_PAPERS, CHECKED)
        self.assertEqual(len(citations['publications']), 8)
        self.assertNotIn('mmhri', citations['publications'])
        self.assertEqual(citations['publications']['give']['count'], 1)
        self.assertEqual(citations['publications']['neuralmusic']['count'], 0)
        self.assertEqual(citations['publications']['smamdiff']['count'], 1)

    def test_pending_paper_starts_syncing_when_indexed(self):
        pending = next(p for p in ALL_PAPERS if p['id'] == 'mmhri')
        soup = BeautifulSoup(HTML, 'html.parser')
        row = soup.select_one('.gsc_a_tr')
        row.select_one('.gsc_a_at').string = pending['title']
        citations, _ = sync.parse_profile(str(soup), [pending], CHECKED)
        self.assertEqual(citations['publications']['mmhri']['count'], 43)

    def test_indexed_pending_paper_keeps_stable_id(self):
        pending = next(p for p in ALL_PAPERS if p['id'] == 'mmhri')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data').mkdir()
            (root / 'data/publications.json').write_text(json.dumps([pending]))
            (root / 'data/citations.json').write_text(json.dumps({'publications': {
                'mmhri': {'scholarId': '5cEG4tIAAAAJ:zYLM7Y9cAGgC'}}}))
            with patch.object(sync, 'ROOT', root), patch.object(sync, 'fetch_profile', return_value=HTML), \
                    patch.object(sys, 'argv', ['sync_scholar.py']), redirect_stdout(io.StringIO()):
                self.assertEqual(sync.main(), 0)
            cache = json.loads((root / 'data/citations.json').read_text())
            self.assertEqual(cache['publications']['mmhri']['count'], 43)

    def test_selected_papers_and_real_zero(self):
        citations, metrics = sync.parse_profile(HTML, PAPERS, CHECKED)
        self.assertEqual({k: v['count'] for k, v in citations['publications'].items()},
                         {'m4human': 11, 'mmpred': 9, 'mmdiff': 43, 'distillation': 0, 'iomt': 42})
        self.assertEqual(metrics['citations'], 111)
        self.assertEqual(metrics['hIndex'], 4)
        self.assertEqual(metrics['i10Index'], 3)
        self.assertEqual(metrics['source'], 'Google Scholar')
        zero = citations['publications']['distillation']
        self.assertEqual(zero['citedByUrl'], zero['articleUrl'])
        self.assertIn('cites=', citations['publications']['mmdiff']['citedByUrl'])

    def test_exact_titles_do_not_match_supplementary_material(self):
        papers = [{k: v for k, v in p.items() if k != 'scholarId'} for p in PAPERS]
        citations, _ = sync.parse_profile(HTML, papers, CHECKED)
        self.assertEqual(citations['publications']['mmdiff']['count'], 43)
        soup = BeautifulSoup(HTML, 'html.parser')
        for row in soup.select('.gsc_a_tr'):
            if row.select_one('.gsc_a_at')['href'].endswith('zYLM7Y9cAGgC'):
                row.decompose()
        with self.assertRaises(ValueError):
            sync.parse_profile(str(soup), papers, CHECKED)

    def test_stable_id_survives_title_update(self):
        modified = HTML.replace('M4human: A large-scale', 'M4Human: Updated large-scale')
        citations, _ = sync.parse_profile(modified, PAPERS, CHECKED)
        self.assertEqual(citations['publications']['m4human']['count'], 11)

    def test_unavailable_html_is_not_zero(self):
        for html in ['<html>Too many requests</html>', '<html>CAPTCHA</html>',
                     HTML.replace('Junqiao Fan', 'Different Author')]:
            with self.assertRaises(ValueError):
                sync.parse_profile(html, PAPERS, CHECKED)

    def test_missing_and_malformed_counts_are_rejected(self):
        soup = BeautifulSoup(HTML, 'html.parser')
        soup.select_one('.gsc_a_ac').decompose()
        with self.assertRaises(ValueError):
            sync.parse_profile(str(soup), PAPERS, CHECKED)
        soup = BeautifulSoup(HTML, 'html.parser')
        soup.select_one('.gsc_a_ac').string = 'Unavailable'
        with self.assertRaises(ValueError):
            sync.parse_profile(str(soup), PAPERS, CHECKED)
        soup.select_one('.gsc_a_ac').string = ''
        with self.assertRaises(ValueError):
            sync.parse_profile(str(soup), PAPERS, CHECKED)

    def test_missing_author_metrics_are_rejected(self):
        soup = BeautifulSoup(HTML, 'html.parser')
        soup.select_one('#gsc_rsb_st').decompose()
        with self.assertRaises(ValueError):
            sync.parse_profile(str(soup), PAPERS, CHECKED)

    def test_rate_limit_leaves_cache_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data').mkdir()
            (root / 'data/publications.json').write_text(json.dumps(PAPERS))
            for name in ['citations', 'metrics']:
                (root / f'data/{name}.json').write_text('{"existing":42}')
            error = HTTPError(sync.PROFILE, 429, 'Too many requests', {}, None)
            with patch.object(sync, 'ROOT', root), patch.object(sync, 'fetch_profile', side_effect=error), \
                    patch.object(sys, 'argv', ['sync_scholar.py']), redirect_stderr(io.StringIO()):
                self.assertEqual(sync.main(), 1)
            for name in ['citations', 'metrics']:
                self.assertEqual((root / f'data/{name}.json').read_text(), '{"existing":42}')

    def test_success_updates_both_cached_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data').mkdir()
            (root / 'data/publications.json').write_text(json.dumps(PAPERS))
            with patch.object(sync, 'ROOT', root), patch.object(sync, 'fetch_profile', return_value=HTML), \
                    patch.object(sys, 'argv', ['sync_scholar.py']), redirect_stdout(io.StringIO()):
                self.assertEqual(sync.main(), 0)
            cache = json.loads((root / 'data/citations.json').read_text())
            metrics = json.loads((root / 'data/metrics.json').read_text())
            self.assertEqual(cache['publications']['iomt']['count'], 42)
            self.assertEqual(cache['checked'], metrics['checked'])


if __name__ == '__main__':
    unittest.main()
