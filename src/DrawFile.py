# Created on Mon Sep 04 16:37:00 2023
# Author: mokarahan

import pandas as pd
import argparse
import utils as u

SAMPLE_SIZE = 128

# Defining main function
def init():

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)

# Parse arguments
def main():

    # 1. Initialize the argument parser
    parser = argparse.ArgumentParser(description="A script that accepts a filename as an argument and processes the CSV file.")

    # 2. Add an argument (positional or optional)
    parser.add_argument("--filename", type=str, help="Metadata csv to process")

    # 3. Parse the command-line arguments
    args = parser.parse_args()

    # Define the path to CSV file
    # (Can be a local file path or a direct web URL)
    filename = args.filename

    # 4. Access and use the argument value
    print(f"Processing file: {filename}")

    process(filename)


def process(filename: str= './tmp/00001.csv'):

    try:
        df_disc_recs = pd.read_csv(filename)
        figure_title = f'Data File: {filename}'

        u.plot_xyyy(df_disc_recs.Time,
            [df_disc_recs.Voltage_measured, df_disc_recs.Current_measured, df_disc_recs.Temperature_measured],
             figure_title,
            profile="summarize")

        for d_in, d_row in df_disc_recs.iterrows():
            print(
                f'Record at: {d_in} ',
                f'Voltage_Measured: {d_row['Voltage_measured']}, ',
                f'Current_measured: {d_row['Current_measured']}, ',
                f'Temperature_measured: {d_row['Temperature_measured']}',
                f'at: {d_row['Time']}',
            )

    except FileNotFoundError:
        print(f"Error: The file at {filename} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Using the special variable 
# __name__
if __name__=="__main__":
    init()
    main()