import sys
sys.path.append('C://Users//admin//projects//fastpipeline')

import os
import numpy as np
import pandas as pd

from fastpipeline.base_node import BaseNode
from fastpipeline.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
import spacy

nlp = spacy.load('en_core_web_sm')

DF_NODE_OUT = {
    'df': pd.DataFrame({
                'col1': [x for x in range(100)],
                'col2': [str(x) for x in range(100)]
            })
}

LOGREG_OUT = {
    'clf': LogisticRegression()
    }

SPACY_OUT = {
    'docs':[nlp('there is this man'), nlp('Hello world')]
    }

class DataFrameNode(BaseNode):
    '''Returns a dict containing dataframe with integer and string columns'''
    def run(self, input):
        return DF_NODE_OUT

class LogisticRegressionNode(BaseNode):
    '''Returns a dict wih a sklearn classifier'''
    def run(self, input):
        return LOGREG_OUT


class SpacyNode(BaseNode):
    '''Returns list of spacy docs'''
    def run(self, input):
        return SPACY_OUT


def test_data_frame():
    pipeline = Pipeline('data_test', [DataFrameNode()])
    out = pipeline.run(input={})
    assert isinstance(out['df'], pd.DataFrame)
    assert (out['df'] == DF_NODE_OUT['df']).all().all()

def test_log_reg():
    pipeline = Pipeline('data_test', [LogisticRegressionNode()])
    out = pipeline.run(input={})
    assert isinstance(out['clf'], LogisticRegression)

def test_spacy():
    pipeline = Pipeline('data_test', [SpacyNode()])
    out = pipeline.run({})
    for i, doc in enumerate(out['docs']):
        assert isinstance(doc, spacy.tokens.doc.Doc)
        assert doc.text == SPACY_OUT['docs'][i].text
