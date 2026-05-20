import re


def clean_text(text: str) -> str:

    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"[^\x20-\x7E]", " ", text)

    text = re.sub(r"[•●▪▸►◆■□▶]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip().lower()