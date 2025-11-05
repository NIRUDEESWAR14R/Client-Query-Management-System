# src/eda_analysis.py

import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# --- Database Connection ---
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="client_query_db"   # ✅ Correct DB name
)

# --- Load Data ---
df = pd.read_sql("SELECT * FROM queries", db)
print(f"\n✅ Connected to database: client_query_db")
print(f"📊 Total rows in 'queries' table: {len(df)}")

# --- Convert Date Columns ---
df['date_raised'] = pd.to_datetime(df['date_raised'], errors='coerce')
df['date_closed'] = pd.to_datetime(df['date_closed'], errors='coerce')

# --- Handle missing or invalid 'date_closed' values ---
df['resolution_days'] = (df['date_closed'] - df['date_raised']).dt.days
df['resolution_days'].fillna(0, inplace=True)  # replace NaN with 0 if still open

# --- Outlier Detection ---
Q1 = df['resolution_days'].quantile(0.25)
Q3 = df['resolution_days'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['resolution_days'] < (Q1 - 1.5 * IQR)) | (df['resolution_days'] > (Q3 + 1.5 * IQR))]
print(f"\n⚠️ Outliers found: {len(outliers)} ({(len(outliers)/len(df))*100:.2f}% of total rows)")

# --- Correlation / Average Resolution Time by Status ---
status_duration = df.groupby('status')['resolution_days'].mean()
print("\n📈 Average resolution time by status:\n", status_duration)

# --- Seasonality Check ---
if 'date_raised' in df.columns:
    df['month'] = df['date_raised'].dt.month
    monthly_counts = df['month'].value_counts().sort_index()

    print("\n🗓️ Monthly query distribution:")
    print(monthly_counts)

    # Optional: visualize monthly distribution
    try:
        monthly_counts.plot(kind='bar', title='Monthly Query Volume', xlabel='Month', ylabel='Number of Queries')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print("\n(📉 Plot skipped - likely running in console environment)")
else:
    print("\n⚠️ Column 'date_raised' not found; skipping monthly analysis.")

# --- Encode Categorical Columns for ML ---
df_encoded = pd.get_dummies(df, columns=['status'], drop_first=True)
print("\n🧩 Encoded columns added for modeling:\n", df_encoded.columns)

# --- Save EDA Summary ---
summary = {
    "Total Rows": [len(df)],
    "Outliers Found": [len(outliers)],
    "Avg Resolution (Closed)": [status_duration.get("Closed", None)],
    "Avg Resolution (Opened)": [status_duration.get("Opened", None)],
}

summary_df = pd.DataFrame(summary)
summary_df.to_csv("eda_results.csv", index=False)
print("\n💾 EDA summary saved to 'eda_results.csv'")
