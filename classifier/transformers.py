from sklearn.base import TransformerMixin
from sklearn.cluster import KMeans
import datetime
import pandas as pd
import pdb


class ColumnExtractor(TransformerMixin):

    def __init__(self, columns=[]):
        self.columns = columns

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def transform(self, X, **transform_params):
        return X[self.columns]

    def fit(self, X, y=None, **fit_params):
        return self


class ClusterTransformer(TransformerMixin):

    def __init__(self, n_clusters):
        self.model = KMeans(n_clusters=n_clusters)

    def transform(self, X, **transform_params):
        return self.model.predict(X).reshape((-1, 1))

    def fit(self, X, y=None, **fit_params):
        self.model.fit(X, y)
        return self


class DebugTransformer(TransformerMixin):

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def transform(self, X, **transform_params):
        pdb.set_trace()
        return X

    def fit(self, X, y=None, **fit_params):
        return self


class FillNaTransformer(TransformerMixin):

    def __init__(self, value):
        self.value = value

    def transform(self, X, **transform_params):
        return X.fillna(self.value)

    def fit(self, X, y=None, **fit_params):
        return self


class ParseDate(TransformerMixin):

    def __init__(self, format):
        self.format = format

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def transform(self, X, **transform_params):
        return pd.to_datetime(X, format=self.format)

    def fit(self, X, y=None, **fit_params):
        return self


class DayOfWeekTransformer(TransformerMixin):
    """Maps datetime's to their day of the week in 0-6 format where 6 is Sunday
    """

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def transform(self, X, **transform_params):
        return X.apply(datetime.date.weekday)

    def fit(self, X, y=None, **fit_params):
        return self


class HourOfDay(TransformerMixin):

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def transform(self, X, **transform_params):
        return X.apply(lambda x: x.hour)

    def fit(self, X, y=None, **fit_params):
        return self


class ModelTransformer(TransformerMixin):

    def __init__(self, model):
        self.model = model

    def fit(self, *args, **kwargs):
        self.model.fit(*args, **kwargs)

    def transform(self, X, y=None, **fit_params):
        return self.model.predict_proba(X)

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)


class SeriesToDataFrame(TransformerMixin):

    def transform(self, X, **transform_params):
        return pd.DataFrame(X)

    def fit(self, X, y=None, **fit_params):
        return self


class IsWeekendTransformer(TransformerMixin):
    """Maps days of week to Weekend or Weekday
    """

    def transform(self, X, **transform_params):
        return X.isin((5, 6))

    def fit(self, X, y=None, **fit_params):
        return self
