from sklearn.tree import DecisionTreeClassifier
import pandas as pd

def train_model():
    data = {
        "category": [0, 1, 0, 1, 0, 1],
        "dance": [0, 1, 2, 1, 2, 0],
        "recommend": [0, 1, 1, 1, 0, 0]
    }

    df = pd.DataFrame(data)
    X = df[["category", "dance"]]
    y = df["recommend"]

    model = DecisionTreeClassifier()
    model.fit(X, y)

    return model

def predict(model, cat, dan):
    return model.predict([[cat, dan]])