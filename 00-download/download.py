import shutil
import os

SRC_DATA = "/opt/MVRBind/data_process/data"
SRC_PT   = "/opt/MVRBind/pt/2JUKA_pt"
OUT_DIR  = "outputs"

os.makedirs(OUT_DIR, exist_ok=True)

dirs = ["pdb", "fasta", "aligned", "em", "asa"]
for d in dirs:
    src = os.path.join(SRC_DATA, d)
    dst = os.path.join(OUT_DIR, d)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f"Copied {src} -> {dst}")

pt_dst = os.path.join(OUT_DIR, "pt")
if os.path.exists(pt_dst):
    shutil.rmtree(pt_dst)
shutil.copytree(SRC_PT, pt_dst)
print(f"Copied {SRC_PT} -> {pt_dst}")
