# Repository review inventory — initial snapshot, 2026-09-07

This is the inventory before documentation updates and HF evidence downloads.
Hashes identify the initial bytes, not the subsequently edited versions.
See [PROJECT_UNDERSTANDING.md](PROJECT_UNDERSTANDING.md) for synthesis,
review scope and limits. Generated duplicates and nonresearch binaries are included;
git internals and audit scratch files are excluded.

| File | Initial bytes | Initial SHA-256 (prefix) | Role / reviewed structure |
|---|---|---|---|
| [.gitignore](.gitignore) | 574 | `e36e4124246d6e02` | Generated files, data roots and scratch exclusions |
| `AGENTS.md` | 47 | `a89f940f05478ce2` | Documentation: Imported Claude Cowork project instructions |
| [benchmark/bench_throughput.py](benchmark/bench_throughput.py) | 21,971 | `ed99b77c80ee3316` | bench_throughput.py -- measure training throughput without going near the edge. |
| [benchmark/convsweep_resnet50_20260812_074341.json](benchmark/convsweep_resnet50_20260812_074341.json) | 1,024 | `c35727bba75d68bb` | Recorded hardware benchmark data |
| [benchmark/README.md](benchmark/README.md) | 7,017 | `c2b658942acc93ce` | Documentation: Throughput benchmark |
| [benchmark/results/bench_CB-410-122_20260808_101635.json](benchmark/results/bench_CB-410-122_20260808_101635.json) | 7,475 | `459a3ba4322ffe41` | Recorded hardware benchmark data |
| [build_notebooks.py](build_notebooks.py) | 149,053 | `80da022994617e1a` | build_notebooks.py -- regenerate the Kaggle notebooks from src/msc_lib.py. |
| [build_notebooks_in100.py](build_notebooks_in100.py) | 89,083 | `f8ed004a5b17acd2` | build_notebooks_in100.py -- generate the five ImageNet-100 notebooks. |
| [build_notebooks_study2.py](build_notebooks_study2.py) | 49,465 | `b263d0c4c154b68c` | build_notebooks_study2.py -- generate the Study 2 notebooks. |
| [build_notebooks_study3.py](build_notebooks_study3.py) | 68,308 | `6d3b691d071185b0` | Generate the Study 3 notebooks. |
| [build_notebooks_study4.py](build_notebooks_study4.py) | 73,863 | `2524f0e68968d213` | Generate the Study 4 notebooks. |
| [CITATION.cff](CITATION.cff) | 777 | `cf1bbbff3a483573` | Software citation metadata |
| [docs/cifar100/00_RESEARCH_PROTOCOL.md](docs/cifar100/00_RESEARCH_PROTOCOL.md) | 30,601 | `abe82676e8faf2c2` | Documentation: Research Protocol v1.0 |
| [docs/cifar100/01_PHASE0_GO_NOGO.md](docs/cifar100/01_PHASE0_GO_NOGO.md) | 7,164 | `2799273922affa4b` | Documentation: Phase 0 — Decisive Pilot |
| [docs/cifar100/02_ENGINEERING_SPEC.md](docs/cifar100/02_ENGINEERING_SPEC.md) | 15,093 | `22a7d53696b4d57c` | Documentation: Engineering Specification |
| [docs/cifar100/03_IMPLEMENTATION_PLAN.md](docs/cifar100/03_IMPLEMENTATION_PLAN.md) | 24,131 | `7fa70af5a4ad6678` | Documentation: Implementation Plan — MSC |
| [docs/cifar100/04_NOTEBOOK_RUNBOOK.md](docs/cifar100/04_NOTEBOOK_RUNBOOK.md) | 24,005 | `dd964da0630bb1e0` | Documentation: Notebook Runbook |
| [docs/cifar100/05_PLAIN_ENGLISH_GUIDE.md](docs/cifar100/05_PLAIN_ENGLISH_GUIDE.md) | 26,620 | `66b32ba5ec81dfdf` | Documentation: What We Are Doing, In Plain English |
| [docs/cifar100/06_DATA_SCHEMA.md](docs/cifar100/06_DATA_SCHEMA.md) | 14,866 | `59a894e9d86ec3a4` | Documentation: Repository Structure & Data Schema |
| [docs/cifar100/07_REPLICATION_PLAYBOOK.md](docs/cifar100/07_REPLICATION_PLAYBOOK.md) | 33,210 | `547f55c276f1db1e` | Documentation: Replication Playbook |
| [docs/cifar100/08_PHASE0_RESULTS.md](docs/cifar100/08_PHASE0_RESULTS.md) | 9,751 | `3c78f1a160b6c14f` | Documentation: Phase 0 Results |
| [docs/cifar100/09_LAB_NOTEBOOK.md](docs/cifar100/09_LAB_NOTEBOOK.md) | 126,796 | `41cc45c7725264c4` | Documentation: Lab Notebook |
| [docs/cifar100/10_FINAL_RESULTS.md](docs/cifar100/10_FINAL_RESULTS.md) | 12,408 | `03162077c68786f5` | Documentation: Final Results — Minimum Sufficient Compute |
| [docs/imagenet100/20_IN100_PORT_PLAN.md](docs/imagenet100/20_IN100_PORT_PLAN.md) | 24,011 | `a142342fea791d16` | Documentation: ImageNet-100 Port — Design and Run Matrix |
| [docs/imagenet100/21_IN100_ENGINEERING_DELTA.md](docs/imagenet100/21_IN100_ENGINEERING_DELTA.md) | 13,409 | `c43c0325499780c9` | Documentation: Engineering Delta — CIFAR-100 → ImageNet-100 |
| [docs/imagenet100/22_IN100_LAB_NOTEBOOK.md](docs/imagenet100/22_IN100_LAB_NOTEBOOK.md) | 169,275 | `2b19ea4752b26590` | Documentation: Lab Notebook — ImageNet-100 Port |
| [docs/imagenet100/23_IN100_RUNBOOK.md](docs/imagenet100/23_IN100_RUNBOOK.md) | 26,050 | `e17929adedd3136f` | Documentation: ImageNet-100 Runbook |
| [docs/imagenet100/24_IN100_STATUS.md](docs/imagenet100/24_IN100_STATUS.md) | 15,683 | `bfbf7abc8e748e51` | Documentation: ImageNet-100 — LIVE STATUS |
| [docs/imagenet100/25_IN100_DATA_CARD.md](docs/imagenet100/25_IN100_DATA_CARD.md) | 10,846 | `01e7a2c61f582c68` | Documentation: Data Card — ImageNet-100 (this project's subset) |
| [docs/imagenet100/26_IN100_FINDINGS.md](docs/imagenet100/26_IN100_FINDINGS.md) | 8,193 | `74e29a940fc63eda` | Documentation: ImageNet-100 — FINDINGS |
| [LICENSE](LICENSE) | 1,073 | `b3d30bc0c6782900` | MIT software license |
| [msc_core.py](msc_core.py) | 20,703 | `2cc4ba5e09354335` | msc_core.py -- Minimum Sufficient Compute: oracle and analysis statistics. |
| [msc_torch.py](msc_torch.py) | 11,773 | `2c09ffea219692ae` | msc_torch.py -- model-side components for MSC-KD. |
| `notebooks/Microsoft.Services.Store.winmd` | 5,120 | `45715793b8c85715` | Windows binary metadata; unrelated to research; not executed |
| [notebooks/NB00_Setup_And_Verify.ipynb](notebooks/NB00_Setup_And_Verify.ipynb) | 742,177 | `c157e26c16df5267` | Generated notebook; 19 cells (9 code, 10 Markdown); parsed, not GPU-executed |
| [notebooks/NB01_Phase0_Train.ipynb](notebooks/NB01_Phase0_Train.ipynb) | 738,509 | `4842b1b126b5e6c8` | Generated notebook; 17 cells (8 code, 9 Markdown); parsed, not GPU-executed |
| [notebooks/NB02_Phase0_Measure.ipynb](notebooks/NB02_Phase0_Measure.ipynb) | 739,140 | `322e7b39cf05db77` | Generated notebook; 15 cells (7 code, 8 Markdown); parsed, not GPU-executed |
| [notebooks/NB03_Phase0_Decision.ipynb](notebooks/NB03_Phase0_Decision.ipynb) | 745,217 | `dd2d435a471d6969` | Generated notebook; 23 cells (11 code, 12 Markdown); parsed, not GPU-executed |
| [notebooks/NB04_Atlas_Train_ResNets.ipynb](notebooks/NB04_Atlas_Train_ResNets.ipynb) | 739,184 | `788fe319508bd835` | Generated notebook; 18 cells (10 code, 8 Markdown); parsed, not GPU-executed |
| [notebooks/NB05_Atlas_Train_WRN_VGG.ipynb](notebooks/NB05_Atlas_Train_WRN_VGG.ipynb) | 739,107 | `85158c326d7d55dd` | Generated notebook; 18 cells (10 code, 8 Markdown); parsed, not GPU-executed |
| [notebooks/NB06_Atlas_Train_Mobile.ipynb](notebooks/NB06_Atlas_Train_Mobile.ipynb) | 738,828 | `ae90234eca188a91` | Generated notebook; 18 cells (10 code, 8 Markdown); parsed, not GPU-executed |
| [notebooks/NB07_Atlas_Train_Modern.ipynb](notebooks/NB07_Atlas_Train_Modern.ipynb) | 739,459 | `f1c445f3c6febf68` | Generated notebook; 18 cells (10 code, 8 Markdown); parsed, not GPU-executed |
| [notebooks/NB08_Atlas_Measure.ipynb](notebooks/NB08_Atlas_Measure.ipynb) | 736,662 | `cb359b326f373a67` | Generated notebook; 17 cells (8 code, 9 Markdown); parsed, not GPU-executed |
| [notebooks/NB09_Analysis_Q1_NoiseCeiling.ipynb](notebooks/NB09_Analysis_Q1_NoiseCeiling.ipynb) | 736,395 | `8f324159ed1eb659` | Generated notebook; 14 cells (7 code, 7 Markdown); parsed, not GPU-executed |
| [notebooks/NB10_Analysis_Q2_AxisStructure.ipynb](notebooks/NB10_Analysis_Q2_AxisStructure.ipynb) | 738,817 | `4f00272ea3c97fe9` | Generated notebook; 14 cells (7 code, 7 Markdown); parsed, not GPU-executed |
| [notebooks/NB11_Analysis_Q3_Transfer.ipynb](notebooks/NB11_Analysis_Q3_Transfer.ipynb) | 742,595 | `c084eb5ba6d85ec8` | Generated notebook; 18 cells (9 code, 9 Markdown); parsed, not GPU-executed |
| [notebooks/NB12_Analysis_Q4_Irreducibility.ipynb](notebooks/NB12_Analysis_Q4_Irreducibility.ipynb) | 739,807 | `d9f5c38971fb6a73` | Generated notebook; 14 cells (7 code, 7 Markdown); parsed, not GPU-executed |
| [notebooks/NB13_Method_MSCKD_Train.ipynb](notebooks/NB13_Method_MSCKD_Train.ipynb) | 740,661 | `07f03a756bd8c473` | Generated notebook; 16 cells (8 code, 8 Markdown); parsed, not GPU-executed |
| [notebooks/NB14_Method_Comparison.ipynb](notebooks/NB14_Method_Comparison.ipynb) | 745,918 | `2432a878424c0219` | Generated notebook; 18 cells (9 code, 9 Markdown); parsed, not GPU-executed |
| [notebooks/NB15_Paper_Outputs.ipynb](notebooks/NB15_Paper_Outputs.ipynb) | 833,597 | `13e07528d6091542` | Generated notebook; 22 cells (11 code, 11 Markdown); parsed, not GPU-executed |
| [notebooks/NB16_Fix_Gaps.ipynb](notebooks/NB16_Fix_Gaps.ipynb) | 741,922 | `4fbf17561ef2cf78` | Generated notebook; 19 cells (9 code, 10 Markdown); parsed, not GPU-executed |
| [notebooks_in100/msc_core.py](notebooks_in100/msc_core.py) | 20,735 | `4cd0dfe5f06cd2d5` | Generated adjacent core copy; compare to root source when rebuilding |
| [notebooks_in100/NB1_Setup.ipynb](notebooks_in100/NB1_Setup.ipynb) | 1,232,001 | `f132c23e43fe4001` | Generated notebook; 17 cells (9 code, 8 Markdown); parsed, not GPU-executed |
| [notebooks_in100/NB2_Train.ipynb](notebooks_in100/NB2_Train.ipynb) | 1,225,391 | `7eb9cefa92702076` | Generated notebook; 11 cells (6 code, 5 Markdown); parsed, not GPU-executed |
| [notebooks_in100/NB3_Measure.ipynb](notebooks_in100/NB3_Measure.ipynb) | 1,219,542 | `700cfc49ccf9ab7b` | Generated notebook; 8 cells (6 code, 2 Markdown); parsed, not GPU-executed |
| [notebooks_in100/NB4_Analysis.ipynb](notebooks_in100/NB4_Analysis.ipynb) | 1,233,740 | `0b4c2112ebeab40a` | Generated notebook; 19 cells (13 code, 6 Markdown); parsed, not GPU-executed |
| [notebooks_in100/NB5_Method.ipynb](notebooks_in100/NB5_Method.ipynb) | 1,228,655 | `0199ce0a08c094f4` | Generated notebook; 12 cells (8 code, 4 Markdown); parsed, not GPU-executed |
| [notebooks_in100/NB6_Publish.ipynb](notebooks_in100/NB6_Publish.ipynb) | 1,240,253 | `41fdabe2147c4295` | Generated notebook; 12 cells (7 code, 5 Markdown); parsed, not GPU-executed |
| [notebooks_study2/msc_core.py](notebooks_study2/msc_core.py) | 20,735 | `4cd0dfe5f06cd2d5` | Generated adjacent core copy; compare to root source when rebuilding |
| [notebooks_study2/S2_NB0_Fetch.ipynb](notebooks_study2/S2_NB0_Fetch.ipynb) | 1,271,956 | `b6a6858db843c971` | Generated notebook; 10 cells (6 code, 4 Markdown); parsed, not GPU-executed |
| [notebooks_study2/S2_NB1_Reliability.ipynb](notebooks_study2/S2_NB1_Reliability.ipynb) | 1,283,761 | `5e69fd0dc5c8045b` | Generated notebook; 13 cells (7 code, 6 Markdown); parsed, not GPU-executed |
| [notebooks_study2/S2_NB2_Ceiling.ipynb](notebooks_study2/S2_NB2_Ceiling.ipynb) | 1,299,072 | `8da51a79a76457e3` | Generated notebook; 16 cells (9 code, 7 Markdown); parsed, not GPU-executed |
| [notebooks_study3/msc_core.py](notebooks_study3/msc_core.py) | 20,703 | `2cc4ba5e09354335` | Generated adjacent core copy; compare to root source when rebuilding |
| [notebooks_study3/S3_NB0_Extrapolate.ipynb](notebooks_study3/S3_NB0_Extrapolate.ipynb) | 1,277,517 | `1e6994ae02d709f4` | Generated notebook; 11 cells (6 code, 5 Markdown); parsed, not GPU-executed |
| [notebooks_study3/S3_NB1_JointTrain.ipynb](notebooks_study3/S3_NB1_JointTrain.ipynb) | 1,279,327 | `5d083d6f76c0b429` | Generated notebook; 15 cells (9 code, 6 Markdown); parsed, not GPU-executed |
| [notebooks_study3/S3_NB2_Compare.ipynb](notebooks_study3/S3_NB2_Compare.ipynb) | 1,276,777 | `77b3e7de59beb0d6` | Generated notebook; 12 cells (7 code, 5 Markdown); parsed, not GPU-executed |
| [notebooks_study3/S3_NB3_Router.ipynb](notebooks_study3/S3_NB3_Router.ipynb) | 1,281,411 | `cbcbbb6c3dbc30d7` | Generated notebook; 14 cells (9 code, 5 Markdown); parsed, not GPU-executed |
| [notebooks_study3/S3_NB4_Pruning.ipynb](notebooks_study3/S3_NB4_Pruning.ipynb) | 1,279,507 | `a6bafa20f029cb90` | Generated notebook; 14 cells (9 code, 5 Markdown); parsed, not GPU-executed |
| [notebooks_study3/S3_NB5_Publish.ipynb](notebooks_study3/S3_NB5_Publish.ipynb) | 1,273,162 | `2362c5e72b92e0bc` | Generated notebook; 11 cells (6 code, 5 Markdown); parsed, not GPU-executed |
| [notebooks_study4/S4_NB0_Figures.ipynb](notebooks_study4/S4_NB0_Figures.ipynb) | 1,275,223 | `aab2acd235e04984` | Generated notebook; 13 cells (7 code, 6 Markdown); parsed, not GPU-executed |
| [notebooks_study4/S4_NB1_Baselines.ipynb](notebooks_study4/S4_NB1_Baselines.ipynb) | 1,285,369 | `2d69bf599373543b` | Generated notebook; 16 cells (9 code, 7 Markdown); parsed, not GPU-executed |
| [notebooks_study4/S4_NB2_ImageNet.ipynb](notebooks_study4/S4_NB2_ImageNet.ipynb) | 1,273,318 | `8bb79b07004f3472` | Generated notebook; 15 cells (8 code, 7 Markdown); parsed, not GPU-executed |
| [notebooks_study4/S4_NB3_Publish.ipynb](notebooks_study4/S4_NB3_Publish.ipynb) | 1,288,550 | `63e961860c9475a1` | Generated notebook; 12 cells (7 code, 5 Markdown); parsed, not GPU-executed |
| [notebooks_study4/S4_NB4_MSDNet.ipynb](notebooks_study4/S4_NB4_MSDNet.ipynb) | 1,596,238 | `3770164da5496a44` | Generated notebook; 25 cells (14 code, 11 Markdown); parsed, not GPU-executed |
| [PAPER.md](PAPER.md) | 30,845 | `5ac613c920708acf` | Documentation: How Much Computation Does an Image Need? A Noise-Ceiling-Corrected Atlas of Per-Sample Compute Requirements Across Fifteen Architectures |
| [PAPER_CLAIM.md](PAPER_CLAIM.md) | 16,252 | `7a9b8ce188fd0fa3` | Documentation: What we can claim, and what it takes to publish it |
| [README.md](README.md) | 13,588 | `94acb3e4752def9c` | Documentation: Minimum Sufficient Compute (MSC) |
| [requirements.txt](requirements.txt) | 2,802 | `c1b2df8f4cd3da7d` | Runtime dependencies and installation notes |
| [RESULTS.csv](RESULTS.csv) | 5,790 | `09b4e757fba15afd` | Generated headline-result table |
| [RESULTS.md](RESULTS.md) | 6,667 | `832c30667cc441e6` | Documentation: Results — every headline number, generated from the artifacts |
| `src/__pycache__/msc_lib.cpython-310.pyc` | 337,244 | `a5a7da97b0a90e2b` | Generated Python bytecode cache; not executed |
| [src/msc_lib.py](src/msc_lib.py) | 779,063 | `f737f75f9303a552` | msc_lib.py -- Minimum Sufficient Compute: full Kaggle/HuggingFace pipeline. |
| [study2/01_POSTMORTEM.md](study2/01_POSTMORTEM.md) | 5,581 | `c1114244772c3fcf` | Documentation: Why Study 1 fell short |
| [study2/02_PROTOCOL.md](study2/02_PROTOCOL.md) | 8,762 | `f59cf0220d8d487a` | Documentation: Study 2 — pre-registration |
| [study2/03_INVENTORY.md](study2/03_INVENTORY.md) | 6,465 | `36076a349e95803b` | Documentation: What already exists |
| [study2/04_DESIGN.md](study2/04_DESIGN.md) | 6,219 | `acaf878845582ca2` | Documentation: Study 2 — the plan |
| [study2/05_OPEN_DECISIONS.md](study2/05_OPEN_DECISIONS.md) | 7,563 | `9d759ce4c4bfb5a1` | Documentation: Decisions — settled |
| [study2/06_RISK_REGISTER.md](study2/06_RISK_REGISTER.md) | 10,736 | `0db4a7fe0275984f` | Documentation: Risk register — how this study fails, and what stops it |
| [study2/07_PROGRESS.md](study2/07_PROGRESS.md) | 22,701 | `c375717630b3f669` | Documentation: Study 2 — progress log |
| [study2/08_RELATED_WORK.md](study2/08_RELATED_WORK.md) | 8,463 | `0eea6b4283811c1c` | Documentation: Related work — what exists, and where the gap is |
| [study2/PAPER.md](study2/PAPER.md) | 20,799 | `d74fcc37010df3c7` | Documentation: Oracle upper bounds for early-exit routing are inflated by per-exit noise |
| [study2/README.md](study2/README.md) | 7,652 | `769e07dfccf675b8` | Documentation: Study 2 — complete |
| [study3/01_PROTOCOL.md](study3/01_PROTOCOL.md) | 10,299 | `34097ffba240a317` | Documentation: Study 3 — pre-registration |
| [study3/02_RISKS.md](study3/02_RISKS.md) | 6,988 | `a1f45fea81e8e213` | Documentation: Study 3 — risk register |
| [study3/03_LOG.md](study3/03_LOG.md) | 36,251 | `aadf19eed5b15056` | Documentation: Study 3 — live log |
| [study3/04_FINDINGS.md](study3/04_FINDINGS.md) | 10,163 | `d58a40eaa7664661` | Documentation: Study 3 — findings |
| [study3/README.md](study3/README.md) | 8,003 | `2959a4a0488d9309` | Documentation: Study 3 — complete |
| [study4/01_PROTOCOL.md](study4/01_PROTOCOL.md) | 10,124 | `84f965d2029dd267` | Documentation: Study 4 — pre-registration |
| [study4/02_RISKS.md](study4/02_RISKS.md) | 6,359 | `93047e28cb16cfc3` | Documentation: Study 4 — risk register |
| [study4/03_LOG.md](study4/03_LOG.md) | 19,011 | `53410c8aaef814df` | Documentation: Study 4 — live log |
| [study4/README.md](study4/README.md) | 7,514 | `53f7937cbf130662` | Documentation: Study 4 — plan |
| [tools/bisect_speed.py](tools/bisect_speed.py) | 11,055 | `b2b4675bc6701d9c` | bisect_speed.py -- stop theorising. Time each stage separately. |
| [tools/build_results.py](tools/build_results.py) | 10,474 | `f54160ac534290eb` | Regenerate RESULTS.md and RESULTS.csv from the analysis CSVs. |
| [tools/check_links.py](tools/check_links.py) | 2,510 | `1be9cd75ac0fa550` | check_links.py -- every document reference in the repo must resolve. |
| [tools/check_names.py](tools/check_names.py) | 9,505 | `5be82a8065ffe421` | check_names.py -- a name used in a function that is defined nowhere. |
| [tools/conv_sweep.py](tools/conv_sweep.py) | 8,195 | `9e65520a90e91950` | conv_sweep.py -- why is ResNet-50 7.5x slower than ViT-S at the same FLOPs? |
| [tools/diagnose_epochs.py](tools/diagnose_epochs.py) | 6,992 | `358fdd2fdb40770b` | diagnose_epochs.py -- where did the epoch time actually go? |
| [tools/fetch_assets.py](tools/fetch_assets.py) | 13,877 | `d322d5d7f92f3b20` | fetch_assets.py -- run ONCE with internet. Everything after that runs offline. |
| [tools/pack_imagenet100.py](tools/pack_imagenet100.py) | 18,041 | `207fa8329b3e81fb` | pack_imagenet100.py -- turn 129,395 loose JPEGs into one packed uint8 memmap, |
| [tools/s2_canaries.py](tools/s2_canaries.py) | 2,241 | `c81ec0ba1f02d469` | Canaries for the S2_NB1 statistics: each must be shown CAPABLE of |
| [tools/s2_cell_harness.py](tools/s2_cell_harness.py) | 3,795 | `8e24fe7d5236e77d` | Execute S2_NB1's real notebook cells against synthetic frames that |
| [tools/s2_routing_canaries.py](tools/s2_routing_canaries.py) | 9,592 | `44b42fa7bb7068ba` | Canaries for route_by / route_confidence in S2_NB2. |
| [tools/s3_canaries.py](tools/s3_canaries.py) | 13,537 | `b1ff0819dc474397` | Canaries for Study 3's new library code. |
| [tools/s3_nb0_harness.py](tools/s3_nb0_harness.py) | 3,669 | `361bd8daed5427de` | Execute S3_NB0's real analysis cells against synthetic frames. |
| [tools/s3_nb3_harness.py](tools/s3_nb3_harness.py) | 5,380 | `449b37d92aab5304` | Execute S3_NB3's real cells against synthetic frames. |
| [tools/s4_harness.py](tools/s4_harness.py) | 12,246 | `f301b73a15359b90` | Execute S4_NB0 and S4_NB1's real cells against synthetic data. |
| [tools/s4_msdnet_canaries.py](tools/s4_msdnet_canaries.py) | 16,363 | `5c651c5ec83b4492` | Canaries for MSDNet's channel arithmetic -- and for the canaries themselves. |
| [tools/validate_notebooks.py](tools/validate_notebooks.py) | 49,506 | `aef51fb1f2d69cbe` | validate_notebooks.py -- refuse to ship a notebook that names a column or a |
| [tools/verify_d55.py](tools/verify_d55.py) | 8,365 | `ff52f9260b40094b` | verify_d55.py -- measure what the memory-format fix is actually worth. |
| [tools/verify_loader.py](tools/verify_loader.py) | 6,141 | `0680a7d587627d52` | verify_loader.py -- is the input pipeline the bottleneck, and does RAM fix it? |

Total: **120 initial files**. Complete hashes are retained in [the initial inventory](docs/evidence/hf_2026-09-07/repository_inventory.json).

The binary and ignored generated-file links refer to the local checkout; those files are not added to version control by this audit.
