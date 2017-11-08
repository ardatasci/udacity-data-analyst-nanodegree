#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data


import numpy as np
import pandas as pd

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

### NOTE: feature_list is a list of selected features the selection process is defined in detail, please see enron_data_investigate.html. Data selection process was not reflected in poi_id.py, since it is a preliminary process.
features_list = ['poi',
                 'to_messages', 
                 'exercised_stock_options', 
                 'bonus', 
                 'restricted_stock', 
                 'shared_receipt_with_poi', 
                 'to_message_poi_ratio']


### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
    
df = pd.DataFrame.from_dict(data_dict, orient='index')


### Task 2: Remove outliers
### NOTE: To see how I found TOTAL as outlier and mailing features, moreover LOCKHART EUGENE E was dropped since all the fields were NaN, high number of to_messages and from_messages were accepted as outliers and dropped from dataset, for details please see enron_data_investigate.html 
df = df.drop('TOTAL')
df = df.drop('LOCKHART EUGENE E')
df = df[df.to_messages < 6000]
df = df[df.from_messages < 1000]


### NOTE: There are NaN values which need to be zeros (if financial features) and feature median (if mailing features). please see enron_data_investigate.html
df = df.replace('NaN', np.nan)

financial_features = ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']
df[financial_features] = df[financial_features].fillna(0)


email_features = ['to_messages', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']
df[email_features] = df[email_features].fillna(df[email_features].median())

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
### NOTE: For details, please see enron_data_investigate.html

df['to_message_poi_ratio'] = df['from_this_person_to_poi'] / df['to_messages']
df['from_message_poi_ratio'] = df['from_poi_to_this_person'] / df['from_messages']
df['message_in_out_ratio'] = df['from_messages'] / df['to_messages']

engineered_features = list(df)


def created_engineered_dataframe(engineered_f, data_frame):
    X_engineered = df[engineered_features]
    return X_engineered

X = created_engineered_dataframe(engineered_features, df)
y = df.poi


my_dataset = X.to_dict('index')



### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

### NOTE: I have tried 3 different classifiers, and tune their parameters, please see enron_data_investigate.html for details.
from sklearn.tree import DecisionTreeClassifier

clf = DecisionTreeClassifier(random_state=42)

# Provided to give you a starting point. Try a variety of classifiers.
#from sklearn.naive_bayes import GaussianNB
#clf = GaussianNB()

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html


### NOTE: Finally I have chosen DecisionTree with parameters {'criterion': 'entropy', 'max_depth': 7, 'min_samples_leaf': 1}, please see enron_data_investigate.html for details.

DT_best_tune = {'criterion': 'entropy', 
                'max_depth': 7, 
                'min_samples_leaf': 1}
clf.set_params(**DT_best_tune)



# Example starting point. Try investigating other evaluation techniques!
#from sklearn.cross_validation import train_test_split
#features_train, features_test, labels_train, labels_test = \
 #   train_test_split(features, labels, test_size=0.3, random_state=42)

    
    
### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)