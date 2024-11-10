import numpy as np
import json
import pickle
import os
from mp4_model import SVM

class Verifier:
    def __init__(self, jsonFile):
        self.jsonFile = jsonFile
        self.features = [0] * 5000

    def getFeatureArray(self, featureList, addedFeatureList):
        with open(featureList, 'r') as f:
            all_features = json.load(f)  
        
        with open(addedFeatureList, 'r') as f:
            added_features = f.readlines()  
        
        added_features_set = set([feature.strip() for feature in added_features])  
        
        with open(self.jsonFile, 'r') as f:
            original_features = json.load(f)
        
        feature_name_to_index = {name: idx for idx, name in enumerate(all_features)}
        
        feature_vector = [0] * len(all_features)
        
        for feature in original_features:
            if feature in feature_name_to_index:
                idx = feature_name_to_index[feature]
                feature_vector[idx] = 1
        
        for feature in added_features_set:
            if feature in feature_name_to_index:
                idx = feature_name_to_index[feature]
                feature_vector[idx] = 1
        
        return np.array(feature_vector)  


if __name__ == "__main__":
    verifier_5E06B7 = Verifier(
        "./5E06B7510B55B52C94D2AB0D7BB94AAA454860C6F8729BA2842438D92CDB8EEE.json"
    )
    verifier_49875A = Verifier(
        "./49875A9C25EB18945A8E7F27C8188834CFF48070413604D477763EC7A20E9C4A.json"
    )
    
    input_file_folder = f"data"
    # featureList is the output file with the 5000 in the name
    # aFList_# is the additional features added to the json file of the outputs
    fList = f"{input_file_folder}/all_feature_names_5000.json"
    aFList_5E06B7 = "added-features-5E06B7.txt"
    aFList_49875A = "added-features-49875A.txt"

    # Load trained SVM model with 5000 features
    model_filename = "svm-f5000.p"
    with open(model_filename, 'rb') as f:
        svm_model = pickle.load(f)

    # Get the model's coefficients
    coef = svm_model.clf.coef_.flatten()  # Flatten to 1D array
    
    with open(fList, 'r') as f:
        feature_names = json.load(f)
    
    # Filter features that start with 'app_permission' or 'api_permission'
    desired_feature_names = []
    for feature in feature_names:
        if feature.startswith("app_permission") or feature.startswith("api_permission"):
            desired_feature_names.append(feature)
    
    # Filter coefficients to match the desired features
    desired_coef = []
    for i, feature in enumerate(feature_names):
        if feature in desired_feature_names:
            desired_coef.append(coef[i])

    sorted_idx = np.argsort(np.abs(desired_coef))[::-1]  
    
    # Select the top 10 influential features based on their coefficients
    top_influential_idx = sorted_idx[:10]  
    top_influential_names = []
    top_influential_coef = []
    for idx in top_influential_idx:
        top_influential_names.append(desired_feature_names[idx])
        top_influential_coef.append(desired_coef[idx])
    
    # print("Top 10 influential features:")
    # for name, coef in zip(top_influential_names, top_influential_coef):
    #     print(f"Feature: {name}, Coefficient: {coef}")

    # Select adversarial features based on coefficients
    adversarial_features_5E06B7 = []
    adversarial_features_49875A = []

    for i in range(len(top_influential_coef)):
        if top_influential_coef[i] > 0:
            adversarial_features_5E06B7.append(top_influential_names[i])
        elif top_influential_coef[i] < 0:
            adversarial_features_49875A.append(top_influential_names[i])
            
    # Add adversarial features to "added-features-5E06B7.txt" 
    with open(aFList_5E06B7, 'w') as f:
        for feature in adversarial_features_5E06B7:
            f.write(f"{feature}\n")
    
    # Add adversarial features to "added-features-49875A.txt"
    with open(aFList_49875A, 'w') as f:
        for feature in adversarial_features_49875A:
            f.write(f"{feature}\n")
    
    # Merge the feature arrays with the adversarial features
    feature_vector_5E06B7 = verifier_5E06B7.getFeatureArray(fList, aFList_5E06B7)
    feature_vector_49875A = verifier_49875A.getFeatureArray(fList, aFList_49875A)

    # Make predictions
    prediction_5E06B7 = svm_model.clf.predict([feature_vector_5E06B7])
    prediction_49875A = svm_model.clf.predict([feature_vector_49875A])

    # Output predicted label and original label for each sample
    print('{"5E06B7": ' + str(prediction_5E06B7[0]) + ', "49875A": ' + str(prediction_49875A[0]) + '}')

    # Object needed to be printed out -  res = {"5E06B7": <value>, "49875A": <value>}
    # The predicted value can be 0 or 1. 
    # Expected output
    # {"5E06B7": 1, "49875A": 0}
    
    # Please put your thought as code comments below why these features might be helpful to make an adversarial sample.
