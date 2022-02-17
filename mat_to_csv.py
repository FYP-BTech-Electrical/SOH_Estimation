import pandas as pd
import numpy as np
import h5py
from mat4py import loadmat

from scipy import io



def _check_keys( dict):
    """
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    """
    for key in dict:
        if isinstance(dict[key], io.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict


def _todict(matobj):
    """
    A recursive function which constructs from matobjects nested dictionaries
    """
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, io.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict


def load(filename):
    """
    this function should be called instead of direct scipy.io .loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    """
    data = io.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

def obj_to_dataframe(mat_data):

    '''
    :param mat_data: data in the form of matlab objects
    :return: df_charge and df_discharge
    '''
    print('getting data............')
    df_charge_total = pd.DataFrame()
    df_discharge_total = pd.DataFrame()
    charge_cycle = 0
    discharge_cycle = 0
    for i in range(mat_data.size):
        df_charge = pd.DataFrame()
        df_discharge = pd.DataFrame()
        #print(i)

        if mat_data[i].type == 'charge':
            df_charge['Time'] = mat_data[i].data.Time
            df_charge['Current_charge'] = mat_data[i].data.Current_charge
            df_charge['Voltage_charge'] = mat_data[i].data.Voltage_charge
            df_charge['Temperature_measured'] = mat_data[i].data.Temperature_measured
            df_charge['Current_measured'] = mat_data[i].data.Current_measured
            df_charge['Voltage_measured'] = mat_data[i].data.Voltage_measured
            charge_cycle += 1
            df_charge['charge_cycle'] = np.ones(len(df_charge['Time']))*(charge_cycle)

            #append to main dataframe
            df_charge_total = df_charge_total.append(df_charge, ignore_index= True)

        elif mat_data[i].type == 'discharge':
            df_discharge['Time'] = mat_data[i].data.Time
            df_discharge['Current_load'] = mat_data[i].data.Current_load
            df_discharge['Voltage_load'] = mat_data[i].data.Voltage_load
            df_discharge['Temperature_measured'] = mat_data[i].data.Temperature_measured
            df_discharge['Current_measured'] = mat_data[i].data.Current_measured
            df_discharge['Voltage_measured'] = mat_data[i].data.Voltage_measured
            discharge_cycle += 1
            df_discharge['discharge_cycle'] = np.ones(len(df_discharge['Time']))*(discharge_cycle)

            #append to main to dataframe

            df_discharge_total = df_discharge_total.append(df_discharge, ignore_index= True)

        else:
            continue


    return df_charge_total, df_discharge_total

if __name__=='__main__':

    mat_data = load('matlab_data/B0007.mat')['B0007']['cycle']

    df_charge, df_discharge = obj_to_dataframe(mat_data)


    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    from matplotlib.animation import FuncAnimation

    for i in range(100,len(df_charge['charge_cycle'].unique())):
        fig = plt.figure(dpi=100, figsize=(20, 10), tight_layout=True)
        plot_data = df_charge[df_charge['charge_cycle']==i]
        plt.plot(plot_data['Time'],plot_data['Voltage_measured'])

        plt.xlabel('Time (s)')
        plt.xlim([0,3000])

        plt.title('Charge Cycle - {}'.format(i))
        plt.ylabel('Voltage (V)')
        plt.ylim([3.5, 4.5])
        plt.grid()
        plt.savefig('charge_cycle/cycle_{}'.format(i), bbox_inches='tight')
        plt.close(fig)


    for i in range(100,len(df_discharge['discharge_cycle'].unique())):
        fig = plt.figure(dpi=100, figsize=(20, 10), tight_layout=True)
        plot_data = df_discharge[df_discharge['discharge_cycle']==i]
        plt.plot(plot_data['Time'],plot_data['Voltage_measured'])

        plt.xlabel('Time (s)')
        plt.xlim([0, 3000])
        plt.title('discharge Cycle - {}'.format(i))
        plt.ylabel('Voltage (V)')
        plt.ylim([2,4.5])
        plt.grid()
        plt.savefig('discharge_cycle/cycle_{}'.format(i), bbox_inches='tight')
        plt.close(fig)
