import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

data = {
'customer_id': range(1, 11),
'age': [22, 25, 47, 52, 46, 56, 23, 40, 60, 48],
'annual_income': [15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
'spending_score': [39, 81, 6, 77, 40, 76, 94, 3, 72, 14]
}

df = pd.DataFrame(data)

X = df.drop('customer_id', axis=1)

kmeans1 = KMeans(n_clusters=3, random_state=0)
df['cluster_no_scaling'] = kmeans1.fit_predict(X)

scaler = StandardScaler()
X_scaled = X.copy()
cols = [c for c in X.columns if c != 'age']
X_scaled[cols] = scaler.fit_transform(X_scaled[cols])

kmeans2 = KMeans(n_clusters=3, random_state=0)
df['cluster_with_scaling'] = kmeans2.fit_predict(X_scaled)

print(df)
