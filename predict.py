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

latest_build = '8b502e'

path_to_pickle = path.join(BUILDS_PATH, latest_build, BASE, 'data' )

#reinflate pickle
pipeline = joblib.load(path.join(path_to_pickle,'pipeline.pkl' ))

#now get data to predict on

data = pd.DataFrame.from_csv(path.join("DATA", 'AR_un_locations.csv'), index_col = None)

data['norm_SCH_NAME'] = k12_clean(data['LocDesc'].astype(str))

# bring in ST categories

st_categories = pd.Series.from_csv(path.join("Data", "st_categories.csv"))


data['ST'] = data['State'].astype('category')

# add the other state categories
data.ST.cat.set_categories(st_categories, inplace=True)


x_cols = ['norm_SCH_NAME', 'ST']

X = data[x_cols]

y_pred = pipeline.predict(X)

data['y_pred'] = y_pred

y_score_df = pd.DataFrame(data =  pipeline.decision_function(X), columns=pipeline.classes_ )

y_score_df['y_pred'] = y_pred
y_score_df = y_score_df.join(X)

