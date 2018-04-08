import argparse
import numpy as np
import pandas as pd

from classifier import pipeline


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Evaluate the work order classification model.')
    parser.add_argument('-t', '--train',
                        action='store',
                        default='data/work_orders.clean.csv',
                        dest='train_file',
                        help='Dataset to train on')
    parser.add_argument('-c', '--confusion-matrix',
                        action='store_const',
                        const=True,
                        default=False,
                        dest='confusion_matrix',
                        help='Compute a confusion matrix')
    args = parser.parse_args()

    np.random.seed(0)

    data = pd.read_csv(args.train_file, encoding='iso-8859-1')
    X = data.drop(['Class'], axis=1)
    y = data['Class']

    pipeline.fit(X, y)

    text_pipeline = pipeline.named_steps['features'].transformer_list[0][1]
    feature_names = text_pipeline.named_steps['vectorize'].get_feature_names()
    classes = text_pipeline.named_steps['classify'].model.classes_
    coefs = text_pipeline.named_steps['classify'].model.coef_

    with open('ngrams-by-class.md', 'w') as f:
        for i, class_ in enumerate(classes):
            feature_coefs = list(reversed(sorted(zip(
                coefs[i], feature_names))))
            top_50 = feature_coefs[:50]
            f.write("\n## {}\n".format(class_))
            f.write("| Term | Coefficient |\n")
            f.write("| --- | --- |\n")
            for coef, ngram in top_50:
                f.write("| {} | {} |\n".format(ngram, coef))
