# %% [markdown]
# # Transforming MATLAB files into Machine Learning Reading CSV files
# A new version of this dataset has been published. This dataset explore the original raw dataset and transform it into a Machine Learning ready dataset in a significantly better format.

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:22:00.408122Z","iopub.execute_input":"2022-10-29T20:22:00.408552Z","iopub.status.idle":"2022-10-29T20:22:00.41436Z","shell.execute_reply.started":"2022-10-29T20:22:00.408519Z","shell.execute_reply":"2022-10-29T20:22:00.412996Z"}}
# Some boring imports
import numpy as np
import pandas as pd
import os
import scipy.io

home_path = os.environ.get("HOME")
project_path = f"{home_path}/Dev/Doktora/Dataset/Nasa/"
print ("Project Home: ", project_path)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:22:04.66978Z","iopub.execute_input":"2022-10-29T20:22:04.670241Z","iopub.status.idle":"2022-10-29T20:22:04.678514Z","shell.execute_reply.started":"2022-10-29T20:22:04.670199Z","shell.execute_reply":"2022-10-29T20:22:04.677212Z"}}
# Helper functions
def load_filelist():
    
    FILELIST = []
    for dirname, _, filenames in os.walk(project_path):
        for filename in filenames:

            #filepath = filename
            FILELIST.append(os.path.join(dirname, filename))
    return FILELIST
            
            
def filter_matfiles_list(filelist):
    filelist = [filepath for filepath in filelist if filepath.endswith('.mat')]
    filelist = [filepath for filepath in filelist if "BatteryAgingARC_25_26_27_28_P1" not in filepath] # removing duplicates
    return filelist


def loadmat(filepath):
    #np.set_printoptions(suppress=True, precision=4)
    return scipy.io.loadmat(filepath, simplify_cells=True)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:22:16.548807Z","iopub.execute_input":"2022-10-29T20:22:16.54959Z","iopub.status.idle":"2022-10-29T20:22:16.566778Z","shell.execute_reply.started":"2022-10-29T20:22:16.549535Z","shell.execute_reply":"2022-10-29T20:22:16.56519Z"}}
FILELIST = filter_matfiles_list(load_filelist())

# %% [markdown]
# ## Generic Dataset Informations
# Repeated charge and discharge cycles result in accelerated aging of the batteries while impedance measurements provide insight into the internal battery parameters that change as aging progresses.
# 
# - Charge profile:
#     - The charge profile for all battery tests seems to be identifical.
#     - Charging was carried out in a constant current (CC) mode at 1.5A until the battery voltage reached 4.2V and then continued in a constant voltage (CV) mode until the charge current dropped to 20mA. 
# 
# - Discharge:
#     - Discharge profiles were different from battery to battery.
#     - Discharge was carried out at a constant current (CC) level of 1-4 A until the battery voltage fell to values such 2.7V, 2.5V, 2.2V and 2.5V.
# 
# - Impedance:
#     - Impedance measurement was carried out through an electrochemical impedance spectroscopy (EIS) frequency sweep from 0.1Hz to 5kHz.
# 
# The experiments were stopped when the batteries reached a given end-of-life (EOL) criteria: for example 30% fade in rated capacity (from 2Ahr to 1.4Ahr). Other stopping criteria were used such as 20% fade in rated capacity. Note that for batteries 49,50,51,52, the experiments were not stop due to battery EOL but because the software has crashed.
# 
# # Tasks
# 
# This dataset can be used for the prediction of both:
# - remaining charge (for a given discharge cycle) and,
# - remaining useful life (RUL).

