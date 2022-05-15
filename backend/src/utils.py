import pandas as pd


def get_prop_list(csv_file="data/realis_processed.csv"): #get_prop_list rename
     """Get property list from csv file
     csv_file (str): path to processed realist csv file
     """
     """_summary_

     Args:
         csv_file (str, optional): _description_. Defaults to "data/realis_processed.csv".

     Returns:
         _type_: _description_
     """
     df = pd.read_csv(csv_file)
     prop_list = df['Project Name'].tolist()
     prop_list = sorted(list(set(prop_list)))

     return prop_list