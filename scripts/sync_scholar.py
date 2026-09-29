#!/usr/bin/env python3
"""Refresh publication citations from one public Google Scholar profile request.

Only a fully validated response replaces cached data. Errors, rate limits,
CAPTCHAs, ambiguous matches, and missing papers leave the previous snapshot intact.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
AUTHOR = '5cEG4tIAAAAJ'
PROFILE = 'https://scholar.google.com/citations?' + urlencode(
    {'user': AUTHOR, 'hl': 'en', 'pagesize': 100})


def normalize_title(value):
    return ''.join(c for c in unicodedata.normalize('NFKC', value).casefold() if c.isalnum())


def count_value(text):
    value = text.strip().replace(',', '').replace('\u00a0', '')
    if not re.fullmatch(r'\d+\*?', value):
        raise ValueError('Invalid citation count')
    return int(value.rstrip('*'))


def scholar_url(href):
    url = urljoin('https://scholar.google.com', href)
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.hostname != 'scholar.google.com':
        raise ValueError('Unexpected Scholar link')
    return url


def parse_profile(html, papers, checked):
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.select_one('#gsc_prf_in')
    if not name or normalize_title(name.get_text()) != 'junqiaofan':
        raise ValueError('Scholar profile unavailable or unexpected author; cached counts retained')
    rows = soup.select('.gsc_a_tr')
    if not rows:
        raise ValueError('No Scholar publication rows; cached counts retained')
    articles = []
    for row in rows:
        title = row.select_one('.gsc_a_at')
        if not title:
            continue
        url = scholar_url(title.get('href', ''))
        identifier = parse_qs(urlparse(url).query).get('citation_for_view', [''])[0]
        if not identifier.startswith(AUTHOR + ':'):
            raise ValueError('Article belongs to another profile')
        articles.append((identifier, title.get_text(' ', strip=True), row, url))

    selected = {}
    for paper in papers:
        expected = paper.get('scholarId')
        if expected:
            matches = [a for a in articles if a[0] == expected]
        else:
            matches = [a for a in articles if normalize_title(a[1]) == normalize_title(paper['title'])]
        if not matches and not expected and paper.get('scholarPending'):
            # A newly released, explicitly pending preprint is not an uncited paper.
            # It starts syncing automatically when its exact title is indexed.
            continue
        if len(matches) != 1:
            raise ValueError(f'Expected one exact Scholar match for {paper["id"]}; found {len(matches)}')
        identifier, title, row, url = matches[0]
        cell = row.select_one('.gsc_a_ac')
        if cell is None:
            raise ValueError(f'Missing citation cell for {paper["id"]}')
        text = cell.get_text(strip=True)
        href = cell.get('href', '').strip()
        # Scholar represents an uncited article by an empty, linkless count cell.
        # A missing/malformed count is never converted to zero.
        count = count_value(text) if text else 0
        if not text and href:
            raise ValueError(f'Empty count with a citation link for {paper["id"]}')
        selected[paper['id']] = {
            'scholarId': identifier, 'title': title, 'count': count,
            'articleUrl': url, 'citedByUrl': scholar_url(href) if href else url,
            'checked': checked,
        }

    metrics = {}
    labels = {'Citations': 'citations', 'h-index': 'hIndex', 'i10-index': 'i10Index'}
    for row in soup.select('#gsc_rsb_st tr'):
        cells = row.select('td')
        if len(cells) < 2:
            continue
        label = cells[0].get_text(' ', strip=True)
        if label in labels:
            metrics[labels[label]] = count_value(cells[1].get_text(strip=True))
    if set(metrics) != set(labels.values()):
        raise ValueError('Missing author-wide Scholar metrics; cached counts retained')
    return {
        'source': 'Google Scholar', 'profileUrl': PROFILE, 'authorId': AUTHOR,
        'checked': checked, 'publications': selected,
    }, {
        'source': 'Google Scholar', 'url': PROFILE, 'checked': checked,
        **metrics, 'scope': 'Author-wide Google Scholar metrics.',
    }


def fetch_profile():
    request = Request(PROFILE, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en'})
    # A single bounded request per run. No CAPTCHA bypass or retry loop.
    with urlopen(request, timeout=30) as response:
        return response.read(5_000_000).decode('utf-8')


def save_json(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html', type=Path, help='Import an already downloaded Scholar profile HTML')
    args = parser.parse_args()
    papers = json.loads((ROOT / 'data/publications.json').read_text())
    try:
        cache_path = ROOT / 'data/citations.json'
        cached = json.loads(cache_path.read_text()).get('publications', {}) if cache_path.exists() else {}
        for paper in papers:
            # Once a pending paper is indexed, remember its stable Scholar ID.
            if not paper.get('scholarId') and cached.get(paper['id'], {}).get('scholarId'):
                paper['scholarId'] = cached[paper['id']]['scholarId']
        html = args.html.read_text() if args.html else fetch_profile()
        checked = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
        citations, metrics = parse_profile(html, papers, checked)
    except (HTTPError, URLError, ValueError, TimeoutError, OSError) as error:
        print(f'Scholar sync unavailable: {error}. Previous data was not changed.', file=sys.stderr)
        return 1
    # Validate the entire result before either write. Keep identity mapping stable.
    save_json(ROOT / 'data/citations.json', citations)
    save_json(ROOT / 'data/metrics.json', metrics)
    print('Google Scholar citations: ' + ', '.join(f'{key}={p["count"]}' for key, p in citations['publications'].items()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
