# Setup guide

This folder is everything for your `black-bird7/black-bird7` profile repo:
a neofetch-style animated header (built from your photo) sitting on top of
the polished sections from your current README.

## 1. Personalize the placeholder fields

`render_svg.py` has a `STATIC_LINES` list near the top with the info-panel
content (OS, shell, editor, focus areas, contact). Three lines are
generic placeholders — edit them to match reality, then re-run the render
step (step 4) to bake the changes in:

```python
("kv", "OS", "Arch Linux / Kali Linux"),   # <- your actual OS(es)
("kv", "Shell", "zsh"),                     # <- your actual shell
("kv", "Editor", "Neovim, VS Code"),        # <- your actual editor(s)
```

Everything else (languages, focus areas, contact info) was pulled directly
from your existing README, so it should already be accurate.

## 2. Drop these files into your repo

Copy everything in this folder — `README.md`, `light_mode.svg`,
`dark_mode.svg`, `today.py`, `.github/workflows/build.yaml`, and
`cache/` — into the root of `black-bird7/black-bird7`, keeping the
folder structure intact.

## 3. Add the repo secret

Create a **fine-grained Personal Access Token** with:

- Account permissions: `read:Followers`, `read:Starring`, `read:Watching`
- Repository permissions (all repos): `read:Commit statuses`,
  `read:Contents`, `read:Issues`, `read:Metadata`, `read:Pull Requests`

Add it to the repo as a secret named **`ACCESS_TOKEN`**
(Settings → Secrets and variables → Actions → New repository secret).

## 4. Rebuild ASCII art from a different photo (optional)

If you want to regenerate the portrait — a different photo, a tighter
crop, a wider/narrower grid — run:

```bash
pip install pillow opencv-python-headless numpy
python build_ascii_art.py your_photo.jpg --cols 60 > ascii_lines.txt
python render_svg.py
```

This overwrites `light_mode.svg` and `dark_mode.svg` with the new art
(GitHub stats fields reset to placeholder `0`s — the next Actions run
fills them back in).

## 5. Trigger the first build

Push to `main`, or run the **"README build"** workflow manually from the
Actions tab. It fetches your live repo/star/commit/follower/LOC counts
and commits the updated SVGs — and re-runs daily after that.

## Notes

- The "GitHub Member Since" field is computed from your account's real
  creation date via the API — not invented.
- Lines-of-code counting clones every owned repo's default branch and
  walks its full commit history, so the first run can take a while on
  an account with a lot of repos. Cached per-repo commit counts (in
  `cache/`) make subsequent runs fast — only repos with new commits get
  re-walked.
