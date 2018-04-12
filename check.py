import pandas as pd


raw = pd.read_csv('/home/datapriest/Project/ochki/0product.csv')

#print(raw)
print(raw['category'].value_counts())