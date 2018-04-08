from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline

from .transformers import *


debugger = ('debug', DebugTransformer())

pipeline = Pipeline([
    ('features', FeatureUnion([
        ('RequestDesc', Pipeline([
            ('extract', ColumnExtractor('RequestDesc')),
            ('vectorize', TfidfVectorizer(ngram_range=(1, 2))),
            ('classify', ModelTransformer(SGDClassifier(
                loss='modified_huber')))
            #debugger  # uncomment this to inspect ouput of ModelTransformer
        ])),
        ('CraftID', Pipeline([
            ('extract', ColumnExtractor(['CraftID'])),
            ('fill_nan', FillNaTransformer(0)),
            ('one_hot', OneHotEncoder())
        ])),
        ('Emergency', ColumnExtractor(['Emergency'])),
        ('PriorityID', Pipeline([
            ('extract', ColumnExtractor(['PriorityID'])),
            ('fill_nan', FillNaTransformer(0)),
            ('one_hot', OneHotEncoder())
        ])),

        # Experiements that haven't been valuable
        #('TimeOfDay', Pipeline([
            #('extract', ColumnExtractor('CreatedOnDate')),
            #('parse', ParseDate('%d%b%Y:%H:%M:%S.%f')),
            #('hour_of_day', HourOfDay()),
            #('up_dim', SeriesToDataFrame()),
            #('cluster', ClusterTransformer(n_clusters=7)),
            #('one_hot', OneHotEncoder()),
        #])),
        #('IsWeekend', Pipeline([
            #('extract', ColumnExtractor('CreatedOnDate')),
            #('parse', ParseDate('%d%b%Y:%H:%M:%S.%f')),
            #('day_of_week', DayOfWeekTransformer()),
            #('up_dim', SeriesToDataFrame()),
            #('is_weekend', IsWeekendTransformer())
        #])),
    ])),
    ('classifier', LogisticRegression())
])
