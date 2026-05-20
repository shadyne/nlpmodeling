from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_similarity_matrix(data):
    all_docs = []
    doc_meta = []
    
    for company, years_data in data.items():
        for y, docs in years_data.items():
            for idx, doc in enumerate(docs):
                all_docs.append(doc)
                doc_meta.append((company, y, idx))
                
    if not all_docs:
        return None, None

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_docs)
    
    return tfidf_matrix, doc_meta

def compute_metrics(data, similarity_data):
    tfidf_matrix, doc_meta = similarity_data
    results = []
    
    if tfidf_matrix is None:
        return results

    def get_indices(target_company, target_year=None, prior_years=None):
        if prior_years:
            return [i for i, meta in enumerate(doc_meta) if meta[0] == target_company and meta[1] in prior_years]
        return [i for i, meta in enumerate(doc_meta) if meta[0] == target_company and meta[1] == target_year]

    for company, years_data in data.items():
        years = sorted(years_data.keys())
        
        for i, y in enumerate(years):
            curr_idx = get_indices(company, target_year=y)
            total_kam = len(curr_idx)
            
            if total_kam == 0:
                continue

            prev_idx = get_indices(company, prior_years=years[:i]) if i > 0 else []
            last_idx = get_indices(company, target_year=years[i-1]) if i > 0 else []

            rep_last = 0
            rep_prior = 0
            identical_last = 0

            for c_id in curr_idx:
                c_vec = tfidf_matrix[c_id]
                
                if last_idx:
                    sims_last = cosine_similarity(c_vec, tfidf_matrix[last_idx])[0]
                    max_sim_last = np.max(sims_last)
                    if max_sim_last > 0.85: rep_last += 1
                    if max_sim_last > 0.99: identical_last += 1
                        
                if prev_idx:
                    sims_prior = cosine_similarity(c_vec, tfidf_matrix[prev_idx])[0]
                    max_sim_prior = np.max(sims_prior)
                    if max_sim_prior > 0.85: rep_prior += 1

            results.append({
                "Company ID": company,
                "Year": y,
                "#KAMs": total_kam,
                "%RepKAM_prior_years": (rep_prior / total_kam) if total_kam > 0 else None,
                "%RepKAM_last_year": (rep_last / total_kam) if total_kam > 0 else None,
                "KAM_Similarity": (identical_last / total_kam) if total_kam > 0 else None,
                "#NewKAM_prior_years": total_kam - rep_prior,
                "#NewKAM_last_year": total_kam - rep_last
            })

    return results