# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 09:21:28 2018
This code merges plaque burden values computed from an algorithm and values from
an excel sheet
@author: David
"""

import pandas as pd

# read algorithm plaque burden data
algorithm_data = pd.read_csv('C:\Users\David\Desktop\Plaque_burden.txt', sep='\s+', header=None)
#algorithm_data = pd.read_csv('C:\Users\David\Desktop\Plaque_burdenraw.txt', sep='\s+', header=None)

# remove png extension from filenames
algorithm_data.iloc[:, 0] = algorithm_data.iloc[:, 0].apply(lambda x: x.split('.png')[0])
algorithm_data.rename(columns={0:'Patient', 1:'Plaque burden mask'}, inplace=True)
algorithm_data.set_index('Patient', inplace=True)

# read labelled data
label_data = pd.read_excel('C:\Users\David\Desktop\Plaque_burden_data.xlsx')

# add the frame number to the patient id
label_data['Patient'] = label_data.apply(lambda x: x['Patient'] + '_' + str(x['Frame']), axis=1)
label_data.set_index('Patient', inplace=True)

# ensure all indices are upper case to facilitate merge
algorithm_data.rename(index=lambda x: x.upper(), inplace=True)
label_data.rename(index=lambda x: x.upper(), inplace=True)

# join dataframes based on the patient id and frame number
combined_data = algorithm_data.join(label_data['Plaque burden'])

# plot linear regression
combined_data.plot(x='Plaque burden', y='Plaque burden mask', kind='scatter')

# write csv file with both plaque burdens
combined_data.to_csv('C:\Users\David\Desktop\Plaque_burden_data.csv', header=False, index=False)