import numpy as np
import pandas as pd
from scipy.io import loadmat

def main_data_dic_generator(base_dir,
                            file_pattern, 
                            index_list, 
                            parcellation,
                            print_bool=False):
    # Base directory and file pattern
    # base_dir = '/Users/user/NIBS 2 controls Schaeffer300'
    # file_pattern = 'Schaeffer300_AAL3_timeseries_{:03d}_Run1.mat'  # {:03d} will be replaced by numbers with leading zeros
    # print(xxxx)
    # Dictionary to store arrays
    dic = {}

    for i in index_list:  # Range from 001 to 020
        file_name = file_pattern.format(i)
        file_path = f'{base_dir}/{file_name}'
        
        # Load the .mat file
        mat_contents = loadmat(file_path)
        
        # Assuming the main data is stored under a specific key.
        #data_key = next(key for key in mat_contents.keys() if not key.startswith('__'))

        # Convert to DataFrame
        #df = pd.DataFrame(mat_contents[data_key])

        if print_bool==True:
            print(mat_contents.keys())    
        #Schaeffer300 or AAL3
        if parcellation=='Schaeffer300':
            df = pd.DataFrame(mat_contents['Schaeffer_300'])#.transpose()
        if parcellation=='AAL3':
            df = pd.DataFrame(mat_contents['AAL3'])#.transpose()

        # Export to CSV
        if parcellation=='Schaeffer300':
            csv_file_path = f'{base_dir}/{file_name[:-4]}_onlySchaeffer300.csv'
        if parcellation=='AAL3':
            csv_file_path = f'{base_dir}/{file_name[:-4]}_onlyAAL3.csv'

        df.to_csv(csv_file_path, index=False, header=False)
        #print(f"File #{i} has been converted and saved as {csv_file_path}")

    #     print(file_name)
    #     print(file_path)
    #     print(csv_file_path)
        
        key = f'{i:03d}'  # Creates string with leading zeros, e.g., 'array_001'
        dic[key] = df.to_numpy().transpose()
        if print_bool==True:
            print(np.shape(dic[key]))
    
    if print_bool==True:
        for key in sorted(dic.keys()):
            print(f"{key}: shape = {dic[key].shape}")

    return dic