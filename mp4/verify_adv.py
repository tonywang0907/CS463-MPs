import numpy as np
import json
import pickle
import os
from mp4_model import SVM

class Verifier:
    def __init__(self, jsonFile):
        self.jsonFile = jsonFile
        self.features = [0] * 5000

    # def getFeatureArray(self, featureList, addedFeatureList):
    #     with open(featureList, 'r') as f:
    #         all_features = json.load(f)
        
    #     with open(addedFeatureList, 'r') as f:
    #         added_features = f.readlines()


    #     with open(self.jsonFile, 'r') as f:
    #         original_features = json.load(f)
        
    #     feature_vector = [0] * len(all_features)

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

    # Merge the feature array with the added features
    feature_vector_5E06B7 = verifier_5E06B7.getFeatureArray(fList, aFList_5E06B7)
    feature_vector_49875A = verifier_49875A.getFeatureArray(fList, aFList_49875A)
    # Load trained SVM model with 5000 features

    model_filename = "svm-f5000.p"
    with open(model_filename, 'rb') as f:
        svm_model = pickle.load(f)

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

