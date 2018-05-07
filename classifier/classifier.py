from sklearn.preprocessing import OneHotEncoder, LabelEncoder, LabelBinarizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectPercentile, SelectFromModel
from sklearn.multiclass import OneVsRestClassifier

from sklearn.pipeline import FeatureUnion, Pipeline

from .transformers import *


debugger = ('debug', DebugTransformer())

pipeline = Pipeline([
    ('features', FeatureUnion([
        ('norm_SCH_NAME', Pipeline([
            ('extract', ColumnExtractor('norm_SCH_NAME')),
            ('vectorize', CountVectorizer(ngram_range=(1, 2))),
            ('select', SelectPercentile(percentile=5)),
            #('ovr', OneVsRestClassifier(estimator = LinearSVC(random_state=0))),
            
                #loss='modified_huber')))
            #('classify', LinearSVC())
            #debugger  # uncomment this to inspect ouput of ModelTransformer
        ])),
        ('ST', Pipeline([
          ('extract', ColumnExtractor(['ST'])),
          ('gd', GetPandasDummies()),
          
           
        ])),
    ])),
    ('classifier', OneVsRestClassifier(LinearSVC()))
])
