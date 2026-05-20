import os
import re
import fitz  # Ini adalah PyMuPDF, library PDF super cepat
from tqdm import tqdm
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from utils.text_cleaner import clean_text

def process_single_pdf(file, base_dir):
    """Fungsi untuk membaca satu PDF. Dipisah agar bisa diproses paralel."""
    if not file.endswith(".pdf") or "Copy of" in file:
        return None
    
    match_year = re.search(r'(2022|2023|2024)', file)
    if not match_year:
        return None
    year = int(match_year.group(1))
    
    company_id = file.replace(str(year), '').replace('.pdf', '').strip(' _-')
    if not company_id:
        company_id = "UNKNOWN_COMPANY"

    path = os.path.join(base_dir, file)
    
    try:
        doc = fitz.open(path)
        
        text = " ".join([page.get_text() for page in doc])
        doc.close()
        
        cleaned_text = clean_text(text)
        
        if cleaned_text.strip():
            return (company_id, year, cleaned_text)
            
    except Exception as e:
        print(f"\nError reading {file}: {e}")
        return None
        
    return None

def extract_pdfs(base_dir):
    data = defaultdict(lambda: defaultdict(list))
    
    if not os.path.exists(base_dir):
        print(f"Folder {base_dir} tidak ditemukan!")
        return {}

    files = [f for f in os.listdir(base_dir) if f.endswith('.pdf')]

    print(f"Ditemukan {len(files)} file PDF. Memulai ekstraksi cepat...")
    
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_single_pdf, file, base_dir): file for file in files}
        
        for future in tqdm(as_completed(futures), total=len(futures), desc="Extracting PDFs"):
            result = future.result()
            if result:
                comp_id, y, text = result
                data[comp_id][y].append(text)

    return data