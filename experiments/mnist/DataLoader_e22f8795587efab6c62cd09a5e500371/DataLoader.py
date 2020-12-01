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
