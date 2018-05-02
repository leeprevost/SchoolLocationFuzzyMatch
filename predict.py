# -*- coding: utf-8 -*-
"""
Created on Tue May  1 12:29:54 2018

@author: lprevost
"""

from os import path, listdir
from sklearn.externals import joblib
import pandas as pd
from helpers import k12_clean



BASE_PATH = path.dirname(path.realpath(__file__))
BASE = path.basename(BASE_PATH)

BUILDS_PATH = path.join(BASE_PATH, 'builds')

latest_build = 'dcc40f'

path_to_pickle = path.join(BUILDS_PATH, latest_build, BASE, 'data' )

#reinflate pickle
pipeline = joblib.load(path.join(path_to_pickle,'pipeline.pkl' ))

#now get data to predict on

data = pd.DataFrame.from_csv(path.join("DATA", 'AR_un_locations.csv'), index_col = None)

data['norm_SCH_NAME'] = k12_clean(data['LocDesc'].astype(str))

data['ST'] = data['State'].astype('category')

x_cols = ['norm_SCH_NAME', 'ST']

X = data[x_cols]

y_pred = pipeline.predict(X)


