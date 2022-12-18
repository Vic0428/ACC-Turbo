import matplotlib.pyplot as plt
import pandas as pd


def plot_10_features():
    df = pd.read_csv("10features.dat", header=None)
    n_cluster_list = [4, 6, 8, 10, 12]
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    ax1.plot(n_cluster_list, df.iloc[0:5, 1], "-o", label="Online K-means")
    ax1.plot(n_cluster_list, df.iloc[5:10, 1], "-o", label="ACC-Turbo Clustering")
    ax1.axhline(y=df.iloc[5, 1], linestyle="--", color='gray', label="ACC-Turbo on Tofino")
    ax1.set_xlabel("Num Clusters")
    ax1.set_ylabel("Purity (%)")
    ax1.legend()

    ax2.plot(n_cluster_list, df.iloc[0:5, 4], "-o", label="Online K-means")
    ax2.plot(n_cluster_list, df.iloc[5:10, 4], "-o", label="ACC-Turbo Clustering")
    ax2.axhline(y=df.iloc[5, 4], linestyle="--", color='gray', label="ACC-Turbo on Tofino")
    ax2.set_xlabel("Num Clusters")
    ax2.set_ylabel("Recall Benign (%)")
    ax2.legend()

    ax3.plot(n_cluster_list, df.iloc[0:5, 5], "-o", label="Online K-means")
    ax3.plot(n_cluster_list, df.iloc[5:10, 5], "-o", label="ACC-Turbo Clustering")
    ax3.axhline(y=df.iloc[5, 5], linestyle="--", color='gray', label="ACC-Turbo on Tofino")
    ax3.set_xlabel("Num Clusters")
    ax3.set_ylabel("Recall Malicious (%)")
    ax3.legend()

    fig.savefig("10features.png")

if __name__ == "__main__":
    plot_10_features()