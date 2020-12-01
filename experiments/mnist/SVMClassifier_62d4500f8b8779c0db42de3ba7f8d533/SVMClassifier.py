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
