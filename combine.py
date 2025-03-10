import pandas as pd

# Load the two CSV files
df1 = pd.read_csv('output_second_final.csv')
df2 = pd.read_csv('output_second_final_1.csv')

# Concatenate the DataFrames
combined_df = pd.concat([df1, df2], ignore_index=True)
combined_df.reset_index(drop=True, inplace=True)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('second_file.csv', index=True)