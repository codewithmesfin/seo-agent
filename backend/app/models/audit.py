from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from beanie import Document, Indexed, Link
from pydantic import Field
from .user import User

class Page(Document):
    url: str
    scan_id: Indexed(str)
    title: Optional[str] = None
    meta_description: Optional[str] = None
    seo_score: float = 0.0
    word_count: int = 0
    data: Dict[str, Any] = {} # Full SEO data
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "pages"

class Scan(Document):
    user_id: Indexed(str)
    domain: str
    overall_score: float = 0.0
    status: str = "pending" # pending, running, completed, failed
    progress: int = 0
    pages_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "scans"

class Competitor(Document):
    user_id: Indexed(str)
    domain: str
    base_domain: str
    overlap_score: float = 0.0
    data: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "competitors"
