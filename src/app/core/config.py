"""Loads settings from .env once and shares them across the app."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # GCP / Gemini
    gcp_project_id: str
    gcp_location: str = "asia-south1"
    gemini_llm_model: str = "gemini-2.5-flash"

    # Supabase
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_key: str = ""
    supabase_db_password: str = ""

    # Langfuse
    langfuse_host: str = "https://cloud.langfuse.com"
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    gemini_embed_model: str = "text-embedding-005"


@lru_cache
def get_settings() -> Settings:
    return Settings()