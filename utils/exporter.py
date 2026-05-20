import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def export_excel(metrics, path):
    df = pd.DataFrame(metrics)

    df["%rep_last_year"] = df["rep_last_year"] / df["total_kam"]
    df["%rep_prior_years"] = df["rep_prior_years"] / df["total_kam"]

    df.to_excel(path, index=False)


def export_graph(metrics, path):
    df = pd.DataFrame(metrics)

    plt.figure()

    plt.plot(df["year"], df["%rep_last_year"], label="Rep Last Year")
    plt.plot(df["year"], df["%rep_prior_years"], label="Rep Prior Years")

    plt.legend()
    plt.title("KAM Similarity Trend")
    plt.savefig(path)
    plt.close()