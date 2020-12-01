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
