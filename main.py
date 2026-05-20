import os
import sys
from utils.pdf_reader import extract_pdfs
from utils.similarity import compute_similarity_matrix, compute_metrics
from utils.exporter import export_full_excel

DATA_DIR    = "data"
OUTPUT_DIR  = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "kam_similarity_results.xlsx")


def main():
    print("=" * 50)
    print("   KAM SIMILARITY ANALYSIS")
    print("=" * 50)

    print("\n[1] Mengekstrak KAM dari PDF...")
    data = extract_pdfs(DATA_DIR)

    if not data:
        print("Tidak ada data ditemukan. Pastikan folder 'data/' berisi PDF.")
        sys.exit(1)

    total_companies = len(data)
    total_kams = sum(
        len(kams) for comp in data.values() for kams in comp.values()
    )
    print(f"{total_companies} perusahaan | {total_kams} KAM teridentifikasi")

    print("\n[2] Membangun matriks TF-IDF similarity...")
    sim_data = compute_similarity_matrix(data)

    if sim_data[0] is None:
        print("Matriks similarity kosong. Keluar.")
        sys.exit(1)

    print("\n[3] Menghitung metrik KAM...")
    metrics = compute_metrics(data, sim_data)

    if not metrics:
        print("Tidak ada metrik yang berhasil dihitung.")
        sys.exit(1)

    print(f"{len(metrics)} baris metrik dihasilkan")

    print("\n[4] Membuat laporan Excel...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    export_full_excel(metrics, OUTPUT_FILE)

    print("\n" + "=" * 50)
    print(f"[SELESAI] Output: {OUTPUT_FILE}")
    print("=" * 50)


if __name__ == "__main__":
    main()