# %% [markdown]
# ## Structure of .mat files
# - **dictionary** (loaded mat file)
#     - **dictionary** (e.g. B0005)
#         - **list (cycle)** -> one test per element in the list
#             - element of the list = dict = all data for one test of that battery
#                 - **type**:  operation  type, can be charge, discharge or impedance
#                 - **ambient_temperature**:  ambient temperature (degree C)
#                 - **time**:  the date and time of the start of the cycle, in MATLAB  date vector format
#                 - **data (dict)**:  data structure containing the measurements
#                     - data fields with key being measured variable, values the actual records (see below)
#                     
#                     
# *    for charge the fields are:
#     *     Voltage_measured: 	Battery terminal voltage (Volts)
#     *     Current_measured:	Battery output current (Amps)
#     *     Temperature_measured: 	Battery temperature (degree C)
#     *     Current_charge:		Current measured at charger (Amps)
#     *     Voltage_charge:		Voltage measured at charger (Volts)
#     *     Time:			Time vector for the cycle (secs)
# *    for discharge the fields are:
#     *     Voltage_measured: 	Battery terminal voltage (Volts)
#     *     Current_measured:	Battery output current (Amps)
#     *     Temperature_measured: 	Battery temperature (degree C)
#     *     Current_load:		Current measured at load (Amps)
#     *     Voltage_load:		Voltage measured at load (Volts)
#     *     Time:			Time vector for the cycle (secs)
#     *     Capacity:		Battery capacity (Ahr) for discharge till 2.7V 
# *    for impedance the fields are:
#     *     Sense_current:		Current in sense branch (Amps)
#     *     Battery_current:	Current in battery branch (Amps)
#     *     Current_ratio:		Ratio of the above currents 
#     *     Battery_impedance:	Battery impedance (Ohms) computed from raw data
#     *     Rectified_impedance:	Calibrated and smoothed battery impedance (Ohms) 
#     *     Re:			Estimated electrolyte resistance (Ohms)
#     *     Rct:			Estimated charge transfer resistance (Ohms)

# %% [markdown]
# ### Differences between README files
# - discharge CC level
# - discharge runs stopped voltage
# - EOL criteria (30% -> 1.4 Ah, 20% -> 1.6 Ah, software crash)

# %% [markdown]
# # TODOs
# - Fill in metadata with new columns to include information from README files...
# - start_time
# 
# **README**
# - 

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:22:20.178164Z","iopub.execute_input":"2022-10-29T20:22:20.178557Z","iopub.status.idle":"2022-10-29T20:22:20.951511Z","shell.execute_reply.started":"2022-10-29T20:22:20.178524Z","shell.execute_reply":"2022-10-29T20:22:20.95041Z"}}
#mat = loadmat("$HOME/Dev/Doktora/DataSets/Nasa/5. Battery Data Set/1. BatteryAgingARC-FY08Q4/B0005.mat")
battery_class="B0006"
file_path = f"{project_path}/5. Battery Data Set/1. BatteryAgingARC-FY08Q4/{battery_class}.mat"
print ("Converted Data File: ", file_path)
mat = loadmat(file_path)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:22:20.953136Z","iopub.execute_input":"2022-10-29T20:22:20.95349Z","iopub.status.idle":"2022-10-29T20:22:20.964747Z","shell.execute_reply.started":"2022-10-29T20:22:20.953459Z","shell.execute_reply":"2022-10-29T20:22:20.962998Z"}}
df = pd.DataFrame(data=mat[battery_class]['cycle'][0]['data'])

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:22:22.648629Z","iopub.execute_input":"2022-10-29T20:22:22.649079Z","iopub.status.idle":"2022-10-29T20:22:22.680637Z","shell.execute_reply.started":"2022-10-29T20:22:22.64904Z","shell.execute_reply":"2022-10-29T20:22:22.679216Z"}}
df.info()

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:22:23.30009Z","iopub.execute_input":"2022-10-29T20:22:23.300818Z","iopub.status.idle":"2022-10-29T20:22:23.314552Z","shell.execute_reply.started":"2022-10-29T20:22:23.300759Z","shell.execute_reply":"2022-10-29T20:22:23.313283Z"}}
import matplotlib.pyplot as plt

