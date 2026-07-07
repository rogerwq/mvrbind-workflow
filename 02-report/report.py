import os
from Bio import SeqIO

IN_DIR   = "inputs"
OUT_DIR  = "outputs"

os.makedirs(OUT_DIR, exist_ok=True)

pred_path = os.path.join(IN_DIR, "predictions.txt")

sequences = []
for fname in sorted(os.listdir(IN_DIR)):
    if fname.endswith(".fasta") or fname.endswith(".fa"):
        for rec in SeqIO.parse(os.path.join(IN_DIR, fname), "fasta"):
            sequences.append((rec.id, str(rec.seq)))

with open(pred_path) as f:
    all_preds = [list(map(int, line.split())) for line in f if line.strip()]

rows = ""
for (seq_id, seq), preds in zip(sequences, all_preds):
    nucleotides = ""
    for i, (nuc, label) in enumerate(zip(seq, preds)):
        color = "#e05c5c" if label == 1 else "#d4edda"
        title = "binding site" if label == 1 else "non-binding"
        nucleotides += (
            f'<span style="background:{color};padding:2px 4px;margin:1px;'
            f'border-radius:3px;font-family:monospace;font-size:14px;" '
            f'title="pos {i+1}: {title}">{nuc}</span>'
        )
    binding_count = sum(preds)
    rows += f"""
    <tr>
      <td style="padding:8px;font-weight:bold;">{seq_id}</td>
      <td style="padding:8px;">{nucleotides}</td>
      <td style="padding:8px;text-align:center;">{binding_count}/{len(preds)}</td>
    </tr>"""

html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>MVRBind — Binding Site Predictions</title>
  <style>
    body {{ font-family: sans-serif; margin: 40px; }}
    h1 {{ color: #333; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th {{ background: #333; color: white; padding: 10px; text-align: left; }}
    tr:nth-child(even) {{ background: #f9f9f9; }}
    .legend {{ margin: 16px 0; font-size: 13px; }}
    .legend span {{ padding: 2px 8px; border-radius: 3px; margin-right: 8px; }}
  </style>
</head>
<body>
  <h1>MVRBind — RNA Binding Site Predictions</h1>
  <p>Per-nucleotide binding site prediction for RNA-small molecule interactions.</p>
  <div class="legend">
    <span style="background:#e05c5c;">A</span> Predicted binding site &nbsp;
    <span style="background:#d4edda;">A</span> Non-binding
  </div>
  <table>
    <thead>
      <tr>
        <th>RNA ID</th>
        <th>Sequence</th>
        <th>Binding sites</th>
      </tr>
    </thead>
    <tbody>{rows}
    </tbody>
  </table>
</body>
</html>"""

out_path = os.path.join(OUT_DIR, "report.html")
with open(out_path, "w") as f:
    f.write(html)

print(f"Report written to {out_path}")
