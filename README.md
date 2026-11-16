# COMAI

COMAI est une plateforme SaaS multi-agents destinée aux agences de communication et de marketing.

## Socle actuel

La branche `feature/bootstrap-comai` contient le premier socle backend :

- API FastAPI ;
- contrats Pydantic pour les missions et résultats ;
- registre des agents ;
- Strategist AI, Copywriter AI et Creative AI ;
- routes de consultation des agents et d’exécution des missions ;
- tests automatisés de base.

Les résultats actuels sont des structures de travail locales. Aucune API OpenAI, base PostgreSQL, génération d’image ou action externe n’est déclarée opérationnelle à ce stade.

## Installation du backend

Pré-requis : Python 3.12 ou supérieur.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell : .venv\\Scripts\\Activate.ps1
pip install -e ".[test]"
```

## Lancement

```bash
uvicorn app.main:app --reload
```

API : <http://127.0.0.1:8000>  
Documentation OpenAPI : <http://127.0.0.1:8000/docs>

## Vérification

```bash
pytest -q
```

## Routes initiales

| Méthode | Route | Usage |
|---|---|---|
| GET | `/health` | Vérifier l’état de l’API |
| GET | `/api/v1/agents` | Lister les agents disponibles |
| POST | `/api/v1/missions/execute/{agent_id}` | Exécuter une mission sur un agent |

## Exemple de mission

```bash
curl -X POST http://127.0.0.1:8000/api/v1/missions/execute/strategist_ai \\
  -H "Content-Type: application/json" \\
  -d '{
    "task_id": "task-1",
    "organization_id": "org-1",
    "user_id": "user-1",
    "objective": "Préparer une campagne de lancement à Niamey",
    "context": {"secteur": "mode"},
    "authorized_tools": []
  }'
```

## Prochaines étapes

1. Ajouter l’authentification et l’isolation multi-tenant.
2. Introduire la persistance PostgreSQL et les migrations.
3. Ajouter COMAI Manager et LangGraph.
4. Connecter OpenAI derrière des interfaces configurables.
5. Ajouter la mémoire, les coûts, les livrables et la validation humaine.
