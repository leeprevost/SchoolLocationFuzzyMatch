from os import makedirs, path
from sklearn.externals import joblib
from string import Template
import argparse
import numpy as np
import pandas as pd
import shutil

from classifier.classifier import pipeline
from utils import current_git_sha


BASE_PATH = path.dirname(path.realpath(__file__))


README_TEMPLATE = Template("""
# School Name Classifier build

- Version `$version`
- Trained on `$train_file` ($instances instances)

This build artifact includes a trained model, the source code for the model
that was trained, and its python dependencies:

- `setup.py` - package definition and dependencies
- `SchoolLocationFuzzyMatch/*.py` - the model's source code
- `SchoolLocationFuzzyMatch/data/pipeline.pkl` - the trained model

The model is trained against a specific version of the source code and its
dependencies (most importantly sklearn), and while unpickling it in an
environment with other version of these dependencies may work, it is not
recommended and may not work.  See [here][sklearn-persistence] for more
details.

## Usage

(as of production of this, I have not done a VENV)
Add this package to your `requirements.txt` (adjust the relative path as
needed):

```
./SchoolLocationFuzzyMatch
```

Install with pip: `pip install -r requirements.txt`

Load the model and make predictions:

```python
from SchoolLocationFuzzyMatch import load_model

pipeline = load_model()
pipeline.predict(X)
```

[sklearn-persistence]: https://pythonhosted.org/joblib/persistence.html
""".strip())

SETUP_PY_TEMPLATE = Template("""
#!/usr/bin/env python

from distutils.core import setup

setup(name='work_order_classifier',
      version='$version',
      description='School Type Classifier',
      author='Lee Prevost',
      author_email='lee.prevost@dudesolutions.com',
      url='TBD',
      packages=['SchoolLocationFuzzyMatch'],
      package_data={'SchoolLocationFuzzyMatch': ['data/pipeline.pkl']},
      install_requires=[
          'scikit-learn==0.19.0',
          'scipy==0.19.0',
          'pandas==0.20.2',
      ],
      include_package_data=True,
      )
""")


def add_package_setup_to_build(version):
    setup_py = SETUP_PY_TEMPLATE.substitute(version=version)

    with open(path.join(build_path(), 'setup.py'), 'w') as f:
        f.write(setup_py)


def add_readme_to_build(version, train_file, instances):
    readme = README_TEMPLATE.substitute(
        version=version,
        train_file=train_file,
        instances=instances)

    with open(path.join(build_path(), 'README.md'), 'w') as f:
        f.write(readme)


def build_path():
    return path.join(BASE_PATH, 'builds', current_git_sha())


CL_DIR = os.path.join(BASE_PATH, "classifier")

def copy_model_definition_into_build():
    shutil.copyfile(
        path.join(CL_DIR, '__init__.py'),
        path.join(build_path(),  '__init__.py'))
    shutil.copyfile(
        path.join(CL_DIR, 'classifier.py'),
        path.join(build_path(),  'classifier.py'))
    shutil.copyfile(
        path.join(CL_DIR, 'transformers.py'),
        path.join(build_path(), 'transformers.py'))


def ensure_build_dirs_exists():
    makedirs(build_path(), exist_ok=True)
    makedirs(path.join(build_path(), CUR_DIR), exist_ok=True)
    makedirs(path.join(
        build_path(), CUR_DIR, 'data'), exist_ok=True)


def produce_build_artifact(pipeline, train_file, instances):
    ensure_build_dirs_exists()
    joblib.dump(pipeline, path.join(
        build_path(), 'pipeline.pkl'))
    copy_model_definition_into_build()
    add_package_setup_to_build(current_git_sha())
    add_readme_to_build(current_git_sha(), train_file, instances)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Builds a trained model for deployment')
    parser.add_argument('-t', '--train',
                        action='store',
                        default='data/Train_clean_with_support.csv',
                        dest='train_file',
                        help='Dataset to train on')

    args = parser.parse_args()

    np.random.seed(0)

    print('Loading data file...')
    data = pd.read_csv(args.train_file, encoding='iso-8859-1')
    
    x_cols = ['norm_SCH_NAME', 'ST']
    y_col = 'LEVEL'
    
    X = data[x_cols]
    y = data[y_col]

    print('Training the model...')
    pipeline.fit(X, y)

    print('Producing build artifact...')
    instances = len(data)
    produce_build_artifact(pipeline, args.train_file, instances)
    print('Build artifact has been created: {}'.format(build_path()))
