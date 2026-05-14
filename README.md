# MVRBind Workflow

Silva-compatible workflow for RNA-small molecule binding site prediction using [MVRBind](https://github.com/cschen-y/MVRBind).

> **Paper**: [MVRBind: Multi-view Learning for RNA-Small Molecule Binding Site Prediction](https://academic.oup.com/bib/article/26/5/bbaf489/8260790), *Briefings in Bioinformatics*, 2025

## Overview

Per-nucleotide binary classification of RNA binding sites using a multi-view graph convolutional network that integrates primary, secondary, and tertiary structural information.

This workflow runs the pre-packaged **2JUKA** example included in the MVRBind repository.

## Nodes

```
00-download → 01-predict → 02-report
```

| Node | Description | Output |
|---|---|---|
| `00-download` | Copies pre-packaged 2JUKA data from the MVRBind container | PDB, FASTA, MSA, embeddings, SASA, pt |
| `01-predict` | Runs MVRBind per-nucleotide binding site prediction | `predictions.txt` |
| `02-report` | Generates color-coded HTML report | `report.html` |

## Requirements

- [Silva](https://github.com/chiral-data/silva)
- Docker with NVIDIA runtime (CUDA 12.1, ~6 GB VRAM)
- Image: `ghcr.io/chiral-data/mvrbind:2026_05_14`

## Usage

```bash
silva /path/to/mvrbind-workflow
```

### Example output (`predictions.txt`)

```
>2JUKA
GGCCUUCCCACAAGGGAAGGCC
binding sites: [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

Nucleotides 9–12 (`ACAA`) are predicted as binding sites.

## About MVRBind

MVRBind integrates three structural views via multi-head cross-attention:

- **Primary**: RNABERT embeddings + ClustalW evolutionary conservation
- **Secondary**: RNApdbee base-pairing annotations
- **Tertiary**: RNAsnap2 SASA + 3D k-NN graph

Key results: AUC 0.756 on apo-form RNA (vs. RNABind 0.657), 1.47M parameters, 0.18 s inference.

## Limitations

The 2JUKA example uses pre-computed features bundled in the MVRBind repo. Running on a new RNA target requires:

1. PDB download and chain extraction
2. ClustalW multiple sequence alignment
3. RNApdbee secondary structure (web service: http://rnapdbee.cs.put.poznan.pl/)
4. RNABERT embeddings ([repo](https://github.com/mana438/RNABERT))
5. RNAsnap2 SASA features ([repo](https://github.com/jaswindersingh2/RNAsnap2))
