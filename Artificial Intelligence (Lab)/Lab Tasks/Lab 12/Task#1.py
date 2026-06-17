import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.read_csv('house_prices.csv')

print(df.head())
print(df.shape)
print(df.columns)

num_cols = df.select_dtypes(include=np.number).columns
cat_cols = df.select_dtypes(exclude=np.number).columns

missing = df.isnull().sum()
drop_cols = missing[missing > 0.5 * len(df)].index
df = df.drop(columns=drop_cols)

for col in num_cols:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].median())

for col in cat_cols:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mode()[0])

plt.figure()
sns.histplot(df['SalePrice'], kde=True)

plt.figure()
sns.boxplot(x=df['SalePrice'])

if 'GrLivArea' in df.columns:
    plt.figure()
    sns.histplot(df['GrLivArea'], kde=True)

    plt.figure()
    sns.boxplot(x=df['GrLivArea'])

corr = df.corr(numeric_only=True)

if 'SalePrice' in corr.columns:
    sale_corr = corr['SalePrice'].sort_values(ascending=False)

plt.figure(figsize=(10,8))
sns.heatmap(corr, cmap='coolwarm')

if 'GrLivArea' in df.columns and 'SalePrice' in df.columns:
    plt.figure()
    sns.scatterplot(x=df['GrLivArea'], y=df['SalePrice'])

if 'OverallQual' in df.columns and 'SalePrice' in df.columns:
    plt.figure()
    sns.barplot(x=df['OverallQual'], y=df['SalePrice'])

if 'SalePrice' in corr.columns:
    top5 = sale_corr.index[1:6]
    print(top5)

if 'YrSold' in df.columns and 'YearBuilt' in df.columns:
    df['HouseAge'] = df['YrSold'] - df['YearBuilt']

if 'Id' in df.columns:
    df = df.drop(columns=['Id'])

df = pd.get_dummies(df, drop_first=True)

X = df.drop(columns=['SalePrice'])
y = df['SalePrice']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(mae, rmse, r2)
