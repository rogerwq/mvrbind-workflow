import sys
import os
import shutil

sys.path.insert(0, "/opt/MVRBind")

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import torch
from sklearn.cluster import KMeans
from torch_geometric.loader import DataLoader
from model import MVRBind
from data_process.set_seed import set_seed
from data_process.get_pdb_feature import TestDataset

IN_DIR  = "inputs"
OUT_DIR = "outputs"

os.makedirs(OUT_DIR, exist_ok=True)

dataset = TestDataset(
    root=os.path.join(IN_DIR, "pt"),
    pdb_file_path=os.path.join(IN_DIR, "pdb"),
    fasta_file_path=os.path.join(IN_DIR, "fasta"),
    msa_file_path=os.path.join(IN_DIR, "aligned"),
    em_file_path=os.path.join(IN_DIR, "em"),
    asa_file_path=os.path.join(IN_DIR, "asa"),
    top_k=8,
    label_file_path="",
    mode="predict"
)

loader = DataLoader(dataset, batch_size=1)
model = MVRBind(136)
model.load_state_dict(torch.load("/opt/MVRBind/model_parameters/model.pt"))
model.eval()

set_seed(1)

results = []
with torch.no_grad():
    for data in loader:
        output = model(data).detach().numpy().reshape(-1, 1)
        if len(output) < 2:
            continue
        kmeans = KMeans(n_clusters=2, random_state=0).fit(output)
        threshold = np.mean(kmeans.cluster_centers_.flatten())
        predictions = (output > threshold).astype(int).flatten().tolist()
        results.append(predictions)

out_path = os.path.join(OUT_DIR, "predictions.txt")
with open(out_path, "w") as f:
    for preds in results:
        f.write(" ".join(map(str, preds)) + "\n")

# 02-report only depends on this job, not on 00-download, so forward the
# fasta it already has here for 02-report to pick up.
shutil.copy(os.path.join(IN_DIR, "fasta", "2JUKA.fasta"), os.path.join(OUT_DIR, "2JUKA.fasta"))

print(f"Predictions written to {out_path}")
for preds in results:
    print(f"binding sites: {preds}")
