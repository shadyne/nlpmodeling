import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

REPETITION_THRESHOLD = 0.70


def compute_similarity_matrix(data: dict):

    all_docs = []
    doc_meta = []

    for company, years_data in data.items():
        for year, kams in years_data.items():
            for idx, kam_text in enumerate(kams):
                all_docs.append(kam_text)
                doc_meta.append((company, year, idx))

    if not all_docs:
        return None, None

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),  
        min_df=1,
        sublinear_tf=True,    
    )
    tfidf_matrix = vectorizer.fit_transform(all_docs)

    return tfidf_matrix, doc_meta


def compute_metrics(data: dict, similarity_data: tuple) -> list:

    tfidf_matrix, doc_meta = similarity_data
    results = []

    if tfidf_matrix is None:
        return results

    def get_indices(target_company: str, target_year: int = None, prior_years: list = None):
        if prior_years:
            return [
                i for i, (c, y, _) in enumerate(doc_meta)
                if c == target_company and y in prior_years
            ]
        return [
            i for i, (c, y, _) in enumerate(doc_meta)
            if c == target_company and y == target_year
        ]

    for company, years_data in data.items():
        years = sorted(years_data.keys())

        for i, year in enumerate(years):
            curr_idx = get_indices(company, target_year=year)
            total_kam = len(curr_idx)

            if total_kam == 0:
                continue

            prev_years = years[:i]
            prev_idx   = get_indices(company, prior_years=prev_years) if prev_years else []

            last_year  = years[i - 1] if i > 0 else None
            last_idx   = get_indices(company, target_year=last_year) if last_year else []

            rep_prior  = 0   
            rep_last   = 0  

            similarity_scores_last = []

            for c_id in curr_idx:
                c_vec = tfidf_matrix[c_id]

                if last_idx:
                    sims_last = cosine_similarity(c_vec, tfidf_matrix[last_idx])[0]
                    max_sim_last = float(np.max(sims_last))

                    similarity_scores_last.append(max_sim_last)

                    if max_sim_last >= REPETITION_THRESHOLD:
                        rep_last += 1
                else:
                    similarity_scores_last.append(0.0)

                if prev_idx:
                    sims_prior = cosine_similarity(c_vec, tfidf_matrix[prev_idx])[0]
                    max_sim_prior = float(np.max(sims_prior))

                    if max_sim_prior >= REPETITION_THRESHOLD:
                        rep_prior += 1

            kam_similarity = (
                float(np.mean(similarity_scores_last))
                if last_idx else None
            )

            results.append({
                "Company ID"          : company,
                "Year"                : year,
                "#KAMs"               : total_kam,
                "%RepKAM_prior_years" : (rep_prior / total_kam) if prev_idx else None,
                "%RepKAM_last_year"   : (rep_last  / total_kam) if last_idx  else None,
                "KAM_Similarity"      : kam_similarity,
                "#NewKAM_prior_years" : (total_kam - rep_prior) if prev_idx else None,
                "#NewKAM_last_year"   : (total_kam - rep_last)  if last_idx  else None,
            })

    return results