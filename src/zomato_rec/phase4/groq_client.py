from __future__ import annotations

from dataclasses import dataclass

from groq import Groq


@dataclass(frozen=True)
class GroqChatConfig:
    model: str
    temperature: float = 0.2
    max_tokens: int = 900


def groq_chat(*, api_key: str, cfg: GroqChatConfig, system: str, user: str) -> str:
    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model=cfg.model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=cfg.temperature,
        max_tokens=cfg.max_tokens,
    )
    return resp.choices[0].message.content or ""

