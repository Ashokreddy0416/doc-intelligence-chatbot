"""Creates one shared Supabase client for the whole app."""

from functools import lru_cache

from supabase import create_client, Client

from src.app.core.config import get_settings
from src.app.core.logging import get_logger

logger = get_logger(__name__)


@lru_cache
def get_supabase() -> Client:
    settings = get_settings()
    logger.info("Connecting to Supabase...")
    client = create_client(settings.supabase_url, settings.supabase_service_key)
    return client