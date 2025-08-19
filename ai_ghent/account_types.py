import os
import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import MultiLabelBinarizer
import joblib
import numpy as np
import random
import warnings
from itertools import combinations

warnings.filterwarnings("ignore")

# -----------------------------
# Load dataset
# -----------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
with open("data/trainingData_use_less_cereals.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Extract type and other labels (exclude 'economic')
def process_labels(lbls):
    type_label = None
    if "inventory" in lbls:
        type_label = "inventory"
    elif "assignment" in lbls:
        type_label = "assignment"
    other_labels = [l for l in lbls if l not in ["economic", "inventory", "assignment"]]
    return type_label, other_labels

df[["type_label", "other_labels"]] = df["accountType"].apply(lambda x: pd.Series(process_labels(x)))
df = df.dropna(subset=["type_label"])

# Split by type
type_groups = df.groupby("type_label")

# -----------------------------
# Tokenizer: unigrams + unordered bigrams per line
# -----------------------------
def cooccurrence_tokenizer(text):
    tokens = []
    for line in text.split("\n"):
        line_tokens = line.strip().split()
        tokens.extend(line_tokens)  # unigrams
        tokens.extend([f"{a}_{b}" for a, b in combinations(line_tokens, 2)])  # unordered bigrams
    return tokens

def vectorize_texts(texts):
    vectorizer = TfidfVectorizer(tokenizer=cooccurrence_tokenizer, lowercase=False)
    X = vectorizer.fit_transform(texts)
    return vectorizer, X

# -----------------------------
# Get top features
# -----------------------------
def get_top_features(vectorizer, svms, mlb, n=10):
    feature_names = np.array(vectorizer.get_feature_names_out())
    top_features = {}
    for i, label in enumerate(mlb.classes_):
        coefficients = svms[i].coef_.toarray()[0]
        top_positive_idx = np.argsort(coefficients)[-n:]
        top_negative_idx = np.argsort(coefficients)[:n]
        top_features[label] = {
            'positive': [(feature_names[idx], float(coefficients[idx])) for idx in top_positive_idx],
            'negative': [(feature_names[idx], float(coefficients[idx])) for idx in top_negative_idx]
        }
    return top_features

# -----------------------------
# Save features to markdown
# -----------------------------
def save_to_markdown(feature_importance, model_key):
    feature_importance_dir = "analysis"
    os.makedirs(feature_importance_dir, exist_ok=True)
    filename = os.path.join(feature_importance_dir, f"{model_key}_feature_importance.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Top Features per Label\n\n")
        for label, features in feature_importance.items():
            f.write(f"## {label}\n\n")
            f.write("### Positive Features:\n")
            for feat, coef in features['positive']:
                f.write(f"- **{feat}**: {coef:.2f}\n")
            f.write("\n### Negative Features:\n")
            for feat, coef in features['negative']:
                f.write(f"- **{feat}**: {coef:.2f}\n")
            f.write("\n---\n\n")

# -----------------------------
# Train models for each type
# -----------------------------
for type_label, group_df in type_groups:
    print(f"\n=== Training for type: {type_label} ===")
    
    texts = group_df["withNumbers"].tolist()
    labels_list = group_df["other_labels"].tolist()
    
    # Drop rows with no other labels
    mask = [len(lbls) > 0 for lbls in labels_list]
    texts = [texts[i] for i, keep in enumerate(mask) if keep]
    labels_list = [labels_list[i] for i, keep in enumerate(mask) if keep]

    if len(texts) == 0:
        print(f"No rows with other labels for type {type_label}, skipping...")
        continue
    
    # Vectorize
    vectorizer, X = vectorize_texts(texts)
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(labels_list)
    
    # Train-test split (keep indices to recover text samples)
    indices = np.arange(len(texts))
    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X, y, indices, test_size=0.3, random_state=42
    )
    
    # Train SVMs
    svms = []
    for i in range(y_train.shape[1]):
        svm = SVC(kernel='linear', probability=True)
        svm.fit(X_train, y_train[:, i])
        svms.append(svm)
    
    # Save models and vectorizer
    model_key = f"{type_label}"
    model_dir = os.path.join(script_dir, "svm", model_key)
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(svms, os.path.join(model_dir, "svm_models.joblib"))
    joblib.dump(vectorizer, os.path.join(model_dir, "tfidf_vectorizer.joblib"))
    joblib.dump(mlb, os.path.join(model_dir, "mlb.joblib"))
    
    # Evaluation
    y_preds = [svm.predict(X_test) for svm in svms]
    reports = []
    for i, lbl in enumerate(mlb.classes_):
        reports.append(f"Label: {lbl}\n{classification_report(y_test[:, i], y_preds[i])}")
    
    os.makedirs("reports/training", exist_ok=True)
    report_path = os.path.join("reports/training", f"{model_key}_accuracy_report.txt")
    with open(report_path, "w") as f:
        f.write("\n\n".join(reports))
    
    # Feature importance
    feature_importance = get_top_features(vectorizer, svms, mlb)
    save_to_markdown(feature_importance, model_key)
    
    # -----------------------------
    # Save 25 random test examples with certainty
    # -----------------------------
    num_examples = min(25, X_test.shape[0])
    sample_indices = random.sample(range(X_test.shape[0]), num_examples)
    examples_path = os.path.join("reports/training", f"{model_key}_sample_predictions.md")

    with open(examples_path, "w", encoding="utf-8") as f:
        f.write("# Sample Predictions with Certainty\n\n")
        for i, idx in enumerate(sample_indices, 1):
            text_sample = texts[idx_test[idx]]
            true_labels = labels_list[idx_test[idx]]

            pred_labels = []
            pred_certainty = []
            for j, svm in enumerate(svms):
                prob = svm.predict_proba(X_test[idx])[0][1]  # probability of positive class
                if prob >= 0.5:  # threshold
                    pred_labels.append(mlb.classes_[j])
                    pred_certainty.append(round(prob, 2))

            f.write(f"## Example {i}\n")
            f.write(f"**Text:**\n```\n{text_sample}\n```\n")
            f.write(f"**True Labels:** {true_labels}\n")
            f.write(f"**Predicted Labels:** {pred_labels}\n")
            f.write(f"**Certainty:** {pred_certainty}\n\n")

    print(f"Saved model, reports, features, and sample predictions for {model_key}")
