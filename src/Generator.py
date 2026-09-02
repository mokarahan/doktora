import numpy as np
import pandas as pd
import os
import scipy.io

np.set_printoptions(suppress=True, precision=4)

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
    return scipy.io.loadmat(filepath, simplify_cells=True)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-29T20:22:16.548807Z","iopub.execute_input":"2022-10-29T20:22:16.54959Z","iopub.status.idle":"2022-10-29T20:22:16.566778Z","shell.execute_reply.started":"2022-10-29T20:22:16.549535Z","shell.execute_reply":"2022-10-29T20:22:16.56519Z"}}
FILELIST = filter_matfiles_list(load_filelist())

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
        #print("CHECK TIME: ", test_start_time)
        
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