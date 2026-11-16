# COMAI

COMAI est une plateforme SaaS multi-agents destinée aux agences de communication et de marketing.

## Socle de la branche

La branche `feature/bootstrap-comai` contient désormais :

- API FastAPI et agents initiaux ;
- modèles SQLAlchemy pour organisations, membres, clients, projets, missions, tâches, livrables et audits ;
- migration Alembic initiale ;
- repositories filtrés par `organization_id` ;
- validation JWT Supabase et contrôle d’organisation sur les routes de missions ;
- adaptateur Supabase Storage avec chemins par organisation ;
- file et worker Redis ;
- COMAI Manager et workflow LangGraph parallèle ;
- Docker Compose pour PostgreSQL et Redis.

Les secrets ne sont jamais stockés dans Git. Les services réels doivent être configurés localement ou dans la CI.

## Démarrage des services

```bash
docker compose up -d postgres redis
```

## Installation backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell : .venv\\Scripts\\Activate.ps1
pip install -e ".[test]"
cp .env.example .env
```

Renseignez ensuite les clés OpenAI et Supabase dans `.env`.

## Base de données

```bash
cd backend
alembic upgrade head
```

## API et worker

```bash
uvicorn app.main:app --reload
python -m app.workers.mission_worker
```

Documentation OpenAPI : <http://127.0.0.1:8000/docs>

## Tests

```bash
cd backend
pytest -q
```

Les tests d’intégration nécessitant PostgreSQL, Redis, OpenAI ou Supabase doivent être exécutés avec les services et variables correspondants. Ils ne sont pas déclarés comme réussis tant qu’ils n’ont pas été exécutés dans cet environnement.

## Routes

| Méthode | Route | Protection |
|---|---|---|
| GET | `/health` | Publique |
| GET | `/api/v1/agents` | À protéger selon le cas d’usage |
| POST | `/api/v1/missions/execute/{agent_id}` | JWT Supabase + organisation |
| POST | `/api/v1/missions/execute-parallel` | JWT Supabase + organisation |

Les routes métier exigent notamment :

```text
Authorization: Bearer <supabase-jwt>
X-Organization-Id: <organization-id>
```
