# Research sources and media

Verified on **2026-09-29**. The original `index.html` supplied the five selected papers and personal information. The catalog now contains 9 selected papers after the owner requested removing From Radar to Depth, the myocardial infarction / osteoporosis study, Adaptive-gradient federated learning, and Smartphone hypertension detector. mmDiff’s supplementary entry is linked from the main paper rather than counted twice.

## Design reference

[Gen Li's homepage](https://www.genli.top/) informed the compact academic layout, topic filters, paper resources, and looped previews. The page styling and interaction code here are original; no reference-site assets were copied.

## Publications

| Paper | Article / PDF | Code | Project / media |
| --- | --- | --- | --- |
| M4Human | [CVPR proceedings](https://openaccess.thecvf.com/content/CVPR2026/html/Fan_M4Human_A_Large-Scale_Multimodal_mmWave_Radar_Benchmark_for_Human_Mesh_CVPR_2026_paper.html), [arXiv 2512.12378](https://arxiv.org/abs/2512.12378) | [M4Human](https://github.com/FanJunqiao/M4Human) | [Official project](https://fanjunqiao.github.io/M4Human-site/) |
| mmPred | [AAAI proceedings](https://ojs.aaai.org/index.php/AAAI/article/view/37378), [arXiv 2512.00345](https://arxiv.org/abs/2512.00345) | [mmPred](https://github.com/FanJunqiao/mmPred) | [Official project](https://fanjunqiao.github.io/mmPred-site/) |
| mmDiff | [arXiv 2403.16198](https://arxiv.org/abs/2403.16198), [ECCV PDF](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/02408.pdf) | [mmDiff](https://github.com/FanJunqiao/mmDiff) | [Official project](https://fanjunqiao.github.io/mmDiff-site/) |
| Generative Dataset Distillation Using Min-Max Diffusion Model | [arXiv 2503.18626](https://arxiv.org/abs/2503.18626), [Publisher](https://doi.org/10.1007/978-3-031-93806-1_5) | [Author's competition implementation](https://github.com/FanJunqiao/DD_Track2) | [Paper figure](https://arxiv.org/html/2503.18626v1/main.png) |
| Federated Learning Driven Secure Internet of Medical Things | [Publisher DOI](https://doi.org/10.1109/MWC.008.00475) | No verified public repository found | No verified project site or video found |

The dataset distillation repository identifies itself as the author's ECCV 2024 Track 2 competition implementation and references the preceding Minimax Diffusion work. It is labeled **Competition code**, not represented as a new standalone project site.

Publication years follow the proceedings / original selection rather than arXiv upload dates: M4Human and mmPred are 2026; mmDiff and the ECCV workshop paper are 2024. The workshop arXiv manuscript was uploaded in 2025.

The IoMT title and DOI were also confirmed against [Crossref publisher metadata](https://api.crossref.org/works/10.1109/MWC.008.00475). M4Human final pages (42836–42846) and authors were verified on the official CVPR page.

## Media provenance

| Local asset | Original source | Transformation |
| --- | --- | --- |
| `m4human-loop.mp4` | [M4Human action demo](https://fanjunqiao.github.io/M4Human-site/static/dataset_videos/combined_output_depth_43.mp4) | 1–9 seconds, 720px wide, 20fps, muted H.264 |
| `mmpred-loop.mp4` | [mmPred demo](https://fanjunqiao.github.io/mmPred-site/static/videos/demo_small.mp4) | 3–11 seconds, trimmed letterbox, 720px wide, 20fps, muted H.264 |
| `mmdiff-loop.mp4` | [mmDiff demo](https://fanjunqiao.github.io/mmDiff-site/static/videos/mmDiff%20site.mp4) | 3–11 seconds, trimmed letterbox, 720px wide, 20fps, muted H.264 |
| `*-poster.webp` | Corresponding local loop | First frame |
| `distillation.webp` | Figure in the [author's arXiv manuscript](https://arxiv.org/html/2503.18626v1/main.png) | Resized WebP |
| `iomt-fig1.webp` | Figure 1, “System architecture of FLDIoMT,” from the owner-provided `Desktop/Federated_Learning_Driven_Secure_Internet_of_Medical_Things.pdf`, PDF page 2 / printed page 69 | Extracted figure area from the PDF and encoded as a 1400px-wide WebP; original figure colors retained |

The project sites credit the authors and state CC BY-NC 4.0 for the research assets; the linked project pages retain their full license notices. These excerpts are displayed on the author's academic homepage with original-demo links. The portrait, CV, and QR code came from the original workspace.

## Statistics

The original Google Scholar request returned HTTP 429, so an alphaXiv snapshot was initially used. A subsequent successful read of the [Google Scholar profile](https://scholar.google.com/citations?user=5cEG4tIAAAAJ&hl=en&pagesize=100) on 2026-09-29 replaced it with direct Scholar data: **111 citations**, **h-index 4**, and **i10-index 3**. These are author-wide metrics.

The five selected articles were matched by exact titles and their stable Scholar article IDs. The first successful direct snapshot contained M4Human **11**, mmPred **9**, mmDiff **43**, Dataset Distillation **0**, and Federated Learning **42** citations. Current values and retrieval timestamps live in `data/citations.json` and `data/metrics.json` and are updated by `scripts/sync_scholar.py`.

The daily workflow uses GitHub's [custom Pages workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) deployment mechanism. It explicitly deploys in the same run because [events created with GITHUB_TOKEN do not trigger another push workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow). It is configured locally and must be enabled in the published repository before scheduled execution can occur.

GitHub's public API on 2026-09-29 reported 61 stars for M4Human, 29 for mmDiff, 6 for mmPred, and 0 for DD_Track2. These star badges remain separately dated snapshots in `data/publications.json`.

## Typography and competition link

The rounded sans-serif typography uses locally hosted [Nunito](https://fonts.google.com/specimen/Nunito), distributed under the SIL Open Font License in `assets/fonts/OFL.txt`. This follows the reference homepage’s sans-serif typography with a rounder appearance.

Dataset Distillation Challenge mentions link to the [CodaLab competition](https://codalab.lisn.upsaclay.fr/competitions/19577) specified by the owner.


## Expanded catalog (2026-09-29)

| Added work | Verified article / metadata | Additional resources |
| --- | --- | --- |
| mmHRI | [arXiv 2609.34220](https://arxiv.org/abs/2609.34220) | [Author code](https://github.com/FanJunqiao/mmHRI); full demo from `Desktop/mmHRI-site-main/mmhri.mp4` |
| GIVE | [arXiv 2606.13435](https://arxiv.org/abs/2606.13435) | [Official project](https://luis-cloud-sg.github.io/GIVE-project/) and its real-world demo; the project lists code as “Soon”, so no code button is shown |
| NeuralMUSIC | [arXiv 2606.18664](https://arxiv.org/abs/2606.18664) | Figure 1 from [arXiv HTML](https://arxiv.org/html/2606.18664v1/fig/intro.png) |
| SMamDiff | [arXiv 2512.00355](https://arxiv.org/abs/2512.00355), [publisher DOI](https://doi.org/10.1109/CloudCom67567.2025.11331341) | [Architecture figure](https://arxiv.org/html/2512.00355v1/main.png) |

The mmDiff [Supplement PDF](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/02408-supp.pdf) was verified through the [official ECVA page](https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/2408_ECCV_2024_paper.php). No separate publication card is generated for it.

New media: `mmhri-loop.mp4` excerpts 53–61 seconds of the owner’s full demo; `give-loop.mp4` excerpts 3–11 seconds of the [official real-world demo](https://luis-cloud-sg.github.io/GIVE-project/static/videos/real_world/real-time%20experiments.mp4). Both are muted H.264, 720px wide, 20fps. Their posters are the first frames. `neuralmusic.webp` and `smamdiff.webp` are resized original paper figures. Papers without a verified image or demo use a compact text presentation. The mmHRI project URL initially returned 404. The owner subsequently supplied [the project website](https://fanjunqiao.github.io/mmHRI-site/), which is now linked from the mmHRI Website button. The full owner-provided demo remains hosted locally. `mamba_pred` retains an unrelated baseline README, so it is not presented as verified SMamDiff code.

At the owner’s request, the sensing category is named Multimodal Human Sensing. mmHRI and NeuralMUSIC belong to both Multimodal Human Sensing and Robotics; GIVE belongs to Robotics. mmHRI and GIVE are excluded from Generative AI. The mmPred and mmDiff sensing / generative overlaps remain intact.

The selected catalog matches 8 indexed main papers in the Scholar snapshot. Author-wide citation statistics still reflect the full Scholar profile. mmHRI is explicitly pending indexing, so its citation badge stays absent until an exact title match becomes available. All zero-count citation badges are hidden. The list displays five matches initially and can expand to all matches; counts are unique papers, not sums of overlapping categories.


## Current color palette and theme switch

At the owner’s request, the interface defaults to pure white light mode (`#ffffff`) with blue headings (`#294f7d`) and green selected controls (`#31664d`). Dark mode uses a charcoal background (`#151c24`), pale blue headings (`#a6c5ed`), and pale green selections (`#91c7a7`). Body text keeps a subtle green tint with enough contrast in both modes. The [Gen Li homepage](https://www.genli.top/) is the interaction reference for the light/dark switch; the implementation is local and independent. A sun/moon button in the header switches modes and remembers the choice. The original painting remains the color reference for the seafoam, lavender, and wheat badge backgrounds. ECCV and ECCV Workshops continue to share one color.

The postdoctoral contact pill and arXiv badges use the blue background, border, and text palette in both light and dark modes, following the owner’s latest preference.

Scholar badges follow the reference homepage’s separate badge row: **Scholar + count** below the resource links, linking to each paper’s Scholar entry. Citation counts still come from the verified snapshot, and zero or unknown counts remain hidden. The bulk “Download all citations” link has been removed; individual BibTeX links remain.

## Biography update

The final-year Ph.D. status, expected graduation by December 2026, IoT / MARS supervision, PolyU degree and mathematics minor, and research interests were supplied by the owner. The school name is normalized to School of Electrical and Electronic Engineering. Prof. Lihua Xie’s title is written as “Fellow of the Academy of Engineering Singapore,” consistent with his [official DDCLS 2026 speaker biography](https://ddcls26.jsu.edu.cn/Lihua_Xie.html) and the biography in an [NTU-hosted research paper](https://personal.ntu.edu.sg/xlli/publication/TAI.pdf).

## News month labels

News entries use year followed by the abbreviated month and machine-readable `YYYY-MM` values. Acceptance months are inferred from the official conference notification schedules, rather than personal announcement timestamps: M4Human — **Feb 2026** ([CVPR final decisions: February 20](https://cvpr.thecvf.com/Conferences/2026/Dates)); mmPred — **Nov 2025** ([AAAI-26 final notifications: November 8, 2025](https://aaai.org/conference/aaai/aaai-26/)); mmDiff — **Jul 2024** ([ECCV decisions: July 1](https://eccv.ecva.net/Conferences/2024/Dates)). The Dataset Distillation award is placed in **Sep 2024**, using the workshop month in the [official ECCV workshop program](https://media.eventhosts.cc/Conferences/ECCV2024/ECCV2024WorkshopPDF.pdf), not claiming an independently verified award-email date. News rows are ordered from newest to oldest.

The owner confirmed NeuralMUSIC as the paper whose venue should be updated to **IROS 2026**. Its venue badge and BibTeX conference information reflect that update; the arXiv paper and PDF links are retained.
