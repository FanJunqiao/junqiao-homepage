# Junqiao Fan · Academic homepage

A minimal academic homepage with rounded Nunito typography, white light mode, and charcoal dark mode. Titles are blue; active navigation, selected filters, and focused profile buttons use green. Subtle seafoam, lavender, and wheat venue colors retain the painting reference. Static HTML, CSS, and vanilla JavaScript; no browser-side dependencies. Opening `index.html` directly also works.

## Local preview

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open <http://127.0.0.1:8765>.

## Google Scholar citations

Papers with a positive citation count have a compact **Scholar N** badge on a separate row below the resource buttons, linking to the paper’s Google Scholar entry. Zero counts and not-yet-indexed papers have no badge. The tooltip records the last successful refresh. The catalog contains 9 selected papers, including mmHRI, GIVE, NeuralMUSIC, and SMamDiff. Four other Scholar entries were removed from the homepage at the owner’s request. The separately indexed mmDiff supplementary material is linked from its main paper.

- `scripts/sync_scholar.py`: makes one bounded request to the public Scholar profile, matches articles by their stable Scholar IDs (exact normalized title for initial mapping), and validates every indexed article and all author metrics before writing anything.
- `data/citations.json`: verified per-paper counts, source links, and timestamps.
- `data/metrics.json`: verified author-wide Scholar metrics. These are read directly from the profile’s statistics table.
- `.github/workflows/update-scholar.yml`: refreshes daily at **03:23 UTC / 11:23 China Standard Time**, on pushes to `main`, or manually via **Actions → Update Scholar citations and publish homepage → Run workflow**. GitHub may queue scheduled runs.

The workflow saves successful snapshots to the repository, regenerates the page, and deploys a Pages artifact in the same run. This explicit deployment ensures automated commits actually update the website; a commit made with `GITHUB_TOKEN` does not trigger another build workflow.

On HTTP 429, CAPTCHA, unexpected HTML, missing metrics, or an unmatched previously indexed article, the sync step fails visibly and retains the previous counts and timestamps. The site still builds from that snapshot. A valid empty Scholar citation cell means zero; a failed lookup never means zero. Only papers explicitly marked `scholarPending` may be absent from a valid profile. They begin syncing on an exact title match, and the cached Scholar ID is reused afterward. A pending paper does not prevent other papers from updating. No API key or paid service is required. This is a daily snapshot, not a live request from every visitor.

Manual refresh:

```sh
python3 -m pip install -r scripts/requirements.txt
python3 scripts/sync_scholar.py
python3 scripts/build.py
```

Regression checks:

```sh
python3 -m unittest discover -s tests -v
```

## Enable automatic updates and deployment

This local directory tracks `main` in `git@github.com:FanJunqiao/junqiao-homepage.git`.

1. Commit and push the website, including the hidden `.github/workflows/` directory and `.nojekyll`, to the homepage repository's `main` branch.
2. In **Settings → Pages → Build and deployment → Source**, select **GitHub Actions**.
3. Allow the workflow to write repository contents (the workflow requests `contents: write` to save verified snapshots). If repository or branch policies disallow bot pushes, those policies must allow this workflow.
4. Enable Actions if disabled, then run **Update Scholar citations and publish homepage** once.

The same workflow publishes the page after each citation refresh. A branch-only Pages configuration is sufficient for manually uploaded static files, but use the Actions configuration above for automatic citation updates.

## Content and maintenance

### CV compilation and website sync

Edit `Junqiao_Fan_Academic_CV_Template_fixed/Junqiao_Fan_Academic_CV_Template.tex`.
The CV includes seven selected publications, academic service, and skills.

```sh
python3 scripts/build_cv.py
```

This requires Python 3 and TeX Live/MacTeX with `latexmk`. Successful compilation
updates both the source-folder PDF and `assets/Junqiao_Fan_CV.pdf`, then versions
the CV link in `index.html` using the PDF's hash to avoid stale browser caches.
Failed compilation retains the previously published PDF. The local `.latexmkrc`
also runs this sync after direct `latexmk` builds. With the LaTeX Workshop extension,
the included `.vscode/settings.json` builds and syncs the CV whenever its source is saved.

Commit and push the resulting changes to update the public site; local compilation
does not automatically push commits. Original CV photos and LaTeX auxiliary files
are excluded from Git. No images are needed to compile the CV.

### Homepage content

The default **Selected first** order shows mmHRI, GIVE, M4Human, mmPred, and mmDiff in the first five entries of All. NeuralMUSIC remains in the expanded list. Newest/oldest sorting is still available. The selected order follows `data/publications.json`.

- `index.html`: biography, news, the combined **Education & Award** disclosure, and layout. Publication and metric blocks between named comments are generated; edit their data files instead.
- `data/publications.json`: all publications, category membership, links, Scholar IDs, venue colors, media provenance, and dated GitHub star snapshots. GitHub star counts are not refreshed by the Scholar script.
- `assets/style.css`: responsive styles and light/dark color tokens.
- `assets/theme.js`: applies the saved theme before the stylesheet loads, controls the header’s sun/moon switch, and remembers the choice locally. First-time visitors default to light mode, including when their system is dark. Switching still works when browser storage is blocked; without JavaScript the page remains light.
- `assets/app.js`: overlapping categories, search, sorting, five-paper preview / show-all behavior, citation dialogs, video previews, mobile navigation, and WeChat QR dialog.
- `assets/fonts/`: locally hosted Nunito and its OFL license.
- `assets/media/`: five compressed silent MP4 loops and their posters, paper figures, and the owner-provided full mmHRI demo. Short descriptions remain below image/video previews; right-side loop and figure-number labels are omitted.
- `assets/bib/`: individual and combined BibTeX downloads.
- Original portrait, CV, and QR code remain in `assets/`.

After editing publication data, run `python3 scripts/build.py`. This generator needs only the Python standard library; only the Scholar sync requires BeautifulSoup. It does not import extra publications automatically.

Filters cover Multimodal Human Sensing, Generative AI, Robotics, and Healthcare AI. Category memberships overlap; a paper appears in every assigned category. Each view initially shows the first five matching papers, with a Show all / Show fewer control. Filtering, searching, and sorting reset to five. Direct paper links reveal their target even outside the first five. Multimodal Human Sensing includes NeuralMUSIC as well as the radar papers. NeuralMUSIC and mmHRI also belong to Robotics; GIVE belongs to Robotics. mmHRI and GIVE are excluded from Generative AI. Video previews pause offscreen and respect reduced-motion preferences. Education & Award and Citation Statistics are collapsed by default. Core content, paper links, and BibTeX downloads work without JavaScript.

See [SOURCES.md](SOURCES.md) for research and media provenance.
