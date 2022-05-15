import pandas as pd

def get_prop_list(csv_file="data/realis_processed.csv"):
     """Get property name list from realis_processed.csv
     csv_file (str): path to processed realist csv file
     """
     """

     Args:
         csv_file (str): _description_. Defaults to "data/realis_processed.csv".

     Returns:
         _type_: list of property names
     """
     df = pd.read_csv(csv_file)
     prop_list = df['Project Name'].tolist()
     prop_list = sorted(list(set(prop_list)))

     return prop_list