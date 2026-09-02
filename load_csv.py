# Created on Mon Oct 30 14:00:00 2023
# Author: mokarahan

import pandas as pd
import argparse
import utils as u

# 1. Initialize the argument parser
parser = argparse.ArgumentParser(description="A script that accepts a filename as an argument and processes the CSV file.")

# 2. Add an argument (positional or optional)
parser.add_argument("--filename", type=str, help="The name of the filename to process")

parser.add_argument("--line", type=int, default=10, help="The line number to display")

# 3. Parse the command-line arguments
args = parser.parse_args()

# 4. Access and use the argument value
print(f"Processing file: {args.filename}")

# Define the path to CSV file
# (Can be a local file path or a direct web URL)
file_path = args.filename
line_number = args.line

try:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Display basic information about the columns and data types
    u.printb("DataFrame Information")
    print(df.info())

    # Open only discharged rows
    df_discharged = df.loc[df['type'] == 'discharge']

    for f_index, f_row in df_discharged.iterrows():
        u.printb(f'Checking discharged record file: {f_row['filename']}')
        df_disc_recs = pd.read_csv(f'./tmp/{f_row['filename']}')
        battery_id = f_row['battery_id']
        test_id =  f_row['test_id']
        capacity =  f_row['Capacity']
        count_row = df_disc_recs.shape[0] 
        figure_title = f'Battery ID: {battery_id} Data File: {f_row['filename']} Capacity: {f_row['Capacity']} Size: {count_row}'
        u.plot_test_data(df_disc_recs, figure_title, profile="summarize")
        
        
        for d_in, d_row in df_disc_recs.iterrows():
            print(
                f'Record at: {d_in} ',
                f'Voltage_Measured: {d_row['Voltage_measured']}, ',
                f'Current_measured: {d_row['Current_measured']}, ',
                f'Temperature_measured: {d_row['Temperature_measured']}',
                f'at: {d_row['Time']}',
            )

except FileNotFoundError:
    print(f"Error: The file at {file_path} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
