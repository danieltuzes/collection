import pandas as pd
import numpy as np

# Generate data
ID = range(1, 11)
values = np.random.uniform(0, 1000000, size=10)
shares = np.random.uniform(0, 1, size=10)

# Create a DataFrame
data = {'ID': ID, 'value': values, 'share': shares}
df = pd.DataFrame(data)

# Save DataFrame to a CSV file
csv_file = 'example_csv_file.csv'
df.to_csv(csv_file, index=False)

# Print the generated DataFrame
print(df)