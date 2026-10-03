# Lokendra Sonwani — GitHub Profile UI

This version matches the supplied neon terminal reference more closely while keeping **live GitHub contribution/stat extraction**.

## What is included

- Neon cyan/green terminal header
- Green `Learning | Building | Improving ...` line + cursor
- Live profile-views badge
- Contribution **table only** (no snake)
- Neon `whoami` two-panel layout
- Live GitHub stats with contributions, commits, PRs, issues, stars and streaks
- Pink/cyan/green reference-style stats colors
- Tech-stack panel
- GitHub + LinkedIn connect buttons
- Neon wave footer with `Learn. Build. Break. Fix. Repeat.`
- GitHub Actions + GraphQL data refresh

## Update your existing profile repository

Do **not** delete or recreate `lokendra-s64/lokendra-s64`.

1. Replace the repository files with this package.
2. Keep the repository public.
3. Open **Actions**.
4. Run **Update GitHub profile stats** with **Run workflow**.
5. Wait for the green checkmark.
6. Open your profile and press `Ctrl + F5`.

The workflow uses GitHub's built-in `GITHUB_TOKEN`; no separate API key is required.

## Live data flow

`fetch_contributions.py` → `data/contributions.json` → contribution table + stats card.

The workflow refreshes automatically on the schedule in `.github/workflows/update-profile-art.yml` and can also be started manually.
