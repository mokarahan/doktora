import matplotlib.pyplot as plt

import pandas as pd

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printw(str):
    print(f'{bcolors.WARNING}{str}{bcolors.ENDC}')

def printb(str):
    print(f'{bcolors.OKBLUE}{str}{bcolors.ENDC}')

def plot_test_data(df, figurename='', profile="charge"):
    
    if profile=='summarize':
        plt.figure(figsize=(20,8), num=figurename)
        plt.plot(df.Time, df.Voltage_measured, 'b', label='Voltage_measured')
        plt.plot(df.Time, df.Current_measured, 'r', label='Current_measured')
        plt.plot(df.Time, df.Temperature_measured, 'k', label='Temperature_measured')
        plt.legend()
        plt.show()

    elif profile=='charge':
        plt.figure(figsize=(10,4), num=figurename)
        plt.plot(df.Time, df.Voltage_measured, 'b', label='Voltage_measured')
        plt.plot(df.Time, df.Current_measured, 'r', label='Current_measured')
        plt.legend()
        plt.show()

        plt.figure(figsize=(10,4), num=figurename)
        plt.plot(df.Time, df.Voltage_charge, 'b', label='Voltage_charge')
        plt.plot(df.Time, df.Current_charge, 'r', label='Current_charge')
        plt.legend()
        plt.show()

        plt.figure(figsize=(10,4), num=figurename)
        plt.plot(df.Time, df.Temperature_measured, 'k', label='Temperature_measured')
        plt.legend()
        plt.show()

    elif profile=='discharge':
        plt.figure(figsize=(10,4), num=figurename)
        plt.plot(df.Time, df.Voltage_measured, 'b', label='Voltage_measured')
        plt.plot(df.Time, df.Current_measured, 'r', label='Current_measured')
        plt.legend()
        plt.show()

        plt.figure(figsize=(10,4), num=figurename)
        plt.plot(df.Time, df.Voltage_load, 'b', label='Voltage_load')
        plt.plot(df.Time, df.Current_load, 'r', label='Current_load')
        plt.legend()
        plt.show()

        plt.figure(figsize=(10,4), num=figurename)
        plt.plot(df.Time, df.Temperature_measured, 'k', label='Temperature_measured')
        plt.legend()
        plt.show()

    elif profile=='impedance':
        pass
    else:
        print('No cycle recognized')

def normalize (df: pd.DataFrame, colA: str, newCol:str='', amplify: int=1):
    # Formula: (x - min) / (max - min)
    if newCol != '':
        df[newCol] = (df[colA] - df[colA].min()) / (df[colA].max() - df[colA].min()) * amplify
    if newCol == '':
        df[colA] = (df[colA] - df[colA].min()) / (df[colA].max() - df[colA].min())

def max_discharge_time (df: pd.DataFrame, colA: str='Time'):
    # Formula: max of Time
    return df[colA].max()

def max_temp (df: pd.DataFrame, colA: str='Temperature_measured'):
    return df[colA].max()

def max_temp_time (df: pd.DataFrame, colA: str='Temperature_measured'):
    idx = df.iloc[df[colA].idxmax()]
    return idx['Time']