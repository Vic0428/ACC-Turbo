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
         'lines.markersize': 10,
         'lines.markerfacecolor': 'none',
         'lines.markeredgecolor': 'auto',
         'lines.markeredgewidth': 2.0,
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
    ax1.set_ylim(bottom=50, top=102)
    ax1.set_xlim(left=0)
    ax1.legend()
    # fig.savefig("ddos_purity.eps")
    # fig.savefig("ddos_purity.png")

    # print("[RMTF] Purity: {}".format(df.iloc[0:5, 1]))
    # print("[Ideal CPU] Purity: {}".format(df.iloc[6:11, 1]))
    # print("[Switch] Purity: {}".format(df.iloc[5, 1]))

    ## For average recall
    # fig, ax3 = plt.subplots(1, 1)
    # switch = (df.iloc[5, 4] + df.iloc[5, 5])/2
    # f3 = (df.iloc[0:5, 4] + df.iloc[0:5, 5]) / 2
    # cpu = (df.iloc[6:11, 4] + df.iloc[6:11, 5]) / 2,

    # switch = df.iloc[5, 4]
    # f3 = df.iloc[0:5, 4]
    # cpu = df.iloc[6:11, 4]

    switch = df.iloc[5, 5]
    f3 = df.iloc[0:5, 5]
    cpu = df.iloc[6:11, 5]
    print("Max ratio: {}".format(max((100 - switch) / (100-f3))))
    
    ax3.plot(n_cluster_list, f3, "-o", label="[F3] Online K-means")
    ax3.plot(n_cluster_list, cpu, "-o", label="[Ideal CPU] Offline K-means")
    ax3.axhline(y=switch, linestyle="--", color='gray', label="[Switch] ACC-Turbo")
    ax3.set_xticks([0] + n_cluster_list)
    ax3.set_xlabel("Num Clusters", labelpad=0)
    ax3.set_ylabel("Recall Malicious(%)", labelpad=0)
    ax3.set_ylim(bottom=50, top=102)
    ax3.set_xlim(left=0)
    ax3.legend(loc='center left', bbox_to_anchor=(0, 0.4))
    plt.tight_layout()
    fig.savefig("ddos_purity_recall.eps")
    fig.savefig("ddos_purity_recall.png")

    print("[RMTF] Recall: {}".format(f3))
    print("[Switch+CPU] Recall: {}".format(cpu))
    print("[Switch] Recall: {}".format(switch))
   