import os
import pdfplumber
from tqdm import tqdm

def extract_pdfs(base_dir):
    data = {}

    for year in os.listdir(base_dir):
        year_path = os.path.join(base_dir, year)
        if not os.path.isdir(year_path):
            continue

        texts = []

        for file in tqdm(os.listdir(year_path), desc=f"Reading {year}"):
            if file.endswith(".pdf"):
                path = os.path.join(year_path, file)

                try:
                    with pdfplumber.open(path) as pdf:
                        text = " ".join([page.extract_text() or "" for page in pdf.pages])
                        texts.append(text)
                except:
                    continue

        data[year] = texts

    return data