def plot_test_data(df, profile="charge"):
    
    if profile=='charge':
        plt.figure(figsize=(10,4))
        plt.plot(df.Time, df.Voltage_measured, 'b', label='Voltage_measured')
        plt.plot(df.Time, df.Current_measured, 'r', label='Current_measured')
        plt.legend()
        plt.show()

        plt.figure(figsize=(10,4))
        plt.plot(df.Time, df.Voltage_charge, 'b', label='Voltage_charge')
        plt.plot(df.Time, df.Current_charge, 'r', label='Current_charge')
        plt.legend()
        plt.show()

        plt.figure(figsize=(10,4))
        plt.plot(df.Time, df.Temperature_measured, 'k', label='Temperature_measured')
        plt.legend()
        plt.show()
    elif profile=='discharge':
        plt.figure(figsize=(10,4))
        plt.plot(df.Time, df.Voltage_measured, 'b', label='Voltage_measured')
        plt.plot(df.Time, df.Current_measured, 'r', label='Current_measured')
        plt.legend()
        plt.show()

        plt.figure(figsize=(10,4))
        plt.plot(df.Time, df.Voltage_load, 'b', label='Voltage_load')
        plt.plot(df.Time, df.Current_load, 'r', label='Current_load')
        plt.legend()
        plt.show()

        plt.figure(figsize=(10,4))
        plt.plot(df.Time, df.Temperature_measured, 'k', label='Temperature_measured')
        plt.legend()
        plt.show()
    elif profile=='impedance':
        pass
    else:
        print('No cycle recognized')

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:22:23.602456Z","iopub.execute_input":"2022-10-29T20:22:23.603718Z","iopub.status.idle":"2022-10-29T20:22:24.313904Z","shell.execute_reply.started":"2022-10-29T20:22:23.603663Z","shell.execute_reply":"2022-10-29T20:22:24.312751Z"}}
plot_test_data(df)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:22:24.315619Z","iopub.execute_input":"2022-10-29T20:22:24.315977Z","iopub.status.idle":"2022-10-29T20:22:24.341033Z","shell.execute_reply.started":"2022-10-29T20:22:24.315931Z","shell.execute_reply":"2022-10-29T20:22:24.339796Z"}}
df = pd.DataFrame(data=mat[battery_class]['cycle'][1]['data'])
df.head()

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:22:24.682116Z","iopub.execute_input":"2022-10-29T20:22:24.682555Z","iopub.status.idle":"2022-10-29T20:22:25.373825Z","shell.execute_reply.started":"2022-10-29T20:22:24.682517Z","shell.execute_reply":"2022-10-29T20:22:25.372641Z"}}
plot_test_data(df, profile='discharge')

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:22:25.375714Z","iopub.execute_input":"2022-10-29T20:22:25.376203Z","iopub.status.idle":"2022-10-29T20:22:25.390646Z","shell.execute_reply.started":"2022-10-29T20:22:25.376166Z","shell.execute_reply":"2022-10-29T20:22:25.389186Z"}}
def process_data_dict(data_dict):
    """ Creates two dictionaries:
    - ndict: new dictionary with the test data to build a corresponding dataframe
    - metadata_dict: anything that doesn't fit in ndict ('Capacity' is just a float)
    """
    
    ndict = {}
    metadata_dict = {}
    for k, v in data_dict.items():
        if k not in ['Capacity', 'Re', 'Rct']:
            ndict[k]=v
        elif k == 'Capacity':
            metadata_dict[k]=v
        elif k == 'Re':
            metadata_dict[k]=v
        elif k == 'Rct':
            metadata_dict[k]=v
        else:
            print("c'est la merde")
    
    return ndict, metadata_dict


def fill_metadata_row(metadata, test_type, test_start_time, test_temperature, battery_name, test_id, uid, filename, capacity, re, rct):
    tmp = pd.DataFrame(data=[test_type, test_start_time, test_temperature, battery_name, test_id, uid, filename, capacity, re, rct])
    tmp = tmp.transpose()
    tmp.columns = metadata.columns
    metadata = pd.concat((metadata, tmp), axis=0)
    return metadata


