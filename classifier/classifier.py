from sklearn.preprocessing import OneHotEncoder, LabelEncoder, LabelBinarizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectPercentile, SelectKBest

from sklearn.pipeline import FeatureUnion, Pipeline

from .transformers import *


debugger = ('debug', DebugTransformer())

pipeline = Pipeline([
    ('features', FeatureUnion([
        ('norm_SCH_NAME', Pipeline([
            ('extract', ColumnExtractor('norm_SCH_NAME')),
            ('vectorize', CountVectorizer(ngram_range=(1, 2))),
            ('select', SelectKBest(k = 100)),
            #('classify', ModelTransformer(SGDClassifier(
             #   loss='modified_huber')))
            #('classify', LinearSVC())
            #debugger  # uncomment this to inspect ouput of ModelTransformer
        ])),
        ('ST', Pipeline([
          ('extract', ColumnExtractor(['ST'])),
          ('gd', GetPandasDummies()),
          
        
        #   ('lb', LabelBinarizer()),
           
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
    ('classifier', LinearSVC())
])
