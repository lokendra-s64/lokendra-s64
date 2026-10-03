# Lokendra Sonwani — GitHub Profile Setup

## Live data

The workflow uses GitHub Actions' built-in `GITHUB_TOKEN` and the GitHub GraphQL API to refresh:

- contribution calendar / heatmap
- total contributions
- commits
- pull requests
- issues
- repository stars
- current streak
- longest streak
- generated profile/stat cards

The workflow runs every 15 minutes and can also be started manually from **Actions → Update GitHub profile stats → Run workflow**. GitHub can delay scheduled workflows, so this is periodic refresh rather than guaranteed second-by-second real-time data.

## Profile views

The profile-view badge uses the established Komarev GitHub Profile Views Counter service. GitHub does not expose a profile-view count through the GraphQL contribution API, so profile views are handled separately by that badge service.

## Files

- `README.md` — profile layout
- `hero.gif` — typewriter animation
- `waves.gif` — animated layered green footer waves
- `contrib-heatmap.svg` — live contribution calendar render
- `info-card.svg` — terminal profile card
- `stats-card.svg` — live stats card
- `scripts/` — data fetch and asset generators
- `.github/workflows/update-profile-art.yml` — automatic refresh workflow
