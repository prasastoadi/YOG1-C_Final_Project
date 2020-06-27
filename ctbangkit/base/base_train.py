class BaseTrain:

    def __init__(self, model, data):
        self.model = model
        self.data = data

    def train(self):
        raise NotImplementedError
