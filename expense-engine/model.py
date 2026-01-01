from sklearn.naive_bayes import MultinomialNB

model = MultinomialNB()

def train(X, y):
    model.fit(X, y)

def predict(X):
    return model.predict(X)
