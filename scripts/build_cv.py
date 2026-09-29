#!/usr/bin/env python3
"""Compile the CV and synchronize the website PDF after a successful build."""
import argparse
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent
CV_DIR = ROOT / 'Junqiao_Fan_Academic_CV_Template_fixed'
SOURCE = CV_DIR / 'Junqiao_Fan_Academic_CV_Template.tex'
WEBSITE_PDF = ROOT / 'assets/Junqiao_Fan_CV.pdf'


def sync_pdf(pdf):
    data = pdf.read_bytes()
    if not data.startswith(b'%PDF-') or b'%%EOF' not in data[-1024:]:
        raise ValueError(f'Not a complete PDF: {pdf}')
    page = ROOT / 'index.html'
    html = page.read_text()
    version = hashlib.sha256(data).hexdigest()[:12]
    updated, count = re.subn(
        r'href="assets/Junqiao_Fan_CV\.pdf(?:\?[^"<>]*)?"',
        f'href="assets/Junqiao_Fan_CV.pdf?v={version}"', html)
    if count != 1:
        raise ValueError('Expected exactly one CV download link in index.html')
    for target in (SOURCE.with_suffix('.pdf'), WEBSITE_PDF):
        if target.exists() and target.read_bytes() == data:
            continue
        # Readers never see a partly copied PDF.
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as temp:
            temp.write(data)
            name = Path(temp.name)
        name.chmod(0o644)
        name.replace(target)
    if updated != html:
        page.write_text(updated)
    print(f'Website CV updated: assets/Junqiao_Fan_CV.pdf?v={version}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sync', type=Path, help='Sync a successfully compiled PDF (latexmk hook)')
    args = parser.parse_args()
    if args.sync:
        sync_pdf(args.sync.resolve())
        return
    env = os.environ.copy()
    env['PATH'] = '/Library/TeX/texbin' + os.pathsep + env.get('PATH', '')
    latexmk = shutil.which('latexmk', path=env['PATH'])
    if not latexmk:
        raise SystemExit('latexmk is required. Install TeX Live or MacTeX, then rerun this command.')
    subprocess.run(
        [latexmk, '-pdf', '-interaction=nonstopmode', '-halt-on-error', SOURCE.name],
        cwd=CV_DIR, env=env, check=True)
    sync_pdf(SOURCE.with_suffix('.pdf'))


if __name__ == '__main__':
    main()
