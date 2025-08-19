import os
import json
import joblib
import numpy as np
import random

# Load trained models
script_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(script_dir, 'unduplicated_models')

# Load the dataset (corpus to classify)
with open("data/corpusClean.json") as f:
    corpus = json.load(f)

# Define function to load models
def load_model(model_key):
    model_path = os.path.join(model_dir, model_key)
    svms = joblib.load('svm/with_numbers_space/svm_models.joblib')
    vectorizer = joblib.load('svm/with_numbers_space/tfidf_vectorizer.joblib')
    mlb = joblib.load('svm/with_numbers_space/mlb.joblib')
    return svms, vectorizer, mlb

# Process corpus
classified_data = []
label_counts = {}
sample_check = {}

for item in corpus:
    text = item.get("withNumbers", "").strip()  # Use "withNumbers" for classification

    # **Skip text if it has fewer than 6 words**
    if len(text.split()) < 6:
        continue

    model_key = "with_numbers_space"  # Ensure using correct trained model
    svms, vectorizer, mlb = load_model(model_key)

    # Vectorize input text
    X = vectorizer.transform([text])

    # Predict labels
    assigned_labels = []
    for i, svm in enumerate(svms):
        # Check if the model has predict_proba, which provides class probabilities
        if hasattr(svm, "predict_proba"):
            prob = svm.predict_proba(X)[0][1]  # Positive class probability
        else:
            decision_score = svm.decision_function(X)
            prob = 1 / (1 + np.exp(-decision_score))  # Apply sigmoid to get probability

        # Assign label if the probability is above 90%
        if prob >= 0.90:
            label = mlb.classes_[i]
            assigned_labels.append(label + " (automated)")

            # Update counts for report
            label_counts[label] = label_counts.get(label, 0) + 1

            # Store samples for error checking, using the link instead of text
            if label not in sample_check:
                sample_check[label] = []
            link = item.get("link", "No link available")  # Get the link if available
            sample_check[label].append(link)

    # Add assigned labels to item
    item["accountType"].extend(assigned_labels)
    classified_data.append(item)

# Save the classified corpus
output_path = "reports/corpus/classified_corpus.json"
with open(output_path, "w") as f:
    json.dump(classified_data, f, indent=4, ensure_ascii=False)

# Generate reports
report_lines = ["Classification Report:\n"]
for label, count in label_counts.items():
    report_lines.append(f"{label}: {count} times assigned")

# Save classification report
with open("reports/corpus/classification_report.txt", "w") as f:
    f.write("\n".join(report_lines))

# Save sample error-checking report with random links (10 random links for each label)
sample_report_lines = ["Sample Error Checking:\n"]
for label, links in sample_check.items():
    sample_report_lines.append(f"\n{label}:")
    
    # Select 10 random links for error checking (if there are more than 10)
    random_links = random.sample(links, min(10, len(links)))
    for link in random_links:
        sample_report_lines.append(f"{link}")

with open("reports/corpus/sample_error_check.txt", "w") as f:
    f.write("\n".join(sample_report_lines))

print("Tagging complete! Results saved in 'reports/tagged_corpus.json'.")
