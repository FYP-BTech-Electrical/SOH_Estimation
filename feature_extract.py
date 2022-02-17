import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage.filters as filters


def add_features(df):
    df_cell = pd.DataFrame()

    for i in df['charge_cycle'].unique():
        data = df[df['charge_cycle'] == i]
        data = data[(data['Voltage_measured'] < 4.2) & (data['Current_charge'] >= 1.4)]
        # charge in Ah
        data['charge'] = (data['Time'] * data['Current_measured']) / 3600

        data['incremental_capacity'] = data['charge'].diff(periods=6) / data['Voltage_measured'].diff(periods=6)
        data['incremental_capacity_smooth'] = filters.gaussian_filter1d(data['incremental_capacity'],sigma=25)
        data['incremental_capacity_ma'] = data['incremental_capacity'].rolling(20).mean()
        df_cell = df_cell.append(data,ignore_index=True)

    return df_cell

if __name__=="__main__":
    data = pd.read_csv('charge_cycle.csv')

    df = pd.DataFrame()
    cells = ['b5', 'b6', 'b7', 'b18']
    for cell in cells:
        data_cell = data[data['Battery'] == cell]
        d = add_features(data_cell)
        df  = df.append(d,ignore_index=True)


