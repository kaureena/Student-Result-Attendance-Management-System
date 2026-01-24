# Releasing (tags + GitHub Release)

The goal is to publish a stable, reviewable version such as **v0.1.0**.

## Step 1 — Create and push the tag (command line)
From repo root:

```bash
git checkout main
git pull
git tag -a v0.1.0 -m "Baseline + Modernisation scaffold"
git push origin v0.1.0
```

## Step 2 — Create a GitHub Release (UI)
- Go to GitHub → **Releases** → **Draft a new release**
- Choose tag: `v0.1.0`
- Title: `v0.1.0 — Baseline + Modernisation scaffold`
- Paste release notes (see `RELEASE_NOTES_v0.1.0.md`)
- Publish release

GitHub will automatically provide “Source code (zip)” and “Source code (tar.gz)”.

## Optional — SHA256 checksum file
If you attach a custom release ZIP (or you download the GitHub source zip),
you can compute SHA256 on Windows:

```bat
certutil -hashfile <filename.zip> SHA256
```

Copy the hash into a file called `SHA256SUMS.txt` and upload it as a release asset.
