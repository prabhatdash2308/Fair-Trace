from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class ParsedDocument:
    """
    Standardized representation of a parsed document regardless of original format.
    """
    text: str
    page_count: int
    word_count: int
    character_count: int
    title: Optional[str] = None
    author: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    parser_used: str = "unknown"
    parser_version: str = "1.0.0"
