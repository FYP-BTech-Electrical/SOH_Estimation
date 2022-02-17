import pandas as pd
import numpy as np
import mat_to_csv as mat

from glob import glob


"""b5 = mat.load('matlab_data/B0005.mat')['B0005']['cycle']
b7 = mat.load('matlab_data/B0007.mat')['B0007']['cycle']
b6 = mat.load('matlab_data/B0006.mat')['B0006']['cycle']
b18 = mat.load('matlab_data/B0018.mat')['B0018']['cycle']

batteries = {'b5': b5,'b6': b6,'b7': b7, 'b18': b18}

data_charge = pd.DataFrame()
data_discharge = pd.DataFrame()

for key in batteries.keys():
    df_charge, df_discharge = mat.obj_to_dataframe(batteries[key])
    df_charge['Battery'] = key
    df_discharge['Battery'] = key
    data_charge = data_charge.append(df_charge, ignore_index=True)
    data_discharge = data_discharge.append(df_discharge, ignore_index=True)

data_discharge.to_csv('discharge_cycle.csv',index=False)
data_charge.to_csv('charge_cycle.csv', index=False)

"""

#merge all data

file_paths = glob('matlab_data/*.mat')
names = [name.split('\\')[1][:-4] for name in file_paths]

data_charge = pd.DataFrame()
data_discharge = pd.DataFrame()

batteries = {}
for i in range(len(file_paths)):
    print(names[i])
    batteries[names[i]] = mat.load(file_paths[i])[names[i]]['cycle']
    df_charge, df_discharge = mat.obj_to_dataframe(batteries[names[i]])
    df_charge['Battery'] = names[i]
    df_discharge['Battery'] = names[i]
    data_charge = data_charge.append(df_charge, ignore_index=True)
    data_discharge = data_discharge.append(df_discharge, ignore_index=True)

data_discharge.to_csv('csv/discharge_cycle_all.csv',index=False)
data_charge.to_csv('csv/charge_cycle_all.csv', index=False)
