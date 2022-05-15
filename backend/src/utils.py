import pandas as pd
import matplotlib.pyplot as plt

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

def get_sales_stats(propname,postdist,propsize_min,propsize_max,newsaleyear,csv_file="data/realis_processed.csv"):
    df = pd.read_csv(csv_file)
    
    if propname != "All":
        df = df.loc[(df['Project Name']==propname)]
    if postdist != "All":
        df['Postal District'].astype(int)
        df = df.loc[(df['Postal District']==postdist)]
    if newsaleyear != "All":
        df['New Sale Datetime'] = pd.to_datetime(df['New Sale Datetime'])
        df = df.loc[(df['New Sale Datetime'].dt.year>=newsaleyear)]

    df['Area (SQFT)'].astype(int)
    df = df.loc[(df['Area (SQFT)'].between(int(propsize_min), int(propsize_max)))]
    

    df = df[['Project Name','Postal District','Area (SQFT)','New Sale Datetime']]
    count = len(df)
    
    return count


def get_charts(csv_file="data/realis_processed.csv"):
    df_final = pd.read_csv(csv_file)
    
    df_visual = df_final[["Project Name", "Area (SQFT)","Postal District","Market Segment","Property Age (Years)","Price Differential (%)","Annualized Growth"]]

    df_visual.groupby('Market Segment')['Price Differential (%)'].describe()
    df_visual.groupby('Market Segment')['Annualized Growth'].describe()

    district_rank = df_visual.groupby('Postal District')['Annualized Growth'].mean()
    district_rank.sort_values(ascending=False)

    plt.hist(df_visual['Price Differential (%)'], color = '#1f77b4', edgecolor = 'black',
            bins = int(1/0.01))

    plt.title('Range of Capital Gains/Losses')
    plt.xlabel('Price Differential')
    plt.ylabel('Number of Transactions')

    plt.hist(df_visual['Annualized Growth'], color = '#1f77b4', edgecolor = 'black',
            bins = int(0.5/0.005))

    plt.title('Range of Annualized Growth')
    plt.xlabel('Annualized Growth')
    plt.ylabel('Number of Transactions')
    