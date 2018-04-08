from sklearn.externals import joblib
import os
from . import classifier

_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data(path):
    return os.path.join(_ROOT, 'data', path)


def load_classifier():
    pipeline = joblib.load(get_data('pipeline.pkl'))
    return pipeline
