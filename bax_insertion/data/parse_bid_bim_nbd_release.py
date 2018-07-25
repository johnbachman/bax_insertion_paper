import sys
from os.path import abspath, join, dirname
import bax_insertion.data
from bax_insertion.data import parse_data

data_path = dirname(sys.modules['bax_insertion.data'].__file__)
data_file = abspath(join(data_path, 'KD1_dataset.xlsx'))

# This list must match the order in the spreadsheet exactly
nbd_residues = ['WT', '3', '5', '15', '36', '40', '47', '54', '62', '68', '79',
                '120', '122', '126', '138', '151', '175', '179', '184', '188']

# Zero-indexed
FIRST_ROW_INDEX = 4
LAST_ROW_INDEX = 140
FIRST_COL_INDEX = 1

activators = ['Bid', 'Bim']
datatypes = ['Time', 'Release', 'NBD']
reps = [1, 2, 3]
col_types = ['TIME', 'VALUE']

df = parse_data(data_file, nbd_residues, activators, datatypes, reps, col_types,
                FIRST_COL_INDEX, FIRST_ROW_INDEX, LAST_ROW_INDEX)
