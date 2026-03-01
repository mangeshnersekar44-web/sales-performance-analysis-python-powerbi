# -----------------------------
# Smart Sales Analytics Project
# Without Streamlit
# -----------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# -----------------------------
# 1. Load Dataset
# -----------------------------
df = pd.read_csv("sales_dataset.csv")

print("First 5 rows:")
print(df.head())

# -----------------------------
# 2. Data Cleaning & Preprocessing
# -----------------------------
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

df = df.dropna()

# -----------------------------
# 3. Feature Engineering
# -----------------------------
df['Revenue'] = df['Sales']
df['Month'] = df['Order Date'].dt.month
df['Year'] = df['Order Date'].dt.year
df['Quarter'] = df['Order Date'].dt.quarter

# -----------------------------
# 4. Exploratory Data Analysis (EDA)
# -----------------------------

# Revenue by Region
region_sales = df.groupby('Region')['Revenue'].sum()

plt.figure(figsize=(8,5))
region_sales.plot(kind='bar')
plt.title("Revenue by Region")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.show()

# -----------------------------
# Monthly Sales Trend
# -----------------------------
monthly_sales = df.groupby(pd.Grouper(key='Order Date', freq='M'))['Revenue'].sum()

plt.figure(figsize=(10,5))
monthly_sales.plot()
plt.title("Monthly Sales Trend")
plt.ylabel("Revenue")
plt.show()

# -----------------------------
# Heatmap (Product vs Region)
# -----------------------------
pivot = pd.pivot_table(
    df,
    values='Revenue',
    index='Sub-Category',
    columns='Region',
    aggfunc='sum'
)

plt.figure(figsize=(10,6))
sns.heatmap(pivot, cmap="Blues")
plt.title("Product vs Region Revenue Heatmap")
plt.show()

# -----------------------------
# Category Contribution (Pie Chart)
# -----------------------------
category_sales = df.groupby('Category')['Revenue'].sum()

plt.figure(figsize=(6,6))
plt.pie(category_sales, labels=category_sales.index,
        autopct='%1.1f%%', startangle=90)
plt.title("Revenue Share by Category")
plt.show()

# -----------------------------
# 5. Sales Forecasting using Linear Regression
# -----------------------------

# Monthly Aggregated Data
monthly = df.groupby(pd.Grouper(key='Order Date', freq='M'))['Revenue'].sum().reset_index()

monthly['t'] = np.arange(len(monthly))  # Time index

X = monthly[['t']]
y = monthly['Revenue']

# Train-Test Split (No shuffle for time series)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# Model Training
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("\nModel Performance:")
print("R2 Score:", r2_score(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))

# -----------------------------
# Forecast Next 6 Months
# -----------------------------
future_t = pd.DataFrame({
    't': np.arange(len(monthly), len(monthly) + 6)
})

future_forecast = model.predict(future_t)

print("\nFuture 6 Months Forecast:")
print(future_forecast)

# -----------------------------
# Plot Actual vs Predicted
# -----------------------------
plt.figure(figsize=(10,5))
plt.plot(y_test.values, label="Actual")
plt.plot(y_pred, label="Predicted")
plt.title("Actual vs Predicted Sales")
plt.xlabel("Time Index")
plt.ylabel("Revenue")
plt.legend()
plt.show()