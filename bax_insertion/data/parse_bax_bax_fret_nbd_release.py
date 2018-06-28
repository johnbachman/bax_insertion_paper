from os.path import abspath, join, dirname
import sys
import bax_insertion.data
from bax_insertion.data import parse_data

data_path = dirname(sys.modules['bax_insertion.data'].__file__)
data_file = abspath(join(data_path, 'KD3_dataset.xlsx'))

# This list must match the order in the spreadsheet exactly
nbd_residues = ['3', '36', '54', '68', '120', '126', '138', '175', '179']

# Zero-indexed
FIRST_ROW_INDEX = 4
LAST_ROW_INDEX = 130
FIRST_COL_INDEX = 1

activators = ['Bid']
datatypes = ['Time', 'Release', 'FRET', 'NBD']
reps = [1, 2, 3]
col_types = ['TIME', 'VALUE']

df = parse_data(data_file, nbd_residues, activators, datatypes, reps, col_types,
                FIRST_COL_INDEX, FIRST_ROW_INDEX, LAST_ROW_INDEX)
