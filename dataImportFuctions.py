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
            print('key= ', key)
            print(np.shape(dic[key]))
    
    if print_bool==True:
        for key in sorted(dic.keys()):
            print(f"{key}: shape = {dic[key].shape}")

    return dic


def TS_extractor(main_data_dic,
                    index_list, 
                    print_bool=False):

    # Dictionary to store arrays
    dic_2back_TSs = {}
    dic_0back_TSs = {}
    dic_entire_TSs = {}
    #group_size = 12
    # total_rows = 144
    # selected_rows = [i for i in range(total_rows) if (i // group_size) % 2 != 0]

    for i in index_list:  # Range from 001 to 020
        
        TS_2back= []
        TS_0back= []
        TS_entire= []

        keyTS = f'{i:03d}'  
        if print_bool==True:
            print(f"main_data_dic[{keyTS}].shape= ", main_data_dic[keyTS].shape,
                  " with the key as ", keyTS)
        
        N_parcels= main_data_dic[keyTS].shape[1]
        for j in range(6):
            # if print_bool==True:  
            #     print(f"{j+1}-th one minute:")
            #key_12TimePoint_FCs= keyTS + f'{j+1}'

            #2-back FCs
            rows_2back= [12*(2*j+1)+k for k in range(12)] 
            # if print_bool==True:  
            #     print("rows_2back= ", rows_2back)
            
            twoback_TS_30secs= main_data_dic[keyTS][rows_2back, :]
            # if print_bool==True:
            #     print("twoback_TS_30secs.shape= ", twoback_TS_30secs.shape)
            #     #print("twoback_TS_30secs= ", twoback_TS_30secs)
            
            TS_2back.append(twoback_TS_30secs)
            #print("dic_AAL3_controls_2back_FCs[key_0_2back_FCs]= ", dic_AAL3_controls_2back_FCs[key_0_2back_FCs])
            # if print_bool==True:
            #     print(f"dic_2back_FCs[{key_12TimePoint_FCs}].shape= ",
            #           dic_2back_FCs[key_12TimePoint_FCs].shape)

            #0-back FCs
            rows_0back= [12*(2*j)+k for k in range(12)]
            # if print_bool==True:  
            #     print("0back_rows= ", rows_0back)
            # zeroback_TS_30secs= np.zeros((12,166))

            zeroback_TS_30secs = main_data_dic[keyTS][rows_0back, :]
            # if print_bool==True:
                # print("zeroback_TS_30secs.shape= ", zeroback_TS_30secs.shape)
                # #print("zeroback_TS_30secs= ", zeroback_TS_30secs)
            #print("dic_AAL3_controls_0back_FCs[key_0_2back_FCs]= ", dic_AAL3_controls_0back_FCs[key_0_2back_FCs])

            # if print_bool==True:
            #     print(f"dic_0back_FCs[{key_12TimePoint_FCs}].shape= ",
            #         dic_0back_FCs[key_12TimePoint_FCs].shape)

            TS_0back.append(zeroback_TS_30secs)

        #entire
        TS_entire= main_data_dic[keyTS]

        TS_2back= np.array(TS_2back)
        TS_0back= np.array(TS_0back)
        TS_entire= np.array(TS_entire)
            
        TS_2back = TS_2back.reshape(-1, N_parcels)
        TS_0back = TS_0back.reshape(-1, N_parcels)

        dic_2back_TSs[keyTS]= TS_2back
        dic_0back_TSs[keyTS]= TS_0back
        dic_entire_TSs[keyTS]= TS_entire



            #2 minus 0 back FCs
            #print("dic_AAL3_controls_2minus0_FCs[key_0_2back_FCs]= ", dic_AAL3_controls_2minus0_FCs[key_0_2back_FCs])
            # if print_bool==True:
            #     print(f"dic_2minus0_FCs[{key_12TimePoint_FCs}].shape= ",
            #         dic_2minus0_FCs[key_12TimePoint_FCs].shape)
    return  dic_2back_TSs, dic_0back_TSs, dic_entire_TSs
            
        #print(np.shape(dic_AAL3_controls[key]))

    # for key in sorted(dic_AAL3_controls_2minus0_FCs.keys()):
    #     print(f"{key}: shape = {dic_AAL3_controls_2minus0_FCs[key].shape}")
    #     FC_matrix_dfs_plot([dic_AAL3_controls_2minus0_FCs[key]])

