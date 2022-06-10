# ACC-Turbo

This repository contains the code used in [ACC-Turbo](https://nsg.ee.ethz.ch/fileadmin/user_upload/ACC-Turbo.pdf), which will be presented at [SIGCOMM'22](https://conferences.sigcomm.org/sigcomm/2022/).

## What can I find in this repo?

* `simulations` contains the code of all the experiments for **Section 2 (Background)** and **Section 8 (Simulation-based Evaluation)** of the paper. It includes an implementation of ACC-Turbo on Python and the experiments on [NetBench](https://github.com/ndal-eth/netbench).

* `tofino` contains the code of all the experiments for **Section 7 (Hardware-based Evaluation)** of the paper. It includes the code to run ACC-Turbo on programmable switches (both the P4 code and the Python-based controller), and the code required to generate and receive the traffic from each of the servers. It also includes the code to process the results and generate the plots in the paper.

* `paper.pdf` contains the latest version of the paper.

## Structure

```
ACC-Turbo
├── simulations 
│   │
│   ├── netbench
│   │    ├── projects/accturbo
│   │    │   ├── runs
│   │    │   └── analysis
│   │    └── src/main/java/ch/ethz/systems/netbench/xpt/ports
│   │        ├── ACC
│   │        └── ACCTurbo
│   │
│   ├── python
│   │    ├── main.py
│   │    ├── clustering
│   │    └── plots
│   │
│   ├── run_fig_x.sh
│   │
│   └── README.md. 
│
├── tofino
│   │
│   ├── bfrt
│   ├── p4src
│   ├── pd_rpc
│   ├── python_controller
│   │
│   ├── experiment
│   │    ├── sender
│   │    └── receiver
│   │
│   ├── run_fig_x/run_fig_x.sh
│   └── README.md. 
│   
└── paper.pdf
```


 ## Contact

Please, contact us:
- If you are interested in collaborating with the project.
- If you are having issues when trying to run the experiments described on the paper.
- If you happen to find a bug.
- If you have any other questions or concerns :)
