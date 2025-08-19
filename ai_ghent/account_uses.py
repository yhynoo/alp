import os
import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import MultiLabelBinarizer
import joblib
import numpy as np
import random
import warnings
from itertools import combinations

warnings.filterwarnings("ignore")

# -----------------------------
# Load the dataset
# -----------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
with open("data/trainingData_use_less_cereals.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Filtered labels for training ("inventory", "assignment" only)
df["accountType_filtered"] = df["accountType"].apply(
    lambda lbls: [l for l in lbls if l in ["inventory", "assignment"]]
)

texts = df["withNumbers"]

# -----------------------------
# Custom tokenizer (unordered co-occurrence within each line)
# -----------------------------
def cooccurrence_tokenizer(text):
    tokens = []
    for line in text.split("\n"):
        line_tokens = line.strip().split()
        # unigrams
        tokens.extend(line_tokens)
        # unordered bigrams (all pairs within the line)
        tokens.extend([f"{a}_{b}" for a, b in combinations(line_tokens, 2)])
    return tokens

def vectorize_texts(texts):
    vectorizer = TfidfVectorizer(tokenizer=cooccurrence_tokenizer, lowercase=False)
    X = vectorizer.fit_transform(texts)
    return vectorizer, X

# -----------------------------
# Top features
# -----------------------------
def get_top_features(vectorizer, svms, mlb, n=10):
    feature_names = np.array(vectorizer.get_feature_names_out())
    top_features = {}
    for i, label in enumerate(mlb.classes_):
        coef = svms[i].coef_.toarray()[0]
        top_pos_idx = np.argsort(coef)[-n:]
        top_neg_idx = np.argsort(coef)[:n]
        top_features[label] = {
            "positive": [(feature_names[idx], float(coef[idx])) for idx in top_pos_idx],
            "negative": [(feature_names[idx], float(coef[idx])) for idx in top_neg_idx]
        }
    return top_features

def save_to_markdown(feature_importance, model_key):
    os.makedirs("analysis", exist_ok=True)
    path = os.path.join("analysis", f"{model_key}_feature_importance.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Top Features per Label\n\n")
        for label, feats in feature_importance.items():
            f.write(f"## {label}\n\n")
            f.write("### Positive Features:\n")
            for feat, coef in feats["positive"]:
                f.write(f"- **{feat}**: {coef:.2f}\n")
            f.write("\n### Negative Features:\n")
            for feat, coef in feats["negative"]:
                f.write(f"- **{feat}**: {coef:.2f}\n")
            f.write("\n---\n\n")

# -----------------------------
# Train only on inventory/assignment
# -----------------------------
vectorizer, X = vectorize_texts(texts)

mlb = MultiLabelBinarizer(classes=["inventory", "assignment"])

# Build y for all data (so we can later compare)
y_all = mlb.fit_transform(df["accountType_filtered"])

# Train only on rows that have assignment/inventory
mask_train = y_all.sum(axis=1) > 0
X_train = X[mask_train]
y_train = y_all[mask_train]

# Test set = full dataset (all rows, even with no labels)
X_test = X
y_test = y_all
df_test = df

# -----------------------------
# Fit SVMs
# -----------------------------
svms = []
for i in range(y_train.shape[1]):
    svm = SVC(kernel="linear", probability=True)
    svm.fit(X_train, y_train[:, i])
    svms.append(svm)

# -----------------------------
# Save model
# -----------------------------
model_key = "use"
model_dir = os.path.join(script_dir, "svm", model_key)
os.makedirs(model_dir, exist_ok=True)

joblib.dump(svms, os.path.join(model_dir, "svm_models.joblib"))
joblib.dump(vectorizer, os.path.join(model_dir, "tfidf_vectorizer.joblib"))
joblib.dump(mlb, os.path.join(model_dir, "mlb.joblib"))

# -----------------------------
# Evaluation (on all rows)
# -----------------------------
y_probs = np.array([svm.predict_proba(X_test)[:, 1] for svm in svms]).T
threshold = 0.5
y_preds = (y_probs >= threshold).astype(int)

reports = []
for i, label in enumerate(mlb.classes_):
    rep = classification_report(y_test[:, i], y_preds[:, i])
    reports.append(f"Label: {label}\n{rep}")

os.makedirs("reports/training", exist_ok=True)
with open(os.path.join("reports/training", f"{model_key}_accuracy_report.txt"), "w") as f:
    f.write("\n\n".join(reports))

feature_importance = get_top_features(vectorizer, svms, mlb)
save_to_markdown(feature_importance, model_key)

# -----------------------------
# Save 10 random test examples with certainty
# -----------------------------
num_examples = 10
indices = random.sample(range(X_test.shape[0]), num_examples)

examples_path = os.path.join("reports/training", f"{model_key}_sample_predictions.md")
with open(examples_path, "w", encoding="utf-8") as f:
    f.write("# Sample Predictions\n\n")
    for i, idx in enumerate(indices, 1):
        text_sample = df_test.iloc[idx]["withNumbers"]
        true_labels = df_test.iloc[idx]["accountType"]  # show original labels
        pred_labels = []
        pred_certainty = []
        for j in range(len(mlb.classes_)):
            if y_probs[idx, j] >= threshold:
                pred_labels.append(mlb.classes_[j])
                pred_certainty.append(round(y_probs[idx, j], 2))
        f.write(f"## Example {i}\n")
        f.write(f"**Text:**\n```\n{text_sample}\n```\n")
        f.write(f"**True Labels:** {true_labels}\n")
        f.write(f"**Predicted Labels:** {pred_labels}, {pred_certainty}\n\n")

print(f"Model {model_key} - Accuracy Report, Feature Importance, and Sample Predictions with certainty saved.")
