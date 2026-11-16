from openai import AsyncOpenAI

from app.core.config import get_settings


class OpenAIProvider:
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY n'est pas configurée")
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.text_model = settings.openai_text_model
        self.image_model = settings.openai_image_model

    async def generate_text(self, *, system_prompt: str, user_prompt: str) -> tuple[str, dict[str, int]]:
        response = await self.client.chat.completions.create(
            model=self.text_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        text = response.choices[0].message.content or ""
        usage = response.usage
        return text, {
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0,
        }

    async def generate_image(self, *, prompt: str, size: str = "1024x1024") -> dict[str, str | None]:
        response = await self.client.images.generate(
            model=self.image_model,
            prompt=prompt,
            size=size,
        )
        item = response.data[0]
        return {"url": item.url, "revised_prompt": getattr(item, "revised_prompt", None)}
