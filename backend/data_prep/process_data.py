import pandas as pd

from datetime import datetime
import os

os.chdir("backend/data")

realis_data = 'realis.csv'
df = pd.read_csv(realis_data)

df = df.replace(',','', regex=True)
df = df.astype({'Transacted Price ($)': 'int64',
                 'Area (SQFT)': 'float64',
                 'Unit Price ($ PSF)': 'int64'
                })

#Cleaning: Remove columns not relevant. Save as df_main
df_main = df.drop(columns=['Area (SQM)', 
                           'Unit Price ($ PSM)',
                           'Completion Date',
                           'Postal Code',
                          'Postal Sector'])

df_main['project_address']= df_main['Project Name']+df_main['Address']

#Create New Sale table
df_newsale = df_main.loc[df_main['Type of Sale'] == 'New Sale']
df_newsale = df_newsale.drop(columns=['Type of Sale'])
df_newsale['project_address']= df_newsale['Project Name']+df_newsale['Address']


#Create Resale Table
df_resale = df_main.loc[df_main['Type of Sale'].isin(['Resale'])]
df_resale = df_resale[["Transacted Price ($)", "Unit Price ($ PSF)", "Sale Date","project_address"]]

df_combine = pd.merge(df_newsale, df_resale, how = "inner", on = 'project_address')
df_combine = df_combine.drop(columns=['project_address'])

df_combine.rename(columns={'Transacted Price ($)_x': 'New Sale Price ($)', 
                           'Unit Price ($ PSF)_x': 'New Sale Price (PSF)',
                           'Sale Date_x': 'New Sale Date',
                           'Transacted Price ($)_y': 'Resale Price ($)',
                           'Unit Price ($ PSF)_y': 'Resale Price (PSF)',
                           'Sale Date_y': 'Resale Date'
                          }, inplace=True)


df_combine_copy = df_combine

CCR = [9,10,11,1,2,6]
RCR = [3,4,5,7,8,12,13,14,15,20]
OCR = [16,17,18,19,21,22,23,24,25,26,27,28]

def segment(x):
    if x in CCR:
        return 'CCR'
    elif x in RCR:
        return 'RCR'
    elif x in OCR:
        return 'OCR'
    else:
        return 'Null'

df_combine_copy['Market Segment'] = df_combine_copy.apply(lambda row:
                                                    segment(row['Postal District'])
                                                    , axis = 1)


df_combine_copy['New Sale Datetime'] = df_combine_copy['New Sale Date'].apply(lambda x: datetime.strptime(x,'%d/%m/%Y'))
df_combine_copy['Resale Datetime'] = df_combine_copy['Resale Date'].apply(lambda x: datetime.strptime(x,'%d/%m/%Y'))
df_combine_copy = df_combine_copy.drop(columns=['New Sale Date','Resale Date'])
df_combine_copy = df_combine_copy.loc[df_combine_copy['New Sale Datetime'] < df_combine_copy['Resale Datetime']]
df_final = df_combine_copy

def year_convertor(x):
    y = round(int((x.split()[0]))/365,1)
    return y

df_final['Property Age (Years)'] = df_final.apply(lambda row:
                                                    year_convertor(str(row['Resale Datetime'] - row['New Sale Datetime']))
                                                    , axis = 1)


df_final['Price Differential (%)'] = df_final.apply(lambda row:
                                                    (row['Resale Price (PSF)'] - row['New Sale Price (PSF)'])/row['New Sale Price (PSF)']
                                                    , axis = 1)


df_final['Annualized Growth'] = df_final.apply(lambda row:
                                                    ((1+row['Price Differential (%)'])**(1/row['Property Age (Years)']))-1
                                                    , axis = 1)


df_final.to_csv('realis_processed.csv', index=False)