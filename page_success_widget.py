#import libraries
import pandas as pd
import csv
import matplotlib.pyplot as plt

#import CSV file as a Pandas dataframe
data = pd.read_csv('success_widget.csv', index_col = 0)

#Separate English and French data
data_en = data[data['Page URL'].str.contains("/en", na=False)]

data_fr = data[data['Page URL'].str.contains("/fr", na=False)]

#look at what's wrong
what_en = data_en["What's wrong"]

#plot what's wrong

what_en.value_counts().sort_index().plot.bar(x='Reason', y='Number of occurrences')
plt.show()
