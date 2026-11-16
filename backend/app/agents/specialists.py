from app.agents.base import BaseAgent
from app.schemas.agents import AgentDescriptor, AgentResult, AgentTask


class StrategistAgent(BaseAgent):
    descriptor = AgentDescriptor(
        agent_id="strategist_ai",
        name="Strategist AI",
        description="Stratégie marketing et communication",
        capabilities=["étude de marché", "personas", "objectifs SMART", "SWOT"],
        authorized_tools=[],
    )

    async def execute(self, task: AgentTask) -> AgentResult:
        return AgentResult(
            agent_id=self.descriptor.agent_id,
            task_id=task.task_id,
            status="needs_review",
            summary="Brief stratégique préparé à partir des informations fournies.",
            deliverables=[
                {
                    "type": "strategy_brief",
                    "content": {
                        "objective": task.objective,
                        "facts": task.context,
                        "assumptions": [],
                    },
                }
            ],
            warnings=[
                "Aucune donnée externe fournie; les éléments de marché restent à documenter."
            ],
            next_recommendations=[
                "Valider la cible et fournir les données disponibles sur le marché local."
            ],
        )


class CopywriterAgent(BaseAgent):
    descriptor = AgentDescriptor(
        agent_id="copywriter_ai",
        name="Copywriter AI",
        description="Rédaction publicitaire",
        capabilities=["slogans", "textes publicitaires", "scripts vidéo", "storytelling"],
        authorized_tools=[],
    )

    async def execute(self, task: AgentTask) -> AgentResult:
        return AgentResult(
            agent_id=self.descriptor.agent_id,
            task_id=task.task_id,
            status="needs_review",
            summary="Premières pistes rédactionnelles préparées.",
            deliverables=[
                {
                    "type": "copy_draft",
                    "content": {"brief": task.objective, "drafts": []},
                }
            ],
            warnings=[
                "Les textes doivent être validés selon la voix de marque avant publication."
            ],
        )


class CreativeAgent(BaseAgent):
    descriptor = AgentDescriptor(
        agent_id="creative_ai",
        name="Creative AI",
        description="Direction artistique et concepts visuels",
        capabilities=[
            "concepts visuels",
            "briefs graphiques",
            "prompts d’images",
            "formats publicitaires",
        ],
        authorized_tools=[],
    )

    async def execute(self, task: AgentTask) -> AgentResult:
        return AgentResult(
            agent_id=self.descriptor.agent_id,
            task_id=task.task_id,
            status="needs_review",
            summary="Direction artistique et brief visuel préparés.",
            deliverables=[
                {
                    "type": "creative_brief",
                    "content": {
                        "objective": task.objective,
                        "image_generation": {
                            "status": "not_requested",
                            "provider": None,
                        },
                    },
                }
            ],
            warnings=[
                "Aucun visuel généré: aucun fournisseur d’images n’est configuré."
            ],
        )
