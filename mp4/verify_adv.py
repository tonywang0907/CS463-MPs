import numpy as np
import json
import pickle
import os

class Verifier:
    def __init__(self, jsonFile):
        self.jsonFile = jsonFile
        self.features = [0] * 5000

    def getFeatureArray(self, featureList, addedFeatureList):
        pass

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
    verifier_5E06B7.getFeatureArray(fList, aFList_5E06B7)
    verifier_49875A.getFeatureArray(fList, aFList_49875A)
    # Load trained SVM model with 5000 features

    # Make predictions

    # Output predicted label and original label for each sample
    # Object needed to be printed out -  res = {"5E06B7": <value>, "49875A": <value>}
    # The predicted value can be 0 or 1. 
    # Expected output
    # {"5E06B7": 1, "49875A": 0}
    
    # Please put your thought as code comments below why these features might be helpful to make an adversarial sample.
