import requests
import csv
import numpy as np
import scipy.stats
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import pdb

# pull data from google spreadsheet
response = requests.get('https://docs.google.com/spreadsheet/ccc?key=0Ar4H2kiPmGtNdFBWa2FlalVONHpKaTlMekFvTThkeEE&output=csv')
assert response.status_code == 200, 'Wrong status code'

# I feel like there must be a more direct way to extract all of this into
# a numpy array...
csv_data = csv.reader(response.content.split('\n'))

list_data  = list()
for row in csv_data:
    for i, entry in enumerate(row):
        if entry == '':
            row[i] = np.nan
    list_data.append(row)
np_data = np.array(list_data)

# raw data from columns
date = np.array(np_data[2:, 0], dtype='str')
brand = np.array(np_data[2:, 1], dtype='str')
weight = np.array(np_data[2:, 2], dtype='float32')
temp = np.array(np_data[2:, 3], dtype='float32')
time = np.array(np_data[2:, 4], dtype='float32')
ratings = np.array(np_data[2:, 5:9], dtype='float32')
aroma = np.array(np_data[2:, 9:13], dtype='str')
flavor = np.array(np_data[2:, 13:17], dtype='str')

# manipulated data
average_ratings = scipy.stats.nanmean(ratings, axis=1)

# plottage
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
p = ax.scatter(weight, temp, time, c=average_ratings)

ax.set_xlabel('Weight (g)')
ax.set_ylabel(u'Temperature (\N{DEGREE SIGN}F)')
ax.set_zlabel('Brew time (s)')

cb = fig.colorbar(p)
cb.set_label('Average rating')
fig.savefig('3d_colorbar.pdf')

