import pandas as pd

def propnames():
     df = pd.read_csv("src/realis_processed.csv")
     prop_list = df['Project Name'].tolist()
     prop_list = sorted(list(set(prop_list)))

     return prop_list