"""Save parsed document metadata into the Supabase 'documents' table."""

from src.app.core.database import get_supabase
from src.app.core.logging import get_logger
from src.app.ingestion.parser import ParsedDocument

logger = get_logger(__name__)


def save_document(parsed: ParsedDocument, company: str) -> int:
    supabase = get_supabase()

    filename = parsed.source_path.split("\\")[-1].split("/")[-1]

    row = {
        "filename": filename,
        "company": company,
        "char_count": len(parsed.text),
        "num_tables": parsed.num_tables,
        "num_images": parsed.num_images,
    }

    logger.info("Saving %s to database...", filename)
    response = supabase.table("documents").insert(row).execute()

    new_id = response.data[0]["id"]
    logger.info("Saved %s with id=%d", filename, new_id)
    return new_id