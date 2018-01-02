#!/usr/bin/python

import sys, getopt
import pandas as pd
import os
from fuzzywuzzy import process

from options import *

helpline = """Usage:
fuzzy_script.py -i <input csv to match> -d <database in Excel> -o <output file name>
default input csv is "Data\AR_un_locations.csv"
default database in Excel is "Data\EDGE_GEOCODE_PUBLICSCH_1516.xlsx"
default output file name is "sample_match.csv"

options are in options.py

fuzzy_script.py -h print this helpline"""


def read_data(input_file, db_file):
    '''
    reads input_file as csv and db_file as first sheet of Excel file

    returns (dataframe_for_input_file, dataframe_for_db)
    '''
    df = pd.read_csv(input_file)
    df.dropna(axis=0, how='any', subset=[EDUCATION_ID], inplace=True)
    df[EDUCATION_ID] = df[EDUCATION_ID].astype(str)

    db = pd.read_excel(db_file)
    db[NCESSCH] = db[NCESSCH].astype(str)

    return (df, db)


def concatenate_sample_fields(row):
    return " ".join([str(row[field[0]])  for field in FIELDS_TO_MATCH]).upper()


def concatenate_db_fields(row):
    return " ".join([str(row[field[1]]) for field in FIELDS_TO_MATCH]).upper()


def extractOne(df, db):
    '''
    for each row in df narows db using EDUCATION_ID and NCESSCH
    then conctate FIELDS_TO_MATCH in df and db
    and then uses fuzzywuzzy.process.extractOne to find best match

    returns list of 3-tuples (ncessch_from_db, fuzzy_score, id_field)
    '''

    df['Query'] = [concatenate_sample_fields(row) for i, row in df.iterrows()]
    df.sort_values('EducationID', inplace=True)

    result = []
    prev_eduid = None
    for id_field, query, eduid in zip(df[ID_FIELD], df.Query, df[EDUCATION_ID]):
        if eduid != prev_eduid:
            prev_eduid = eduid
            db_district = db[db[NCESSCH].str[NCESSCH_START:NCESSCH_END]==eduid[NCESSCH_START:NCESSCH_END]]
            db_rows = [concatenate_db_fields(row) for i, row in db_district.iterrows()]
        best = process.extractOne(query, db_rows)
        if best is None:
            result.append(('', 0, id_field))
        else:
            idx = db_rows.index(best[0])
            ncessch = db_district[NCESSCH].iloc[idx]
            result.append((ncessch, best[1], id_field))
    return result


def fuzzy_match(input_file, db_file, output_file):
    '''
    reads data, makes fuzzy match and saves result to file
    '''
    df, db = read_data(input_file, db_file)
    result = extractOne(df, db)
    df_res = pd.DataFrame(result, columns=[NCESSCH, 'Score', ID_FIELD])
    df_res = pd.merge(df_res, df, on=ID_FIELD, how='left')
    df_res = pd.merge(df_res, db, on=NCESSCH, how='left')
    df_res.to_csv(output_file, index=False)


def main(argv):
    input_file = os.path.join('Data', 'AR_un_locations.csv')
    db_file = os.path.join('Data', 'EDGE_GEOCODE_PUBLICSCH_1516.xlsx')
    result_file = 'sample_match.csv'
    try:
        opts, args = getopt.getopt(argv,"hi:d:o:",["ifile=", "db=", "ofile="])
    except getopt.GetoptError:
        print
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(helpline)
            sys.exit()
        elif opt in ("-i", "--idir"):
            input_file = arg
        elif opt in ("-d", "--db"):
            db_file = arg
        elif opt in ("-o", "--ofile"):
            result_file = arg

    fuzzy_match(input_file, db_file, result_file)

if __name__ == "__main__":
    main(sys.argv[1:])
