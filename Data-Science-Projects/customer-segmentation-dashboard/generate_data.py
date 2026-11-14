import pandas as pd
import numpy as np

np.random.seed(42)

n = 5000

customer_ids = [f"CUST_{i:05d}" for i in range(1, n + 1)]

data = pd.DataFrame({
    "CustomerID": customer_ids,
    "Age": np.random.randint(18, 70, n),
    "Gender": np.random.choice(["Male", "Female"], n),
    "Income": np.random.randint(25000, 200000, n),
    "Total_Purchases": np.random.randint(1, 50, n),
    "Total_Spend": np.round(np.random.uniform(100, 15000, n), 2),
    "Website_Visits": np.random.randint(1, 100, n),
    "Email_Interactions": np.random.randint(0, 50, n),
    "Days_Since_Last_Purchase": np.random.randint(1, 365, n),
    "Avg_Order_Value": np.round(np.random.uniform(20, 1000, n), 2),
    "Category": np.random.choice(
        ["Electronics", "Clothing", "Home", "Beauty", "Sports"],
        n
    )
})

# Create realistic behavioral relationships
data["Total_Spend"] = (
    data["Total_Purchases"] * data["Avg_Order_Value"]
).round(2)

# Introduce a few missing values
for column in ["Income", "Website_Visits", "Email_Interactions"]:
    indexes = np.random.choice(n, 50, replace=False)
    data.loc[indexes, column] = np.nan

# Save dataset
data.to_csv("data/customers.csv", index=False)

print("Dataset created successfully!")
print(f"Total customers: {len(data)}")
print("Saved to: data/customers.csv")
print("\nFirst 5 rows:")
print(data.head())