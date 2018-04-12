import pandas as pd


raw = pd.read_csv('/home/datapriest/Project/ochki/products.csv')

#print(raw)
print(raw['category'].value_counts())