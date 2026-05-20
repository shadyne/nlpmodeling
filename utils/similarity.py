from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_similarity_matrix(data):
    years = sorted(data.keys())

    all_docs = []
    labels = []

    for y in years:
        for doc in data[y]:
            all_docs.append(doc)
            labels.append(y)

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(all_docs)

    sim = cosine_similarity(tfidf)

    return {
        "matrix": sim,
        "labels": labels,
        "years": years
    }


def compute_metrics(data, sim_data):
    years = sorted(data.keys())

    results = []

    for i, y in enumerate(years):
        docs = data[y]

        prev_docs = []
        for py in years:
            if py < y:
                prev_docs += data[py]

        last_year = data[years[i-1]] if i > 0 else []

        # similarity last year
        rep_last = 0
        rep_prior = 0

        total = len(docs)

        for d in docs:
            for ly in last_year:
                if cosine_similarity([d], [ly])[0][0] > 0.85:
                    rep_last += 1
                    break

            for p in prev_docs:
                if cosine_similarity([d], [p])[0][0] > 0.85:
                    rep_prior += 1
                    break

        results.append({
            "year": y,
            "total_kam": total,
            "rep_last_year": rep_last,
            "rep_prior_years": rep_prior,
            "new_kam": total - rep_prior
        })

    return results