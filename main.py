import os
from utils.pdf_reader import extract_pdfs
from utils.similarity import compute_similarity_matrix, compute_metrics
from utils.exporter import export_excel, export_graph

DATA_DIR = "data"
OUTPUT_EXCEL = "output/result.xlsx"
OUTPUT_GRAPH = "output/graph.png"

def main():
    print("=== KAM SIMILARITY ANALYSIS ===")

    print("[1] Extracting PDF...")
    data = extract_pdfs(DATA_DIR)

    
    print("[2] Computing similarity...")
    sim_matrix = compute_similarity_matrix(data)

    print("[3] Computing metrics...")
    metrics = compute_metrics(data, sim_matrix)

    print("[4] Exporting Excel...")
    export_excel(metrics, OUTPUT_EXCEL)

    print("[5] Generating graph...")
    export_graph(metrics, OUTPUT_GRAPH)

    print("DONE → OUTPUT READY")

if __name__ == "__main__":
    main()