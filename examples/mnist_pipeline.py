# Example taken from: https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html#sphx-glr-auto-examples-classification-plot-digits-classification-py

import sys
sys.path.append('C://Users//admin//projects//fastpipeline')


# Import datasets, classifiers and performance metrics
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split
import numpy as np

from fastpipeline.base_node import BaseNode
from fastpipeline.pipeline import Pipeline

class DataLoader(BaseNode):
    def __init__(self):
        super().__init__()
    
    def run(self, input = {}):
        # The digits dataset
        digits = datasets.load_digits()

        # To apply a classifier on this data, we need to flatten the image, to
        # turn the data in a (samples, feature) matrix:
        n_samples = len(digits.images)
        data = digits.images.reshape((n_samples, -1))
        return {
            'data': data,
            'target': digits.target
        }

class SVMClassifier(BaseNode):
    def __init__(self, config):
        super().__init__(config)
        gamma = config['gamma']
        # Create a classifier: a support vector classifier
        self.classifier = svm.SVC(gamma=gamma)
    
    def run(self, input):
        data = input['data']
        target = input['target']

        # Split data into train and test subsets
        X_train, X_test, y_train, y_test = train_test_split(
            data, target, test_size=0.5, shuffle=False)

        # We learn the digits on the first half of the digits
        self.classifier.fit(X_train, y_train)

        # Now predict the value of the digit on the second half:
        y_pred = self.classifier.predict(X_test)

        return {
            'acc': np.mean(y_test == y_pred),
            'y_test': y_test,
            'y_pred': y_pred 
        }


# if __name__ == "__main__":
#     dl = DataLoader()
#     svms = [ SVMClassifier({'gamma': gamma}) for gamma in [0.01, 0.05, 0.001]]
    
#     pipelines = [ Pipeline('mnist', [dl, svm]) for svm in svms ]
#     for pipeline in pipelines:
#         result = pipeline.run({})
#         gamma = pipeline.nodes[1].config['gamma']
#         print('\nResult for C=%s'%gamma)
#         print('Accuracy: %s'%result['acc'])
if __name__ == "__main__":
    # Initialize the nodes
    dl_node = DataLoader()
    svm_node = SVMClassifier({'gamma': 0.01})

    # Create the pipeline
    pipeline = Pipeline('mnist', [dl_node, svm_node])

    # Run pipeline and see results
    result = pipeline.run(input={})
    print('Accuracy: %s'%result['acc'])


