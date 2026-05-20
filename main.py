import os
from utils.pdf_reader import extract_pdfs
from utils.similarity import compute_similarity_matrix, compute_metrics
from utils.exporter import export_full_excel

DATA_DIR = "data"
OUTPUT_EXCEL = "output/kam_similarity_results.xlsx"

def main():
    print("=== KAM SIMILARITY ANALYSIS ===")

    print("[1] Extracting PDF...")
    data = extract_pdfs(DATA_DIR)
    
    print("[2] Computing similarity vector space...")
    sim_data = compute_similarity_matrix(data)

    if sim_data[0] is None:
        print("No documents found. Exiting.")
        return

    print("[3] Computing metrics...")
    metrics = compute_metrics(data, sim_data)

    print("[4] Generating Full Excel Report...")
    export_full_excel(metrics, OUTPUT_EXCEL)

    print(f"[DONE] OUTPUT READY at {OUTPUT_EXCEL}")

if __name__ == "__main__":
    main()