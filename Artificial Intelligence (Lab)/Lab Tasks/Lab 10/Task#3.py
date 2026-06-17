import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

np.random.seed(0)

n = 100
df = pd.DataFrame({
    'student_id': range(1, n + 1),
    'GPA': np.round(np.random.uniform(2.0, 4.0, n), 2),
    'study_hours': np.round(np.random.uniform(1, 10, n), 1),
    'attendance_rate': np.round(np.random.uniform(60, 100, n), 1)
})

X = df[['GPA', 'study_hours', 'attendance_rate']]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

wcss = []
for i in range(2, 7):
    kmeans = KMeans(n_clusters=i, random_state=0)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

plt.plot(range(2, 7), wcss, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.title('Elbow Method')
plt.show()

kmeans = KMeans(n_clusters=3, random_state=0)
df['cluster'] = kmeans.fit_predict(X_scaled)

plt.scatter(df['study_hours'], df['GPA'], c=df['cluster'])
plt.xlabel('Study Hours')
plt.ylabel('GPA')
plt.title('Student Clusters')
plt.show()

print(df[['student_id', 'cluster']])
