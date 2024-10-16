import data_collection as dc
import decision_tree as dt
import numpy as np

def main():
    print("Collecting URLs...")
    legit_urls = dc.get_urls(dc.legit_urls_filename, dc.legit_index)
    phish_urls = dc.get_urls(dc.phish_urls_filename, dc.phish_index)
    print("All URLs collected.")

    print("Saving screenshots that are relevant...")
    legit_screenshots_with_brands = dc.get_screenshot_and_brand(legit_urls, False)
    phish_screenshots_with_brands = dc.get_screenshot_and_brand(phish_urls, True)
    print("Saved screenshots of relevent brand websites.")

    all_screenshots_with_brands = legit_screenshots_with_brands + phish_screenshots_with_brands
    feature_data = dc.create_data_structure(all_screenshots_with_brands)
    print("Finished creating feature data structures from screenshots.")

    np.random.shuffle(feature_data)

    #Split the data (80:20) for training and testing
    split_point = int(0.8 * len(feature_data))
    train = feature_data[:split_point]
    test = feature_data[split_point:]

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

    num_actual_phish = sum(phish_vals_test == 1)
    num_actual_legit = sum(phish_vals_test == 0)

    num_correct_predicted_phish = sum((predictions == 1) & (phish_vals_test == 1))
    num_false_predicted_phish = sum((predictions == 1) & (phish_vals_test == 0))

    tpr = num_correct_predicted_phish / num_actual_phish
    fpr = num_false_predicted_phish / num_actual_legit

    print("RESULTS OF PHISHYPIXELS")
    print(f"Accuracy: {accuracy}")
    print(f"True positive rate (higher is better): {tpr}")
    print(f"False positive rare (lower is better): {fpr}")


if __name__ == "__main__":
    main()