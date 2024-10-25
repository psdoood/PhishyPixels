#                         <<<IMPORTANT>>>
#Must run data_collection.py first (unless screenshots folders are filled)
#I seperated this process to make the decision tree testing/demo faster

import os
import data_processing as dp
import decision_tree as dt
import numpy as np

def calculate_metrics(predictions, phish_vals_test):
    num_actual_phish = np.sum(phish_vals_test == 0)
    num_actual_legit = np.sum(phish_vals_test == 1)
    print(f"Actual phishing sites used in testing: {num_actual_phish}")
    print(f"Actual legitimate sites used in testing: {num_actual_legit}")
    
    num_correct_predicted_phish = np.sum((predictions == 0) & (phish_vals_test == 0))
    num_false_predicted_phish = np.sum((predictions == 0) & (phish_vals_test == 1))
    
    tpr = num_correct_predicted_phish / num_actual_phish 
    fpr = num_false_predicted_phish / num_actual_legit 
    
    return tpr, fpr

def main():
    print("\nScanning screenshots and creating feature data...")
    legit_dir = "screenshots/not_phish"
    phish_dir = "screenshots/phish"
    
    legit_paths = []
    phish_paths = []

    for file in os.listdir(legit_dir):
        if file.endswith(".png"):
            legit_paths.append(os.path.join(legit_dir, file))

    for file in os.listdir(phish_dir):
        if file.endswith(".png"):
            phish_paths.append(os.path.join(phish_dir, file))

    legit_feature_data = dp.create_data_structure(legit_paths, False)
    phish_feature_data = dp.create_data_structure(phish_paths, True)
    print("Finished creating feature data structures from screenshots.")

    np.random.shuffle(legit_feature_data)
    np.random.shuffle(phish_feature_data)

    legit_split_point = int(0.8 * len(legit_feature_data))
    phish_split_point = int(0.8 * len(phish_feature_data))

    legit_train = legit_feature_data[:legit_split_point]
    legit_test = legit_feature_data[legit_split_point:]
    phish_train = phish_feature_data[:phish_split_point]
    phish_test = phish_feature_data[phish_split_point:]

    train = np.vstack((legit_train, phish_train))
    test = np.vstack((legit_test, phish_test))

    print("Building the decision tree with training data...")
    tree = dt.decision_tree()
    tree.start_building(train)
    print("Finished building the decision tree.")

    print("Running test data for predictions...")
    feature_test = test[:, :-1]
    phish_vals_test = test[:, -1]
    predictions = tree.predict(feature_test)

    print("Calculating results...")
    accuracy = np.mean(predictions == phish_vals_test)
    tpr, fpr = calculate_metrics(predictions, phish_vals_test)
    
    print("\nRESULTS OF PHISHYPIXELS:\n")
    print(f"Accuracy: {accuracy}")
    print(f"True positive rate (higher is better): {tpr}")
    print(f"False positive rate (lower is better): {fpr}")


if __name__ == "__main__":
    main()