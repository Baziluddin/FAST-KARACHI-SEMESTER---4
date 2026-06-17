import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

data = pd.DataFrame({
    "MonthlyCharges": [2000, 3000, 2500, 4000, None, 3500],
    "ContractType": ["Month", "Year", "Month", "Year", "Month", None],
    "Tenure": [12, 24, 10, 36, 15, 20],
    "InternetService": ["DSL", "Fiber", "DSL", None, "Fiber", "DSL"],
    "SupportCalls": [1, 3, 2, 5, 10, 2],
    "Churn": [0, 1, 0, 1, 1, 0]
})

data["MonthlyCharges"] = data["MonthlyCharges"].fillna(data["MonthlyCharges"].mean())
data["ContractType"] = data["ContractType"].fillna(data["ContractType"].mode()[0])
data["InternetService"] = data["InternetService"].fillna(data["InternetService"].mode()[0])

Q1 = data.quantile(0.25)
Q3 = data.quantile(0.75)
IQR = Q3 - Q1
data = data[~((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)]

le = LabelEncoder()
data["ContractType"] = le.fit_transform(data["ContractType"])
data["InternetService"] = le.fit_transform(data["InternetService"])

X = data.drop("Churn", axis=1)
y = data["Churn"]

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)

y_pred = svm_model.predict(X_test)

print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))

rf_model = RandomForestClassifier()
rf_model.fit(X_train, y_train)

print("Feature Importance:", rf_model.feature_importances_)

new_customer = [[3000, 1, 18, 0, 2]]
new_customer = scaler.transform(new_customer)

prediction = svm_model.predict(new_customer)

print("Churn (1=Yes, 0=No):", prediction[0])
