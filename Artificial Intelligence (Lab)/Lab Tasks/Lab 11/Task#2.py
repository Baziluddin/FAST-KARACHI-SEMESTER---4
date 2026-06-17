import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

data = pd.DataFrame({
    "Income": [30000, 50000, 70000, None, 60000],
    "EmploymentStatus": ["Employed", "Employed", "Employed", "Unemployed", None],
    "CreditScore": [600, 700, 750, 650, 720],
    "LoanAmount": [100000, 200000, 150000, 120000, 180000],
    "MaritalStatus": ["Single", "Married", "Married", None, "Married"],
    "LoanApproved": [0, 1, 1, 0, 1]
})

data["Income"] = data["Income"].fillna(data["Income"].mean())
data["EmploymentStatus"] = data["EmploymentStatus"].fillna(data["EmploymentStatus"].mode()[0])
data["MaritalStatus"] = data["MaritalStatus"].fillna(data["MaritalStatus"].mode()[0])

le = LabelEncoder()
data["EmploymentStatus"] = le.fit_transform(data["EmploymentStatus"])
data["MaritalStatus"] = le.fit_transform(data["MaritalStatus"])

print(data.corr()["LoanApproved"].sort_values(ascending=False))

X = data.drop("LoanApproved", axis=1)
y = data["LoanApproved"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))

new_applicant = [[55000, 0, 710, 160000, 1]]
prediction = model.predict(new_applicant)

print("Loan Approved (1=Yes, 0=No):", prediction[0])
