import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

test_ids = test["id"]

X = train.drop(['Irrigation_Need'], axis=1)
y = train['Irrigation_Need']

X = pd.get_dummies(X)
test = pd.get_dummies(test)

test = test.reindex(columns=X.columns, fill_value=0)

X = X.drop(['id'], axis=1)
test = test.drop(['id'], axis=1)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

model = GradientBoostingClassifier(n_estimators=30, learning_rate=0.1)

model.fit(X_train, y_train)

y_pred = model.predict(X_val)

cm = confusion_matrix(y_val, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Low","Medium","High"])
disp.plot()
plt.show()

model.fit(X, y)

pred = model.predict(test)

submission = pd.DataFrame({
    "id": test_ids,
    "Irrigation_Need": pred
})

submission.to_csv("submission.csv", index=False)

print("Submission file created")
