import pandas as pd
import glob
import os
def main(path: str,output_csv_filename: str ):
    '''Inputting all the csv files obtained (the files have to be in the same folder); selecting the desirable entries (i.e. those with external data);
    output the selected entries in a dataframe then to csv file.
    ---args---
    path: str, the path to the directory containing the csv files
    output_csv_filename: str, the name of the csv file this function outputs
    '''
    all_files = glob.glob(path + "/*.csv")
    # a list of csv files you wish to merge, input their paths as str
    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    desired_df = frame[frame['dataset_type'] == 'external_data']
    desired_df = desired_df.drop_duplicates()
    desired_df.to_csv(output_csv_filename, index = False)

if __name__ == "__main__":
    path = 'tmp'
    csv = 'results_table_final.csv'
    main(path, csv)