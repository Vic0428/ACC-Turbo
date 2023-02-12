"""
Plot based on the `simulations/python/plots/num_clusters/clustering_performance_logs.dat`
"""
from cProfile import label
import matplotlib.pyplot as plt
import pandas as pd
import sys
import matplotlib.pylab as pylab
plt.style.use("seaborn-paper")
font_size=16
params = {'legend.fontsize': font_size,
          'figure.figsize': (12, 4),
         'axes.labelsize': font_size,
         'axes.titlesize': font_size,
         'xtick.labelsize':font_size,
         'ytick.labelsize':font_size,
         'lines.linewidth': 2,
         'lines.markersize': 8,
         'font.weight': 3}
pylab.rcParams.update(params)

if __name__ == "__main__":
    name = sys.argv[1]
    df = pd.read_csv(name, header=None)
    n_cluster_list = [4, 8, 12, 16, 20]

    ## For purity
    fig, (ax1, ax3) = plt.subplots(1, 2)
    ax1.plot(n_cluster_list, df.iloc[0:5, 1], "-o",  label="[F3] Online K-means")
    ax1.plot(n_cluster_list, df.iloc[6:11, 1], "-o", label="[Ideal CPU] Offline K-means")
    ax1.axhline(y=df.iloc[5, 1], linestyle="--", color='gray', label="[Switch] ACC-Turbo")
    ax1.set_xticks([0] + n_cluster_list)
    ax1.set_xlabel("Num Clusters")
    ax1.set_ylabel("Purity (%)")
    ax1.set_ylim(bottom=0, top=102)
    ax1.set_xlim(left=0)
    ax1.legend()
    # fig.savefig("ddos_purity.eps")
    # fig.savefig("ddos_purity.png")

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
    # fig, ax3 = plt.subplots(1, 1)
    ax3.plot(n_cluster_list, (df.iloc[0:5, 4] + df.iloc[0:5, 5]) / 2, "-o", label="[F3] Online K-means")
    ax3.plot(n_cluster_list, (df.iloc[6:11, 4] + df.iloc[6:11, 5]) / 2, "-o", label="[Ideal CPU] Offline K-means")
    ax3.axhline(y=(df.iloc[5, 4] + df.iloc[5, 5])/2, linestyle="--", color='gray', label="[Switch] ACC-Turbo")
    # ax2.set_yticks([80 + i for i in range(0, 21, 4)])
    # ax2.set_ylim(bottom=84)
    ax3.set_xticks([0] + n_cluster_list)
    ax3.set_xlabel("Num Clusters", labelpad=0)
    ax3.set_ylabel("Recall(%)", labelpad=0)
    ax3.set_ylim(bottom=0, top=102)
    ax3.set_xlim(left=0)
    ax3.legend()
    plt.tight_layout()
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

