# Work Order Classifier

## Setup

Install [Python 3](python3). Using Anaconda or a similar distribution will also
work, but you may have different version of the dependencies than those listed
in _requirements.txt_.

Create a [virtual environment][virtualenv] to contain the project's
dependencies. This is recommended, but not necessary.

    python -m venv venv
    source venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Put the cleaned-up CSV in the _data_ directory with the following filename:

    data/work_orders.clean.csv

## Usage

### Model Development and Evaluation

`evaluate.py` is a utility for training the model against a train set and
evaluating it against a test set. It will take a split of the train set to test
if a separate test set is not available.

It will write out a file using the curent git SHA containing individual and
aggregate F1 scores. This is useful for tracking our progress over time. While
developing, when the current evaluation out-scores the current best, copy it to
`evaluation-best.json`:

    cp evaluation-version.json evaluation-best.json

Run `evalute.py` to run a train and CV split that shows aggregate and
individual F1 scores

    python evalute.py --train TRAIN_FILE

By default, `evalute.py` will take a split of the TRAIN_FILE and use it to test.
If you want to train on the entire train file, and test against another, use the
`--test` option:

    python evalute.py --train TRAIN_FILE --test TEST_FILE

If you'd like to see a confusion matrix of the classifier's predictions, add
the `-c` flag:

    python evalute.py --train TRAIN_FILE -c


All usage details are available by running

    python evalute.py --help

### Producing a Trained Model for Deployment

When you need to train the model against an entire training set and produce a
pickle file for deployment, use the `train.py` script. This is not ideal for
using in development/evaluation iteration. You should use the `evaluate.py`
script for this purpose and avoid dumping and loading pickles for evaluation.

`train.py` will produce a self-contained and documented build for deploying to
a production environment. Builds will be put into the `builds` directory with
a version number just like the evaluation files.

    python train.py --train TRAIN_FILE

[python3]: https://www.python.org/downloads/
[virtualenv]: https://docs.python.org/3/library/venv.html
