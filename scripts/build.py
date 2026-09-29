#!/usr/bin/env python3
"""Render publication data and metric snapshots into the static homepage.

No packages, bundler, network access, or server-side runtime required.
Run from anywhere: python3 scripts/build.py
"""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = json.loads((ROOT / 'data/publications.json').read_text())
METRICS = json.loads((ROOT / 'data/metrics.json').read_text())
CITATIONS_PATH = ROOT / 'data/citations.json'
CITATIONS = json.loads(CITATIONS_PATH.read_text()) if CITATIONS_PATH.exists() else {'publications': {}}
CATEGORIES = {'sensing': 'Multimodal Human Sensing', 'generative': 'Generative AI', 'robotics': 'Robotics', 'healthcare': 'Healthcare AI'}
ICONS = {
    'paper': '<path d="M14 3H5v18h14V8Zm0 0v5h5M8 12h8M8 16h6"/>',
    'scholar': '<path d="m2 9 10-6 10 6-10 6L2 9Zm4 3v5c3 3 9 3 12 0v-5M22 9v8"/>',
    'pdf': '<path d="M12 3v12m-4-4 4 4 4-4M5 17v4h14v-4"/>',
    'code': '<path d="m8 6-6 6 6 6m8-12 6 6-6 6M14 3l-4 18"/>',
    'website': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c5 5 5 13 0 18-5-5-5-13 0-18"/>',
    'video': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m10 9 5 3-5 3Z"/>',
    'bib': '<path d="M8 4H6c-2 0-2 2-2 4v1c0 2-1 3-2 3 1 0 2 1 2 3v1c0 2 0 4 2 4h2m8-16h2c2 0 2 2 2 4v1c0 2 1 3 2 3-1 0-2 1-2 3v1c0 2 0 4-2 4h-2"/>',
    'loop': '<path d="M20 7H7a5 5 0 0 0-5 5m2 5h13a5 5 0 0 0 5-5M16 3l4 4-4 4M8 13l-4 4 4 4"/>',
    'award': '<circle cx="12" cy="8" r="5"/><path d="m8 12-1 9 5-3 5 3-1-9"/>',
}

def icon(name):
    return '<svg aria-hidden="true" viewBox="0 0 24 24">' + ICONS[name] + '</svg>'

def bibtex(p):
    authors = []
    for name in p['authors']:
        given, family = name.rsplit(' ', 1)
        authors.append(f'{family}, {given}')
    fields = {'title': p['title'], 'author': ' and '.join(authors),
              'journal' if p['bibtype'] == 'article' else 'booktitle': p['booktitle'],
              'year': str(p['year'])}
    for key in ('volume', 'number', 'pages', 'doi'):
        if key in p:
            fields[key] = p[key]
    fields['url'] = p['paper']
    return '@' + p['bibtype'] + '{fan' + str(p['year']) + p['id'] + ',\n' + ''.join(
        '  ' + key + ' = {' + value + '},\n' for key, value in fields.items()) + '}\n'

