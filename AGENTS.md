# Specialized Docker Images

This repository contains Docker images for specialized purposes, built automatically via GitHub Actions and published to GitHub Container Registry (GHCR).

## Available Images

| Image | Purpose | Tags |
|-------|---------|------|
| `ai-agents` | CrewAI, OpenAI, LiteLLM, FastAPI, ChromaDB, FAISS | `latest`, `v*.*.*` |
| `webscraping` | Scrapy, BeautifulSoup, Selenium, Playwright | `latest`, `v*.*.*` |
| `machine-learning` | PyTorch, TensorFlow, scikit-learn, CUDA support | `latest`, `v*.*.*` |
| `nlp` | spaCy, NLTK, transformers, LLM tools | `latest`, `v*.*.*` |
| `analytics-db` | Analytics with Polars, PostgreSQL, MongoDB | `latest`, `v*.*.*` |
| `analytics-db-orchestration` | Dagster orchestration for data workflows | `latest`, `v*.*.*` |
| `analytics-db-orchestration-opencode` | Dagster orchestration with OpenCode integration | `latest`, `v*.*.*` |

## Usage

Pull and run any image:

```bash
# Pull from GHCR
docker pull ghcr.io/<org>/analytics:latest

# Run with mounted workspace
docker run -v $(pwd):/workspace ghcr.io/<org>/analytics:latest
```

## Repository Structure

```
.
├── images/
│   ├── ai-agents/
│   │   ├── Dockerfile
│   │   └── requirements.in
│   ├── webscraping/
│   ├── machine-learning/
│   ├── nlp/
│   ├── analytics-db/
│   ├── analytics-db-orchestration/
│   ├── analytics-db-orchestration-opencode/
│   └── one-company/
├── .github/
│   └── workflows/
│       ├── build-analytics.yml
│       ├── build-analytics-db-orchestration.yml
│       ├── build-analytics-db-orchestration-opencode.yml
│       ├── build-webscraping.yml
│       └── ...
└── agents.md (this file)
```

## Automated Builds

GitHub Actions workflows trigger on:
- Push to `main` branch (updates `latest` tag)
- New releases (tags images with release version)
- Weekly schedule (security updates)
- Pull requests (build verification only, no push)

## Building Locally

```bash
cd images/analytics
docker build -t analytics:local .
```

## Contributing

1. Add new purpose folder under `images/`
2. Include `Dockerfile` and `requirements.in`
3. Add corresponding workflow under `.github/workflows/`
4. Update this `agents.md` with image details
