import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


period = 100
# Create 10 hours of sample data at 1-minute intervals
time_index = pd.date_range("2026-01-01", periods=period, freq="min")
time_index = pd.float_range(0.0, periods=period, freq="min")
df = pd.DataFrame({"temperature": np.random.uniform(0, 30, size=period)}, index=time_index)
print(df)

# Downsample to a target size of 10 rows
target_size = 10
downsampled_df = df.sample(n=target_size, random_state=42, replace=False, weights="temperature")

print(downsampled_df)