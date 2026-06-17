import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

data = pd.DataFrame({
    "StudyHours": [2, 4, 6, None, 5],
    "Attendance": [60, 70, None, 90, 75],
    "PreviousGrades": [50, 60, 65, 80, 70],
    "Participation": ["Low", "Medium", "Medium", "High", "Medium"],
    "InternetUsage": [2, 3, 4, 5, 3],
    "FinalScore": [50, 60, 70, 85, 75]
})

data["StudyHours"] = data["StudyHours"].fillna(data["StudyHours"].mean())
data["Attendance"] = data["Attendance"].fillna(data["Attendance"].mean())

le = LabelEncoder()
data["Participation"] = le.fit_transform(data["Participation"])

print(data.corr()["FinalScore"].sort_values(ascending=False))

X = data.drop("FinalScore", axis=1)
y = data["FinalScore"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("MAE:", mae)
print("RMSE:", rmse)
print("R2 Score:", r2)

new_student = [[5, 80, 70, 2, 3]]
prediction = model.predict(new_student)

print("Predicted Final Score:", prediction[0])
