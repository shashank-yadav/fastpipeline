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
