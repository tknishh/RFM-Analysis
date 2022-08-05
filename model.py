import pandas as pd

def recency(recency):
    res = str(recency).split(' ')[0]
    return(int(res))


#main

df = pd.read_csv("data.csv", encoding='unicode_escape')
df['Total'] = df['UnitPrice']*df['Quantity']
m = df.groupby('CustomerID')['Total'].sum()
m = pd.DataFrame(m).reset_index()
freq = df.groupby('CustomerID')['InvoiceDate'].count()
f = pd.DataFrame(freq).reset_index()
df['date'] = pd.to_datetime(df['InvoiceDate'])
df['rank'] = df.sort_values(['CustomerID','date']).groupby(['CustomerID'])['date'].rank(method='min').astype(int)
recent = df[df['rank']==1]
recent['recency'] = recent['date'] - pd.to_datetime('2010-12-01 08:26:00')
recent['recency'] = recent['recency'].apply(recency)
recent = recent[['CustomerID','recency']]
recent = recent.drop_duplicates()
finaldf = f.merge(m,on='CustomerID').merge(recent,on='CustomerID')


print(finaldf)