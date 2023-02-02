"""
Plot based on the `simulations/python/plots/num_clusters/clustering_performance_logs.dat`
"""
from cProfile import label
import matplotlib.pyplot as plt
import pandas as pd
import sys


if __name__ == "__main__":
    name = sys.argv[1]
    df = pd.read_csv(name, header=None)
    n_cluster_list = [4, 8, 12, 16, 20]
    plt.rc('legend', fontsize=8)

    ## For purity
    fig, ax1 = plt.subplots(1, 1, figsize=(4.5, 4))
    ax1.plot(n_cluster_list, df.iloc[0:5, 1], "-o",  fillstyle='none', label="[RMTF] Online K-means")
    ax1.plot(n_cluster_list, df.iloc[6:11, 1], "-o", fillstyle='none', label="[Ideal CPU] Offline K-means")
    ax1.axhline(y=df.iloc[5, 1], linestyle="--", color='gray', label="[Switch] ACC-Turbo")
    ax1.set_xticks([0] + n_cluster_list)
    ax1.set_xlabel("Num Clusters", labelpad=0)
    ax1.set_ylabel("Purity (%)", labelpad=0)
    ax1.set_ylim(bottom=0, top=102)
    ax1.set_xlim(left=0)
    ax1.legend(bbox_to_anchor=(0.35, 0.3), loc='upper left', borderaxespad=0)
    fig.savefig("ddos_purity.eps")
    fig.savefig("ddos_purity.png")

    print("[RMTF] Purity: {}".format(df.iloc[0:5, 1]))
    print("[Ideal CPU] Purity: {}".format(df.iloc[6:11, 1]))
    print("[Switch] Purity: {}".format(df.iloc[5, 1]))
    # ## For Recall Benign
    # fig, ax2 = plt.subplots(1, 1, figsize=(4.5, 4))
    # ax2.plot(n_cluster_list, df.iloc[0:5, 4], "-o", label="Online K-means")
    # ax2.plot(n_cluster_list, df.iloc[6:11, 4], "-o", label="Offline K-means")
    # ax2.axhline(y=df.iloc[5, 4], linestyle="--", color='gray', label="ACC-Turbo")
    # # ax2.set_yticks([80 + i for i in range(0, 21, 4)])
    # # ax2.set_ylim(bottom=84)
    # ax2.set_xticks(n_cluster_list)
    # ax2.set_xlabel("Num Clusters", labelpad=0)
    # ax2.set_ylabel("Recall Benign (%)", labelpad=0)
    # ax2.legend(bbox_to_anchor=(0.65, 0.3), loc='upper left', borderaxespad=0)
    # fig.savefig("ddos_recall.eps")
    # fig.savefig("ddos_recall.png")

    ## For average recall
    fig, ax3 = plt.subplots(1, 1, figsize=(4.5, 4))
    ax3.plot(n_cluster_list, (df.iloc[0:5, 4] + df.iloc[0:5, 5]) / 2, "-o", fillstyle='none', label="[RMTF] Online K-means")
    ax3.plot(n_cluster_list, (df.iloc[6:11, 4] + df.iloc[6:11, 5]) / 2, "-o", fillstyle='none', label="[Ideal CPU] Offline K-means")
    ax3.axhline(y=(df.iloc[5, 4] + df.iloc[5, 5])/2, linestyle="--", color='gray', label="[Switch] ACC-Turbo")
    # ax2.set_yticks([80 + i for i in range(0, 21, 4)])
    # ax2.set_ylim(bottom=84)
    ax3.set_xticks([0] + n_cluster_list)
    ax3.set_xlabel("Num Clusters", labelpad=0)
    ax3.set_ylabel("Recall(%)", labelpad=0)
    ax3.set_ylim(bottom=0, top=102)
    ax3.set_xlim(left=0)
    ax3.legend(bbox_to_anchor=(0.35, 0.3), loc='upper left', borderaxespad=0)
    fig.savefig("ddos_avg_recall.eps")
    fig.savefig("ddos_avg_recall.png")

    print("[RMTF] Recall: {}".format( (df.iloc[0:5, 4] + df.iloc[0:5, 5]) / 2))
    print("[Switch+CPU] Recall: {}".format((df.iloc[6:11, 4] + df.iloc[6:11, 5]) / 2))
    print("[Switch] Recall: {}".format((df.iloc[5, 4] + df.iloc[5, 5])/2))
    # fig, ax3 = plt.subplots(1, 1, figsize=(4.5, 4))
    # ax3.plot(df.iloc[0:5, 1], df.iloc[0:5, 4], "-o", label="Switch+FPGA")
    # ax3.plot(df.iloc[6:11, 1], df.iloc[6:11, 4], "-o", label="Switch+CPU")
    # ax3.plot(df.iloc[5, 1], df.iloc[5, 4], "o", label="Switch-only")
    # ax3.set_ylabel("Purity (%)", labelpad=0)
    # ax3.set_ylabel("Recall Benign (%)", labelpad=0)
    # ax3.legend()

    # fig.savefig("ddos_tradeoff.eps")
    # fig.savefig("ddos_tradeoff.png")

