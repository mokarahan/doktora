# Created on Mon Oct 30 14:00:00 2023
# Author: mokarahan

import pandas as pd
import argparse
import utils as u

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

# 1. Initialize the argument parser
parser = argparse.ArgumentParser(description="A script that accepts a filename as an argument and processes the CSV file.")

# 2. Add an argument (positional or optional)
parser.add_argument("--filename", type=str, help="Metadata csv to process")
parser.add_argument("--data_dir", type=str, help="Dir of csv data files")
parser.add_argument('--show_figures', action=argparse.BooleanOptionalAction, help="Show figures")
parser.add_argument('--generate_logs', action=argparse.BooleanOptionalAction, help="Generate logs for the battery data")
parser.add_argument('--debug', action=argparse.BooleanOptionalAction, help="Generate Debugging Logs")

# 3. Parse the command-line arguments
args = parser.parse_args()

Sample_Size = 128

# Define the path to CSV file
# (Can be a local file path or a direct web URL)
file_path = args.filename
figure_enabled = args.show_figures
gen_logs = args.generate_logs
data_dir = args.data_dir
debug = args.debug

# 4. Access and use the argument value
if debug :
    print(f"Processing file: {file_path}")

try:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Display basic information about the columns and data types
    if debug :
        u.printb("DataFrame Information")
        print(df.info())

    # Open only discharged rows
    df_discharged = df.loc[df['type'] == 'discharge']

    for f_index, f_row in df_discharged.iterrows():
        filename = f_row['filename']

        if debug :
            u.printb(f'Checking discharged record file: {filename}')

        df_disc_recs = pd.read_csv(f'{data_dir}/{filename}')
        battery_id = f_row['battery_id']
        test_id =  f_row['test_id']
        capacity =  f_row['Capacity']
        count_row = df_disc_recs.shape[0] 
        
        figure_title = f'Battery ID: {battery_id} ' \
            f'Data File: {filename} '      \
            f'Capacity: {f_row['Capacity']} '       \
            f'Size: {count_row}'

        if figure_enabled:
            u.plot_xy(df_disc_recs.Time,
                [df_disc_recs.Voltage_measured, df_disc_recs.Current_measured, df_disc_recs.Temperature_measured],
                figure_title,
                profile="summarize")
        else:
            if debug :
                u.printb(f'Battery data is processed for: {figure_title}' )

        if count_row < Sample_Size:
            u.printe (f'Sample size is bigger than the existing rows in {filename}')
            continue  # Skips the rest of the loop block for number 3

        #if debug:
        u.printg(f'Sampling {Sample_Size} of {count_row} rows in {filename}')

        # Down Sampling to Sample_Size of Rows
        df_interpolated = df_disc_recs.sample(
            n=Sample_Size,
            random_state=42,
            replace=False,
            #weights="Time",
            ignore_index=True 
        ).sort_values(by='Time', ascending=True)

        # Normalize Time column to 1.0 * SampleSize
        u.normalize(df=df_interpolated, colA='Time', newCol='newTime', amplify=Sample_Size)

        print(df_interpolated)

        if figure_enabled:
            u.plot_xy(df_interpolated.newTime,
                [df_interpolated.Voltage_measured, df_interpolated.Current_measured, df_interpolated.Temperature_measured],
                "Down Sampled - " + figure_title,
                profile="summarize")

        if debug :
            u.printb(df_interpolated)

            print(f'Interpolated \
                Col: {df_disc_recs.shape[0]} Row: {df_disc_recs.shape[1]} -> \
                Col: {df_interpolated.shape[0]} Row: {df_interpolated.shape[1]}'
            )
            u.printg(f'For {filename}  \
                Max Discharge Time is: {u.max_discharge_time(df_disc_recs)}  \
                Max Temp is: {u.max_temp(df_disc_recs)} \
                Min Volt is: {u.min_voltage(df_disc_recs)} \
                Max Temp Time is: {u.max_temp_time(df_disc_recs)} \
                Mean Volt is: {u.mean_voltage(df_disc_recs)} \
                ')

        if gen_logs:
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
