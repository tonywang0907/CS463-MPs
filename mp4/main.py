from timeit import default_timer as timer
import numpy as np
import util
import mp4_model as models

input_file_folder = f'data'
X_file_name = f'{input_file_folder}/apg-X.json'
y_file_name = f'{input_file_folder}/apg-y.json'
meta_file_name = f'{input_file_folder}/apg-meta.json'

def train_model(num_features):
    svm_model = models.SVM(X_file_name, y_file_name, meta_file_name, num_features=num_features)
    svm_model.generate()
    ''' generate all the feature names used by current mode '''
    feature_name_list = [svm_model.vec.feature_names_[i] for i in svm_model.column_idxs]
    util.dump_json(feature_name_list, 'data', f'all_feature_names_{svm_model.X_train.shape[1]}.json')

    report_train, report_test = util.evaluate_classifier_perf(svm_model)

    stat(svm_model)

    print('training perf: ', report_train)
    print('testing perf: ',report_test)
    perf = report_test['model_performance']
    return perf['f1'], perf['precision'], perf['recall']


def stat(svm_model):
    ''' TODO: implement me '''
    # return in the following order
    train_cnt = len(svm_model.y_train)
    test_cnt = len(svm_model.y_test)
    train_mal_cnt = np.sum(svm_model.y_train == 1)
    train_benign_cnt = train_cnt - train_mal_cnt
    test_mal_cnt = np.sum(svm_model.y_test == 1)
    test_benign_cnt = test_cnt - test_mal_cnt

    return train_cnt, test_cnt, train_mal_cnt, train_benign_cnt, test_mal_cnt, test_benign_cnt

if __name__ == '__main__':
    start = timer()
    print("features none")
    train_model(num_features=None) # use all the features
    print('=' * 50)
    
    print("features 5k")
    train_model(num_features=5000) # select 5000 features first, then train a new model
    end = timer()
    print(f'tik tok: {end - start:.4f} seconds')

# The line train_model(num_features=None) uses all features, while train_model(num_features=5000) restricts it to the top 5,000.
# Comparing these results, we observe that using feature selection generally yields better performance than using all features.
# This improvement likely occurs because feature selection can remove irrelevant features, allowing the model to generalize better
# and produce more accurate predictions. Additionally, reducing the feature space can improve efficiency, as training time and memory 
# usage are optimized, which is particularly important for high-dimensional data. However, there is a trade-off between feature 
# selection and performance. While feature selection often enhances accuracy, there is a risk of losing crucial information, 
# which could lead to reduced accuracy if important features are excluded.

