# SchoolLocationFuzzyMatch
Fuzzy matching of school locations to a government database

# How to run script
python fuzzy_script.py -i <input csv to match> -d <database in Excel> -o <output file name>
default input csv is "Data\AR_un_locations.csv"
default database in Excel is "Data\EDGE_GEOCODE_PUBLICSCH_1516.xlsx"
default output file name is "sample_match.csv"

options are in options.py

Most important option is

FIELDS_TO_MATCH = [('LocDesc', 'NAME')]  # list of 2-tuples:
                                         # (field_of_sample, field_of_db)
