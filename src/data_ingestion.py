import pandas as pd
import numpy as np
import os

df = pd.read_csv('https://raw.githubusercontent.com/araj2/customer-database/master/Ecommerce%20Customers.csv')
#remove all textual columns
df = df.iloc[:, 3:]
#remove data from length of membership column which has length less than 1
df = df[df['Length of Membership'] > 1]

df.drop(columns=['Time on Website'],inplace=True)
df.to_csv(os.path.join('data','customer.csv'))