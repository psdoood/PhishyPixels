#                         <<<IMPORTANT>>>
#Must run data_collection.py/organize_screenshots.py first (unless 
#screenshot brand folders are already filled, which they should be)
#I seperated this process to make the decision tree testing/demo faster

import os
import data_processing as dp
import decision_tree as dt
import numpy as np

#Calculates the true positive rate (higher better) and false positive rate (lower better)
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


#Implementations of K-Fold cross validation, makes sure each sample (data/k) is used in both training and testing
#at different decision tree creations
def k_fold_cross_validation(k=9):
    accuracy_list = []
    tpr_list = []
    fpr_list = []

    print("Getting screenshot data...")
    legit_on_brand = {}
    phish_on_brand = {}

    for brand in dp.BRAND_NAMES:
        print(f"\nProcessing screenshots from: {brand}")
        legit_dir = f"screenshots/brands/{brand}/legit"
        phish_dir = f"screenshots/brands/{brand}/phish"

        legit_imgs = []
        phish_imgs = []

        for img in os.listdir(legit_dir):
            legit_imgs.append(os.path.join(legit_dir, img))

        for img in os.listdir(phish_dir):
            phish_imgs.append(os.path.join(phish_dir, img))

        np.random.shuffle(legit_imgs)
        np.random.shuffle(phish_imgs)

        legit_on_brand[brand] = dp.create_data_structure(legit_imgs, dp.BRAND_NAMES.index(brand), 1)
        phish_on_brand[brand] = dp.create_data_structure(phish_imgs, dp.BRAND_NAMES.index(brand), 0)

    for i in range(k):
        print(f"\nStarting fold: {i + 1}")
        legit_train = []
        phish_train = []
        legit_test = []
        phish_test = []

        for brand in dp.BRAND_NAMES:
            legit_brand_data = legit_on_brand[brand]
            phish_brand_data = phish_on_brand[brand]

            legit_fold = int(len(legit_brand_data) / k)
            phish_fold = int(len(phish_brand_data) / k)

            legit_start_test = i * legit_fold
            legit_end_test = (i + 1) * legit_fold
            phish_start_test = i * phish_fold
            phish_end_test = (i + 1) * phish_fold

            legit_test.extend(legit_brand_data[legit_start_test:legit_end_test])
            phish_test.extend(phish_brand_data[phish_start_test:phish_end_test])
            legit_train.extend(legit_brand_data[:legit_start_test])
            legit_train.extend(legit_brand_data[legit_end_test:]) 
            phish_train.extend(phish_brand_data[:phish_start_test]) 
            phish_train.extend(phish_brand_data[phish_end_test:])
        
        np.random.shuffle(legit_test)
        np.random.shuffle(phish_test)
        np.random.shuffle(legit_train)
        np.random.shuffle(phish_train)

        train = np.vstack((legit_train, phish_train))
        test = np.vstack((legit_test, phish_test))
        np.random.shuffle(train)
        np.random.shuffle(test)

        print(f"Building the decision tree with training data from fold: {i + 1}")
        tree = dt.decision_tree()
        tree.start_building(train)
        print(f"Finished building the decision tree for fold: {i + 1}")

        print(f"Running test data for predictions for fold: {i + 1}")
        feature_test = test[:, :-1]
        phish_vals_test = test[:, -1]
        predictions = tree.predict(feature_test)

        print("Calculating results...")
        accuracy = np.mean(predictions == phish_vals_test)
        tpr, fpr = calculate_metrics(predictions, phish_vals_test)

        accuracy_list.append(accuracy)
        tpr_list.append(tpr)
        fpr_list.append(fpr)

        print(f"\nResults of fold: {i + 1}")
        print(f"Accuracy: {accuracy}")
        print(f"True positive rate (higher is better): {tpr}")
        print(f"False positive rate (lower is better): {fpr}\n")

    print("\nRESULTS OF PHISHYPIXELS:\n")
    print(f"Accuracy: {np.mean(accuracy_list)}")
    print(f"True positive rate (higher is better): {np.mean(tpr_list)}")
    print(f"False positive rate (lower is better): {np.mean(fpr_list)}")


def main():
    k_fold_cross_validation()

if __name__ == "__main__":
    main()