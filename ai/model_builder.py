#
#   Requirements:
#   The aiInput.json file must me an array of tablets, where each is an object with the following keys:
#       accountTypes: []
#       withoutNumbers: ""
#       withNumbers: ""
#
#   The strings must be sorted alphabetically.
#

import os
import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import MultiLabelBinarizer
import joblib

import warnings
warnings.filterwarnings("ignore")

# Load the dataset
script_dir = os.path.dirname(os.path.abspath(__file__))
with open("data/aiInput.json") as f:
    data = json.load(f)

# Convert data to a pandas DataFrame
df = pd.DataFrame(data["data"])

# Extract labels and text versions
labels = df["accountTypes"]
texts_with_numbers = df["withNumbers"]
texts_without_numbers = df["withoutNumbers"]

# Calculate class distribution
class_distribution = labels.explode().value_counts()

# Find underrepresented class and duplicate some examples
underrepresented_classes = class_distribution[class_distribution < class_distribution.max() / 2].index
over_sampled_df = df[df["accountTypes"].apply(lambda x: any(label in x for label in underrepresented_classes))]
df = pd.concat([df, over_sampled_df], ignore_index=True)

# Update the texts and labels after oversampling
labels = df["accountTypes"]
texts_with_numbers = df["withNumbers"]
texts_without_numbers = df["withoutNumbers"]

# Define a function for vectorization based on a given splitter
def vectorize_texts(texts, splitter):
    if splitter == "space":
        vectorizer = TfidfVectorizer(token_pattern=r"(?u)\S+")
    elif splitter == "newline":
        vectorizer = TfidfVectorizer(token_pattern=r"(?u)[^\n]+")
    return vectorizer, vectorizer.fit_transform(texts)

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
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

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

        # Optionally save to disk
        model_dir = os.path.join(script_dir, 'saved', model_key)
        os.makedirs(model_dir, exist_ok=True)
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

        # Save the classification report to a text file
        report_path = os.path.join(model_dir, f'{model_key}_classification_report.txt')
        with open(report_path, 'w') as report_file:
            report_file.write("\n\n".join(classification_reports))
        print(f"Classification report saved to {report_path}")