def TS_extractor_v2(main_data_dic,
                    index_list, 
                    print_bool=False):

    # Dictionary to store arrays
    dic_2back_TSs = {}
    dic_0back_TSs = {}
    dic_entire_TSs = {}
    #group_size = 12
    # total_rows = 144
    # selected_rows = [i for i in range(total_rows) if (i // group_size) % 2 != 0]

    for key in main_data_dic.keys():  # Range from 001 to 020
        
        TS_2back= []
        TS_0back= []
        TS_entire= []

        # keyTS = f'{i:03d}' 
        keyTS = key 
        if print_bool==True:
            print(f"main_data_dic[{keyTS}].shape= ", main_data_dic[keyTS].shape,
                  " with the key as ", keyTS)
        
        N_parcels= main_data_dic[keyTS].shape[1]
        for j in range(6):
            # if print_bool==True:  
            #     print(f"{j+1}-th one minute:")
            #key_12TimePoint_FCs= keyTS + f'{j+1}'

            #2-back FCs
            rows_2back= [12*(2*j+1)+k for k in range(12)] 
            # if print_bool==True:  
            #     print("rows_2back= ", rows_2back)
            
            twoback_TS_30secs= main_data_dic[keyTS][rows_2back, :]
            # if print_bool==True:
            #     print("twoback_TS_30secs.shape= ", twoback_TS_30secs.shape)
            #     #print("twoback_TS_30secs= ", twoback_TS_30secs)
            
            TS_2back.append(twoback_TS_30secs)
            #print("dic_AAL3_controls_2back_FCs[key_0_2back_FCs]= ", dic_AAL3_controls_2back_FCs[key_0_2back_FCs])
            # if print_bool==True:
            #     print(f"dic_2back_FCs[{key_12TimePoint_FCs}].shape= ",
            #           dic_2back_FCs[key_12TimePoint_FCs].shape)

            #0-back FCs
            rows_0back= [12*(2*j)+k for k in range(12)]
            # if print_bool==True:  
            #     print("0back_rows= ", rows_0back)
            # zeroback_TS_30secs= np.zeros((12,166))

            zeroback_TS_30secs = main_data_dic[keyTS][rows_0back, :]
            # if print_bool==True:
                # print("zeroback_TS_30secs.shape= ", zeroback_TS_30secs.shape)
                # #print("zeroback_TS_30secs= ", zeroback_TS_30secs)
            #print("dic_AAL3_controls_0back_FCs[key_0_2back_FCs]= ", dic_AAL3_controls_0back_FCs[key_0_2back_FCs])

            # if print_bool==True:
            #     print(f"dic_0back_FCs[{key_12TimePoint_FCs}].shape= ",
            #         dic_0back_FCs[key_12TimePoint_FCs].shape)

            TS_0back.append(zeroback_TS_30secs)

        #entire
        TS_entire= main_data_dic[keyTS]

        TS_2back= np.array(TS_2back)
        TS_0back= np.array(TS_0back)
        TS_entire= np.array(TS_entire)
            
        TS_2back = TS_2back.reshape(-1, N_parcels)
        TS_0back = TS_0back.reshape(-1, N_parcels)

        dic_2back_TSs[keyTS]= TS_2back
        dic_0back_TSs[keyTS]= TS_0back
        dic_entire_TSs[keyTS]= TS_entire



            #2 minus 0 back FCs
            #print("dic_AAL3_controls_2minus0_FCs[key_0_2back_FCs]= ", dic_AAL3_controls_2minus0_FCs[key_0_2back_FCs])
            # if print_bool==True:
            #     print(f"dic_2minus0_FCs[{key_12TimePoint_FCs}].shape= ",
            #         dic_2minus0_FCs[key_12TimePoint_FCs].shape)
    return  dic_2back_TSs, dic_0back_TSs, dic_entire_TSs
            
        #print(np.shape(dic_AAL3_controls[key]))

    # for key in sorted(dic_AAL3_controls_2minus0_FCs.keys()):
    #     print(f"{key}: shape = {dic_AAL3_controls_2minus0_FCs[key].shape}")
    #     FC_matrix_dfs_plot([dic_AAL3_controls_2minus0_FCs[key]])