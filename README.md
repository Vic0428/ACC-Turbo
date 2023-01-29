# ACC-Turbo

## For vic's expereiment
1. Derives the necessary speedup `python3 simulations/calc_speedup.py /euler/CICDDoS2019/data/statistics` 
    * Example: Needs 108X speedup to achieve 100Gbps throughput

2. Change the `SPEED_UP_RATIO` constant in `simulations/python/analyzer.py` 

3. `./run_fig_10.sh` in `simulations` folder and we can see the generated `simulations/python/plots/num_clusters/clustering_performance_logs.dat`

4. `python3 plot.py python/plots/num_clusters/clustering_performance_logs.dat` in the `simulations` folder and we can see the generated figure. 


This repository contains the code used in [ACC-Turbo](https://nsg.ee.ethz.ch/fileadmin/user_upload/sigcomm22-final615.pdf), which will be presented at [SIGCOMM'22](https://conferences.sigcomm.org/sigcomm/2022/).

## What can I find in this repo?

* `simulations` contains the code of all the experiments for **Section 2 (Background)** and **Section 8 (Simulation-based Evaluation)** of the paper. It includes an implementation of ACC-Turbo on Python and the experiments on [NetBench](https://github.com/ndal-eth/netbench).

* `tofino` contains the code of all the experiments for **Section 7 (Hardware-based Evaluation)** of the paper. It includes the code to run ACC-Turbo on programmable switches (both the P4 code and the Python-based controller), and the code required to generate and receive the traffic from each of the servers. It also includes the code to process the results and generate the plots in the paper.

* `paper.pdf` contains the latest version of the paper.

**🚀 Quick start:** Check the `README.md` files on the `simulations` and `tofino` folders to find out how to reproduce all the software-based, and hardware-based experiments of the paper, respectively.


 ## Contact

Please, send us an e-mail to: galberto@ethz.ch,
- If you are interested in collaborating with the project.
- If you are having issues when trying to run the experiments described on the paper.
- If you happen to find a bug.
- If you have any other questions or concerns :)
