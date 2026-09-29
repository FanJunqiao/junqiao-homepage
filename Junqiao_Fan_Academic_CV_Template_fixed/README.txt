This text-only academic CV uses pdfLaTeX and the homepage blue (#294F7D).

From the website root, run:
  python3 scripts/build_cv.py

With VS Code's LaTeX Workshop extension, saving the .tex file compiles it
and updates assets/Junqiao_Fan_CV.pdf automatically. The local .latexmkrc
also syncs successful latexmk builds, including builds to another output folder.
Failed compilations retain the website's previous PDF. Each successful update
versions the CV link in index.html so visitors receive the new PDF after deployment.

Commit and push the updated source, PDF, assets/Junqiao_Fan_CV.pdf and index.html
to publish. Compilation does not push to GitHub automatically.

On Overleaf, select pdfLaTeX. Download the compiled PDF and sync it locally with:
  python3 scripts/build_cv.py --sync /path/to/downloaded.pdf
