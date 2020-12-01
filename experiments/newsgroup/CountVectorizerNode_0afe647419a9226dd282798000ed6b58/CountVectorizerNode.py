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
