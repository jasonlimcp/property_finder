import pandas as pd
import matplotlib.pyplot as plt
import io

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

def get_filtered_table(propname,postdist,propsize_min,propsize_max,newsaleyear,csv_file="data/realis_processed.csv"):
    df = pd.read_csv(csv_file)
    
    if propname != "All":
        df = df.loc[(df['Project Name']==propname)]
    if postdist != "All":
        df['Postal District'].astype(int)
        df = df.loc[(df['Postal District']==int(postdist))]
    if newsaleyear != "All":
        df['New Sale Datetime'] = pd.to_datetime(df['New Sale Datetime'])
        df = df.loc[(df['New Sale Datetime'].dt.year>=int(newsaleyear))]

    df['Area (SQFT)'].astype(int)
    df = df.loc[(df['Area (SQFT)'].between(int(propsize_min), int(propsize_max)))]
    
    return df

def get_stats(df):
    df.astype({'Price Differential (%)': 'float', 'Annualized Growth': 'float'})
    df_stats = df[['Price Differential (%)','Annualized Growth']].describe()
    dict_stats = df_stats.fillna(0).to_dict()
    
    return dict_stats

def get_chart_pricediff(df):
    
    df = df[["Project Name", "Area (SQFT)","Postal District","Market Segment","Property Age (Years)","Price Differential (%)"]]
    df_visual = df.copy()
    df_visual['Price Differential (%)'] = df_visual['Price Differential (%)'].apply(lambda x: x*100)
    
    
    plt.hist(df_visual['Price Differential (%)'], color = '#1f77b4', edgecolor = 'black',
            bins = int(1/0.01))

    plt.title('Range of Capital Gains/Losses')
    plt.xlabel('Gain/Loss on Sale (%)')
    plt.ylabel('No. of Transactions')

    chart_pricediff = io.BytesIO()
    plt.savefig(chart_pricediff, format='png')
    plt.clf()
    chart_pricediff.seek(0)

    return chart_pricediff

def get_chart_anngrowth(df):
    
    df = df[["Project Name", "Area (SQFT)","Postal District","Market Segment","Property Age (Years)","Annualized Growth"]]
    df_visual = df.copy()
    df_visual['Annualized Growth'] = df_visual['Annualized Growth'].apply(lambda x: x*100)

    plt.hist(df_visual['Annualized Growth'], color = '#1f77b4', edgecolor = 'black',
            bins = int(0.5/0.005), range=(df_visual['Annualized Growth'].min(), df_visual['Annualized Growth'].max() if df_visual['Annualized Growth'].max()<=100 else 100))

    plt.title('Range of Annualized Growth')
    plt.xlabel('Price Growth/Year (%)')
    plt.ylabel('No. of Transactions')

    chart_anngrowth = io.BytesIO()
    plt.savefig(chart_anngrowth, format='png')
    plt.clf()
    chart_anngrowth.seek(0)

    return chart_anngrowth