def render_paper(p):
    for key in ('poster', 'preview'):
        if key in p and not (ROOT / p[key]).is_file():
            raise ValueError('Missing asset: ' + p[key])
    citation = bibtex(p)
    (ROOT / 'assets/bib' / (p['id'] + '.bib')).write_text(citation)
    authors = ', '.join('<strong>' + escape(a) + '</strong>' if a == 'Junqiao Fan' else escape(a) for a in p['authors'])
    links = []
    for kind, label in [('paper', 'Paper'), ('pdf', 'PDF'), ('code', p.get('codeLabel', 'Code')), ('website', 'Website'), ('video', 'Video'), ('supplement', 'Supplement')]:
        if p.get(kind):
            stars = ''
            if kind == 'code' and p.get('stars', 0):
                stars = f'<span class="stars" title="GitHub stars · {escape(p["starsChecked"])}">☆ {p["stars"]}</span>'
            links.append(f'<a class="pub-link {kind}-link" href="{escape(p[kind])}" target="_blank" rel="noopener noreferrer">{icon("paper" if kind == "supplement" else kind)}{escape(label)}{stars}</a>')
    links.append(f'<a class="pub-link bib-link" href="assets/bib/{p["id"]}.bib" download data-cite="{p["id"]}" aria-label="BibTeX for {escape(p["short"])}">{icon("bib")}BibTeX</a>')
    scholar = ''
    record = CITATIONS.get('publications', {}).get(p['id'])
    if record and isinstance(record.get('count'), int) and record['count'] > 0:
        scholar = f'<div class="pub-citations"><a class="pub-link citation-link" href="{escape(record["articleUrl"])}" target="_blank" rel="noopener noreferrer" title="Google Scholar · {record["count"]} citations · updated {escape(record["checked"])}" aria-label="Google Scholar: {record["count"]} citations for {escape(p["short"])}"><span class="scholar-label">{icon("scholar")}Scholar</span><span class="citation-count">{record["count"]}</span></a></div>'
    if 'preview' in p:
        video = f'<video data-src="{p["preview"]}" poster="{p["poster"]}" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video>'
        media_url = p['video']
        media_action = f'Watch the full {p["short"]} demo (opens in a new tab)'
    else:
        video = ''
        media_url = p['paper']
        media_action = f'Read {p["short"]} (opens in a new tab)'
    award_text = escape(p.get('award', ''))
    if p.get('awardUrl'):
        award_text = f'<a href="{escape(p["awardUrl"])}" target="_blank" rel="noopener noreferrer">{award_text}</a>'
    award = f'<p class="pub-award">{icon("award")}{award_text}</p>' if p.get('award') else ''
    media = f'''<figure class="pub-figure">
    <a class="pub-media" href="{escape(media_url)}" target="_blank" rel="noopener noreferrer" aria-label="{escape(media_action)}">
      <img src="{p['poster']}" alt="{escape(p['mediaLabel'])}" width="720" height="440" loading="lazy" decoding="async">{video}
    </a>
    <figcaption><span>{escape(p['mediaLabel'])}</span></figcaption>
  </figure>''' if p.get('poster') else f'<div class="pub-text-marker" aria-hidden="true"><span>{p["year"]}</span>{icon("paper")}</div>'
    topics = ' · '.join(CATEGORIES[x] for x in p['categories'])
    search = ' '.join([p['short'], p['title'], p['venue'], str(p['year']), ' '.join(p['authors']), p['summary'], topics]).lower()
    return f'''<article class="publication" id="{p['id']}" data-year="{p['year']}" data-categories="{' '.join(p['categories'])}" data-search="{escape(search)}" aria-labelledby="{p['id']}-title">
  {media}
  <div class="pub-body">
    <div class="pub-topline"><p class="pub-venue" data-tone="{escape(p.get('venueTone', 'blue'))}">{escape(p['venue'])}</p><span class="pub-topic">{topics}</span></div>
    <h3 id="{p['id']}-title"><a href="{escape(p['paper'])}" target="_blank" rel="noopener noreferrer">{escape(p['title'])}</a></h3>
    <p class="pub-authors">{authors}</p>
    <p class="pub-summary">{escape(p['summary'])}</p>{award}
    <div class="pub-links">{''.join(links)}</div>
    {scholar}
    <template class="bibtex">{escape(citation)}</template>
  </div>
</article>'''

def replace_block(html, block, content):
    pattern = r'(<!-- ' + block + r':START -->).*?(<!-- ' + block + r':END -->)'
    result, count = re.subn(pattern, lambda m: m[1] + '\n' + content + '\n      ' + m[2], html, flags=re.S)
    if count != 1:
        raise ValueError('Expected exactly one ' + block + ' block')
    return result

assert len({p['id'] for p in PAPERS}) == len(PAPERS), 'Duplicate publication ID'
(ROOT / 'assets/bib').mkdir(exist_ok=True)
rows = '\n'.join(line.rstrip() for p in PAPERS for line in render_paper(p).splitlines())
(ROOT / 'assets/bib/selected-publications.bib').write_text('\n'.join(bibtex(p) for p in PAPERS))
values = [(len(PAPERS), 'Publications'), (METRICS['citations'], 'Citations'), (METRICS['hIndex'], 'h-index'), (METRICS['i10Index'], 'i10-index')]
stats = '<div class="stats-grid">' + ''.join(f'<div class="stat"><span class="stat-number">{n}</span><span class="stat-label">{label}</span></div>' for n, label in values) + '</div>'
stats += f'<p class="stats-note">Author-wide citation metrics · <a href="{escape(METRICS["url"])}" target="_blank" rel="noopener noreferrer">{escape(METRICS["source"])} snapshot</a> · <time datetime="{METRICS["checked"]}">{METRICS["checked"]}</time></p>'
stats = '<details class="stats-disclosure"><summary>Citation Statistics<span class="disclosure-icon" aria-hidden="true"></span></summary><div class="stats-content">' + stats + '</div></details>'
index = ROOT / 'index.html'
html = replace_block(index.read_text(), 'PUBLICATIONS', rows)
html = replace_block(html, 'METRICS', stats)
html = re.sub(r'(<span data-count="([a-z]+)">)\d+(</span>)',
              lambda m: m[1] + str(sum(m[2] == 'all' or m[2] in p['categories'] for p in PAPERS)) + m[3], html)
html = re.sub(r'(<p id="publication-count"[^>]*>).*?(</p>)',
              lambda m: m[1] + f'{len(PAPERS)} publications' + m[2], html)
index.write_text(html)
print(f'Built {len(PAPERS)} publications, citations, and dated metrics. No runtime dependencies.')
