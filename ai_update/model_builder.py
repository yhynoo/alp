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

import warnings
warnings.filterwarnings("ignore")

# Load the dataset
script_dir = os.path.dirname(os.path.abspath(__file__))
with open("data/trainingData.json") as f:
    data = json.load(f)

# Convert data to a pandas DataFrame
df = pd.DataFrame(data)

# Extract labels and text versions
labels = df["accountType"]
texts_with_numbers = df["withNumbers"]
texts_without_numbers = df["withoutNumbers"]

# Define a function for vectorization based on a given splitter
def vectorize_texts(texts, splitter):
    if splitter == "space":
        vectorizer = TfidfVectorizer(token_pattern=r"(?u)\S+", ngram_range=(1, 2))
    elif splitter == "newline":
        vectorizer = TfidfVectorizer(token_pattern=r"(?u)[^\n]+", ngram_range=(1, 2))
    return vectorizer, vectorizer.fit_transform(texts)

# Define function to get top features
def get_top_features(vectorizer, svms, mlb, n=10):
    feature_names = np.array(vectorizer.get_feature_names_out())
    top_features = {}

    for i, label in enumerate(mlb.classes_):
        coefficients = svms[i].coef_.toarray()[0]
        top_positive_idx = np.argsort(coefficients)[-n:]
        top_negative_idx = np.argsort(coefficients)[:n]

        top_features[label] = {
            'positive': [(feature_names[idx], float(coefficients[idx])) for idx in top_positive_idx],  # Ensure float
            'negative': [(feature_names[idx], float(coefficients[idx])) for idx in top_negative_idx]
        }

    return top_features

# Define function to save feature importance to markdown
def save_to_markdown(feature_importance, model_key):
    feature_importance_dir = "analysis"
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

# Create a dictionary to hold the models, vectorizers, and label binarizers
models = {}

# Process all four combinations
for text_version, texts in [("with_numbers", texts_with_numbers), ("without_numbers", texts_without_numbers)]:
    for splitter in ["space", "newline"]:
        # Vectorize the text
        vectorizer, X = vectorize_texts(texts, splitter)

        # Transform labels into binary form
        mlb = MultiLabelBinarizer()
        y = mlb.fit_transform(labels)

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=14)

        # Train the model for each label separately
        svms = []
        for i in range(y_train.shape[1]):
            svm = SVC(kernel='linear', probability=True)
            svm.fit(X_train, y_train[:, i])
            svms.append(svm)

        # Save the model and associated components
        model_key = f"{text_version}_{splitter}"
        models[model_key] = {
            "svms": svms,
            "vectorizer": vectorizer,
            "mlb": mlb
        }

        # Save to disk
        model_dir = os.path.join(script_dir, 'svm', model_key)
        os.makedirs(model_dir, exist_ok=True)
        os.makedirs('svm', exist_ok=True)

        joblib.dump(svms, os.path.join(model_dir, 'svm_models.joblib'))
        joblib.dump(vectorizer, os.path.join(model_dir, 'tfidf_vectorizer.joblib'))
        joblib.dump(mlb, os.path.join(model_dir, 'mlb.joblib'))

        # Evaluation
        y_preds = []
        for svm in svms:
            y_pred = svm.predict(X_test)
            y_preds.append(y_pred)

        # Generate and save the classification report for each label
        classification_reports = []
        for i, label in enumerate(mlb.classes_):
            classification_rep = classification_report(y_test[:, i], y_preds[i])
            classification_reports.append(f"Label: {label}\n{classification_rep}")

        # Save the accuracy report to a text file
        report_path = os.path.join("reports/training", f'{model_key}_accuracy_report.txt')
        with open(report_path, 'w') as report_file:
            report_file.write("\n\n".join(classification_reports))

        # Get and save the feature importance for each model
        feature_importance = get_top_features(vectorizer, svms, mlb)
        save_to_markdown(feature_importance, model_key)

        print(f"Model: {model_key} - Accuracy Report and Feature Importance Saved")