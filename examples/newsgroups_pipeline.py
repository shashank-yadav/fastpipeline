# Example taken from: https://scikit-learn.org/stable/auto_examples/model_selection/grid_search_text_feature_extraction.html
import sys
sys.path.append('C://Users//admin//projects//fastpipeline')

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score
from sklearn import svm


from fastpipeline.pipeline import Pipeline
from fastpipeline.base_node import BaseNode

# Load some categories from the training set
categories = [
    'alt.atheism',
    'talk.religion.misc',
]

# Uncomment the following to do the analysis on all the categories
#categories = None
print("Loading 20 newsgroups dataset for categories:")
print(categories)

data = fetch_20newsgroups(subset='train', categories=categories)
print("%d documents" % len(data.filenames))
print("%d categories" % len(data.target_names))
print()


class CountVectorizerNode(BaseNode):
    def __init__(self, config={}):
        super().__init__(config)
        self.count_vectorizer = CountVectorizer()

    def run(self, input):
        data = input['data']
        target = input['target']
        return {
            'X': self.count_vectorizer.fit_transform(data),
            'y': target
        }

class TfidfTransformerNode(BaseNode):
    def __init__(self, config={}):
        super().__init__(config)
        self.tfidf_transformer = TfidfTransformer()

    def run(self, input):
        X, y = input['X'], input['y']
        return {
            'X': self.tfidf_transformer.fit_transform(X),
            'y': y
        }

class ClassifierNode(BaseNode):
    def __init__(self, config={}):
        super().__init__(config)
        self.clf = svm.SVC(kernel='linear', C=1)
        
    def run(self, input):
        X, y = input['X'], input['y']
        scores = cross_val_score(self.clf, X, y, cv=5)
        return {
            'scores': scores
        }

if __name__ == "__main__":
    input = {
        'data': data.data,
        'target': data.target
    }

    count_vectorizer = CountVectorizerNode()
    tfidf = TfidfTransformerNode()
    clf = ClassifierNode()
    pipeline = Pipeline('newsgroup', [count_vectorizer, tfidf, clf])
    output = pipeline.run(input)
    print(output)
    



