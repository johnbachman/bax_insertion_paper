from itertools import product
import numpy as np
import pandas as pd
from openpyxl import load_workbook


def parse_data(data_file, nbd_residues, activators, datatypes, reps, col_types,
               FIRST_COL_INDEX, FIRST_ROW_INDEX, LAST_ROW_INDEX,
               sheet_name='Dataset'):
    """Parse kinetic data from Excel spreadsheets."""
    wb = load_workbook(data_file, data_only=True)

    # Load the worksheet with the data
    sheet = wb[sheet_name]

    # Initialize some values before iterating
    col_index = FIRST_COL_INDEX
    col_tuples = []
    data = []

    # For all residues...
    for nbd_ix, nbd_residue in enumerate(nbd_residues):
        # ...and replicates...
        for rep_ix, rep in enumerate(reps):
            # ...and activators...
            for act_ix, activator in enumerate(activators):
                # Set the time vector to None so we can make sure that it is set
                # correctly
                time_vector = None
                # Now iterate over the Time, Release, FRET, NBD columns
                for dtype_ix, dtype in enumerate(datatypes):
                    # Skip the FRET and NBD datatypes if we're currently on the
                    # WT Bax section
                    if nbd_residue == 'WT' and \
                       (dtype == 'FRET' or dtype == 'NBD'):
                        col_index += 1
                        continue
                    # Iterate and fill the array of column values
                    value_vector = []
                    data_col = list(sheet.columns)[col_index]\
                                             [FIRST_ROW_INDEX:LAST_ROW_INDEX]
                    for cell in data_col:
                        if (cell.value == None):
                            value_vector.append(np.nan)
                        else:
                            value_vector.append(float(cell.value))
                    # If this is the time column, get and save the time vector
                    if dtype_ix == 0:
                        time_vector = value_vector
                    # Otherwise, get the data and add it along with a time
                    # column
                    else:
                        assert time_vector is not None
                        time_tuple = (activator, dtype, nbd_residue, rep,
                                      'TIME')
                        value_tuple = (activator, dtype, nbd_residue, rep,
                                       'VALUE')
                        col_tuples.append(time_tuple)
                        col_tuples.append(value_tuple)
                        data.append(time_vector)
                        data.append(value_vector)
                    # Increment the index of the current column
                    col_index += 1
    # Create the Pandas dataframe
    data_matrix = np.array(data)
    col_multi_index = pd.MultiIndex.from_tuples(col_tuples,
                        names=('Activator', 'Datatype', 'NBD Site', 'Replicate',
                               'Column'))
    df = pd.DataFrame(data_matrix.T,
                      index=range(LAST_ROW_INDEX - FIRST_ROW_INDEX),
                      columns=col_multi_index)
    return df
