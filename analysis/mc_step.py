import sys
import random
import requests
import csv
import numpy as np
import scipy.stats
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import pdb

def take_step(current_params):
    """
    """
    print "Accepting new parameters and taking step.\n"

    maxes = [5.0, 5.0, 10.0]
    new_vals = [0, 0, 0]
    for i, vals in enumerate(zip(current_params, maxes)):
        current = vals[0]
        max_val = vals[1]
        new_vals[i] = int(current + (2 * random.random() * max_val - max_val))

    print "New parameters are: {0}".format(new_vals)
    return new_vals


# pull data from google spreadsheet
response = requests.get('https://docs.google.com/spreadsheet/ccc?key=0Ar4H2kiPmGtNdFBWa2FlalVONHpKaTlMekFvTThkeEE&output=csv')
assert response.status_code == 200, 'Wrong status code'

# pack everything into a numpy array
csv_data = csv.reader(response.content.split('\n'))
list_data  = list()
for row in csv_data:
    for i, entry in enumerate(row):
        if entry == '':
            row[i] = np.nan
    list_data.append(row)
np_data = np.array(list_data)

# extract relevant data
weight = np.array(np_data[2:, 2], dtype='float32')
temp = np.array(np_data[2:, 3], dtype='float32')
time = np.array(np_data[2:, 4], dtype='float32')
ratings = np.array(np_data[2:, 5:9], dtype='float32')
last_params = [weight[-2], temp[-2], time[-2]]
current_params = [weight[-1], temp[-1], time[-1]]

# calc rating stats
np.seterr(invalid='ignore')  # nanstd returns 'nan' for days with only 1 review
mean_ratings = scipy.stats.nanmean(ratings, axis=1)
stdev_ratings = scipy.stats.nanstd(ratings, axis=1)

last_mean = mean_ratings[-2]
last_stdev = stdev_ratings[-2]
current_mean = mean_ratings[-1]
current_stdev = stdev_ratings[-1]

print u"          Weight (g) Temp (\N{DEGREE SIGN}F) Time (s) | Rating"
print "--------------------------------------------------------------"
print u"Last: {0:10.0f} {1:9.0f} {2:8.0f}     | {3:4.3f}\u00B1{4:4.3f}".format(
        last_params[0],
        last_params[1],
        last_params[2],
        last_mean,
        last_stdev)
print u"Current: {0:7.0f} {1:9.0f} {2:8.0f}     | {3:4.3f}\u00B1{4:4.3f}".format(
        current_params[0],
        current_params[1],
        current_params[2],
        current_mean,
        current_stdev)

# accept/reject
if current_mean > last_mean:
    print "\nRatings improved since last step.\n"
    new_vals = take_step(current_params)
else:
    print "Ratings declined since last step.\n"
    print "Sampling from normal...\n"
    sample = np.random.normal(current_mean, current_stdev)
    if sample > last_mean:
        new_vals = take_step(current_params)
    else:
        print "Rejecting new parameters.\n"
        print "Last parameters were: {0}".format(current_params)
