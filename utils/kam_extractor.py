import re
from typing import List

KAM_HEADING_PATTERNS = [
    # Bahasa Indonesia
    r"hal\s+audit\s+utama\s*[\d]*\s*[:\-–]?\s*(.+?)(?=hal\s+audit\s+utama|\Z)",
    r"matter\s+audit\s+utama\s*[\d]*\s*[:\-–]?\s*(.+?)(?=matter\s+audit\s+utama|\Z)",

    # Bahasa Inggris — pola bernomor, mis. "Key Audit Matter 1", "KAM 1"
    r"key\s+audit\s+matter\s*[\d]+\s*[:\-–]?\s*(.+?)(?=key\s+audit\s+matter\s*[\d]|\Z)",
    r"\bkam\s*[\d]+\s*[:\-–]?\s*(.+?)(?=\bkam\s*[\d]|\Z)",

    # Pola dengan bullet / huruf: "A. ...", "1. ...", "I. ..."
    r"(?:^|\n)\s*(?:[A-Z]|[IVX]+|\d+)\.\s+((?:(?!\n\s*(?:[A-Z]|[IVX]+|\d+)\.).)+)",
]

KAM_SECTION_SPLITTER = re.compile(
    r"(?i)(?:"
    r"key\s+audit\s+matter"
    r"|hal\s+audit\s+utama"
    r"|matter\s+audit\s+utama"
    r"|principal\s+risk"
    r"|critical\s+audit\s+matter"
    r")"
    r"[\s\S]{0,120}?(?=\n)",
    re.IGNORECASE | re.MULTILINE,
)


def split_kams_from_text(text: str, min_length: int = 100) -> List[str]:

    matches = list(KAM_SECTION_SPLITTER.finditer(text))

    if len(matches) < 2:
        stripped = text.strip()
        return [stripped] if len(stripped) >= min_length else []

    segments: List[str] = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        segment = text[start:end].strip()
        if len(segment) >= min_length:
            segments.append(segment)

    if not segments:
        stripped = text.strip()
        return [stripped] if len(stripped) >= min_length else []

    return segments