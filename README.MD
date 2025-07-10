![alt text](imunexlogo.png)
# Imunex API

**Status — Pre‑release (simplified OSS seed)**

Imunex API is an open‑source Django service that generates a resilient device fingerprint from multiple TLS & network signature sources (JA3, JA4, JA4+, PeetPrint …) and returns a risk score that can be consumed in authentication and fraud‑detection pipelines.

> **⚠️ Work in progress:** This repository contains a trimmed‑down reference implementation. Proprietary ML/scoring logic used in production has been removed. Sections marked **TODO** will be completed as we progressively open additional modules.

---

## Table of Contents

- [Imunex API](#imunexapi)
  - [Table of Contents](#table-of-contents)
  - [How It Works](#howitworks)
  - [Quick Start](#quickstart)
  - [API Reference](#apireference)
  - [Fingerprint Models](#fingerprintmodels)
  - [Scoring Algorithm](#scoringalgorithm)
  - [Project Structure](#projectstructure)
  - [Contributing](#contributing)
  - [License](#license)

---

## How It Works

**TODO:** High‑level architecture diagram + narrative (Django, PostgreSQL, Celery, Redis).

The simplified OSS build currently ships with:

* Core fingerprint parsers for **JA3**, **JA4**, **JA4+**, **PeetPrint**
* REST endpoint `/v1/fingerprint/` that ingests raw TLS/HTTP metadata
* Baseline scoring stub returning deterministic values for demo purposes

## Quick Start

```bash
# Clone repository
$ git clone https://github.com/Imunex/api.git
$ cd api

# Spin up local stack (Django + Postgres) with Docker Compose
$ docker compose up -d

# Create admin user
$ docker compose exec web python manage.py createsuperuser
```

**TODO:** Post‑install smoke test and example cURL request/response.

## API Reference

**TODO:** OpenAPI snippet or link once `swagger.json` is published.

## Fingerprint Models

**TODO:** Explain each signature (JA3, JA4, JA4+, PeetPrint) and how we normalise them into a canonical `device_id`.

## Scoring Algorithm

**TODO:** Public explanation of heuristic tiers and how the production model differs from the open version.

## Project Structure
**TODO** After pushing code, update this tree
```text
imunex_api/
├─ imunex/           # Django project
│  ├─ core/          
│  ├─ fingerprint/  
│  └─ scoring/       
└─ docker/
   ├─ Dockerfile
   └─ docker-compose.yml
```

## Contributing

Pull requests are welcome! Before submitting, please:

1. Open an issue describing the bug/feature.
2. Follow the style guide in `.editorconfig` and run `pre‑commit` hooks.
3. Keep PRs focused; large rewrites will be harder to review.

## License

See [`LICENSE`](LICENSE) for details.
