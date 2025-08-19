import os
import json
import pandas as pd

# -----------------------------
# Load dataset
# -----------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "data/trainingData_use_less_cereals.json")

with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# -----------------------------
# Define row categories
# -----------------------------
def label_category(lbls):
    lbls = set(lbls)
    if "inventory" in lbls:
        return "inventory"
    elif "assignment" in lbls:
        return "assignment"
    else:
        return "neither"

df["row_label"] = df["accountType"].apply(label_category)

# -----------------------------
# Columns = account types excluding inventory/assignment
# -----------------------------
all_account_types = set()
for types in df["accountType"]:
    for t in types:
        if t not in {"inventory", "assignment"}:
            all_account_types.add(t)
all_account_types = sorted(all_account_types)

# -----------------------------
# Build cross-tab
# -----------------------------
crosstab = pd.DataFrame(0, index=["inventory", "assignment", "neither"], columns=all_account_types)

for row_label in crosstab.index:
    subset = df[df["row_label"] == row_label]
    for col in crosstab.columns:
        crosstab.at[row_label, col] = subset["accountType"].apply(lambda x: 1 if col in x else 0).sum()

# Add totals
crosstab["Total"] = crosstab.sum(axis=1)
crosstab.loc["Total"] = crosstab.sum(axis=0)

# -----------------------------
# Save reports
# -----------------------------
report_dir = os.path.join(script_dir, "reports/training")
os.makedirs(report_dir, exist_ok=True)

# Markdown
md_path = os.path.join(report_dir, "training_data_crosstab.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("# Training Data Cross-Section Summary\n\n")
    f.write(crosstab.to_markdown())