def extract_more_metadata(metadata_dict):
    
    if 'Capacity' in metadata_dict.keys():
        capacity = metadata_dict['Capacity']
    else:
        capacity = np.nan
        
    if 'Re' in metadata_dict.keys():
        re = metadata_dict['Re']
    else:
        re = np.nan
        
    if 'Rct' in metadata_dict.keys():
        rct = metadata_dict['Rct']
    else:
        rct = np.nan
    
    return capacity, re, rct

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:22:27.711157Z","iopub.execute_input":"2022-10-29T20:22:27.712296Z","iopub.status.idle":"2022-10-29T20:22:27.720353Z","shell.execute_reply.started":"2022-10-29T20:22:27.712244Z","shell.execute_reply":"2022-10-29T20:22:27.719241Z"}}
metadata = pd.DataFrame(data=None, columns=['type', 'start_time', 'ambient_temperature', 'battery_id', 'test_id', 'uid', 'filename', 'Capacity', 'Re', 'Rct'])
battery_list = [item.split('/')[-1].split('.')[0] for item in FILELIST]

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:22:52.032536Z","iopub.execute_input":"2022-10-29T20:22:52.032956Z","iopub.status.idle":"2022-10-29T20:22:52.03907Z","shell.execute_reply.started":"2022-10-29T20:22:52.032905Z","shell.execute_reply":"2022-10-29T20:22:52.038006Z"}}
# We create a tmp directory in which we will save all CSV files
CWD = os.getcwd()
os.listdir(CWD)
directory = "tmp"
path = os.path.join(CWD, directory)
if not os.path.exists(path):
    os.mkdir(path)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:22:52.895601Z","iopub.execute_input":"2022-10-29T20:22:52.896846Z","iopub.status.idle":"2022-10-29T20:22:52.90649Z","shell.execute_reply.started":"2022-10-29T20:22:52.896793Z","shell.execute_reply":"2022-10-29T20:22:52.905171Z"}}
os.listdir(CWD) # we check that tmp exists now

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:23:11.07152Z","iopub.execute_input":"2022-10-29T20:23:11.071981Z","iopub.status.idle":"2022-10-29T20:28:27.382296Z","shell.execute_reply.started":"2022-10-29T20:23:11.071944Z","shell.execute_reply":"2022-10-29T20:28:27.380979Z"}}
uid = 0
# counter = 0
for battery_name, mat_filepath in zip(battery_list, FILELIST):
    # counter +=1
    
    mat_data = scipy.io.loadmat(mat_filepath, simplify_cells=True)
    print(mat_filepath[-10:],"-->", battery_name)
    test_list = mat_data[battery_name]['cycle']
    
    for test_id in range(len(test_list)):
        
        uid += 1
        filename = str(uid).zfill(5)+'.csv'
        filepath = './tmp/' + filename

        # Extract the specific test data and save it as CSV! 
        ndict, metadata_dict = process_data_dict(test_list[test_id]['data'])
        test_df = pd.DataFrame.from_dict(ndict, orient='index')
        test_df = test_df.transpose()

        test_df.to_csv(filepath, index=False)
                
        # Add test information to the metadata
        test_type = test_list[test_id]['type']
        test_start_time = test_list[test_id]['time']
        test_temperature = test_list[test_id]['ambient_temperature']
        
        capacity, re, rct = extract_more_metadata(metadata_dict)
        metadata = fill_metadata_row(metadata, test_type, test_start_time, test_temperature, battery_name, test_id, uid, filename, capacity, re, rct)
        print("CHECK TIME: ", test_start_time)
        
    # if counter > 2:
    #    break

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:28:27.384807Z","iopub.execute_input":"2022-10-29T20:28:27.385254Z","iopub.status.idle":"2022-10-29T20:28:28.396263Z","shell.execute_reply.started":"2022-10-29T20:28:27.385215Z","shell.execute_reply":"2022-10-29T20:28:28.394769Z"}}
metadata.to_csv('metadata.csv', index=False)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:28:28.397989Z","iopub.execute_input":"2022-10-29T20:28:28.398376Z","iopub.status.idle":"2022-10-29T20:28:28.419824Z","shell.execute_reply.started":"2022-10-29T20:28:28.398343Z","shell.execute_reply":"2022-10-29T20:28:28.417772Z"}}
metadata.info()

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:28:28.423671Z","iopub.execute_input":"2022-10-29T20:28:28.424198Z","iopub.status.idle":"2022-10-29T20:28:28.429605Z","shell.execute_reply.started":"2022-10-29T20:28:28.424151Z","shell.execute_reply":"2022-10-29T20:28:28.428281Z"}}
import shutil

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:28:28.431324Z","iopub.execute_input":"2022-10-29T20:28:28.43217Z","iopub.status.idle":"2022-10-29T20:29:20.341771Z","shell.execute_reply.started":"2022-10-29T20:28:28.432116Z","shell.execute_reply":"2022-10-29T20:29:20.340077Z"}}
shutil.make_archive('data', 'zip', 'tmp')

# %% [code]

# %% [markdown]
# ## Problems
# There seems to be a few duplicates for batteries 25,26,27,and 28. Let's actually check the data.
# - By looking at the raw data we confirm that there are duplicates