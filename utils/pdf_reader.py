import os
import re
import fitz  # PyMuPDF
from tqdm import tqdm
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed

from utils.text_cleaner import clean_text
from utils.kam_extractor import split_kams_from_text


def process_single_pdf(file: str, base_dir: str):

    if not file.endswith(".pdf"):
        return None

    match_year = re.search(r"(202[0-9])", file)
    if not match_year:
        return None
    year = int(match_year.group(1))

    company_id = re.sub(r"(202[0-9])", "", file)
    company_id = re.sub(r"\.pdf$", "", company_id, flags=re.IGNORECASE)
    company_id = company_id.strip(" _-")
    if not company_id:
        company_id = "UNKNOWN_COMPANY"

    path = os.path.join(base_dir, file)

    try:
        doc = fitz.open(path)

        raw_pages = [page.get_text() for page in doc]
        doc.close()
        raw_text = "\n".join(raw_pages)

        cleaned = clean_text(raw_text)

        kams = split_kams_from_text(cleaned)

        if kams:
            return (company_id, year, kams)

    except Exception as e:
        print(f"\n[ERROR] Gagal membaca {file}: {e}")

    return None


def extract_pdfs(base_dir: str) -> dict:

    data = defaultdict(lambda: defaultdict(list))

    if not os.path.exists(base_dir):
        print(f"[!] Folder '{base_dir}' tidak ditemukan!")
        return {}

    files = [f for f in os.listdir(base_dir) if f.lower().endswith(".pdf")]
    print(f"Ditemukan {len(files)} file PDF. Memulai ekstraksi...")

    with ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(process_single_pdf, f, base_dir): f for f in files
        }
        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Extracting PDFs"
        ):
            result = future.result()
            if result:
                comp_id, yr, kams = result
                data[comp_id][yr].extend(kams)

    total_kams = sum(
        len(kams)
        for comp in data.values()
        for kams in comp.values()
    )
    print(f"Total KAM teridentifikasi: {total_kams} dari {len(data)} perusahaan.")
    return data