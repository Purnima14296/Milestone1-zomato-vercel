from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(".env")


class Settings(BaseSettings):
    """
    Phase 0 settings.

    Values are loaded from environment variables and optional `.env`.
    """

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE) if _ENV_FILE.is_file() else None,
        env_file_encoding="utf-8",
    )

    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    # LLM configuration (Phase 4+). Optional in Phase 0.
    llm_provider: str | None = Field(default=None, validation_alias="LLM_PROVIDER")
    llm_api_key: str | None = Field(default=None, validation_alias="LLM_API_KEY")

    # Groq (Phase 4)
    groq_api_key: str | None = Field(default=None, validation_alias="GROQ_API_KEY")
    groq_model: str = Field(default="llama-3.3-70b-versatile", validation_alias="GROQ_MODEL")

    # Dataset configuration (Phase 1+).
    hf_dataset_id: str = Field(
        default="ManikaSaini/zomato-restaurant-recommendation",
        validation_alias="HF_DATASET_ID",
    )
    hf_dataset_split: str = Field(default="train", validation_alias="HF_DATASET_SPLIT")

    # Processed dataset (Phase 7 / Render). Overrides default path resolution when set.
    zomato_processed_dataset: str | None = Field(
        default=None, validation_alias="ZOMATO_PROCESSED_DATASET"
    )

