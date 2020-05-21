#import libraries
import pandas as pd
import csv
import matplotlib.pyplot as plt
import nltk

#import CSV file as a Pandas dataframe
data = pd.read_csv('success_widget.csv', index_col = 0)

#Separate English and French data
data_en = data[data['Page URL'].str.contains("/en", na=False)]

data_fr = data[data['Page URL'].str.contains("/fr", na=False)]

#look at what's wrong
what_en = data_en["What's wrong"]
what_fr = data_fr["What's wrong"]


#plot what's wrong

what_en.value_counts().sort_index().plot.bar(x='Reason', y='Number of occurrences')
plt.show()

what_fr.value_counts().sort_index().plot.bar(x='Raisons', y="Nombre d'occurences")
plt.show()



#analyzing words
word_list_en = data_en["Details"].tolist()
word_list_en = [str(i) for i in word_list_en]
all_words_en = ' '.join([str(elem) for elem in word_list_en])
from nltk.tokenize import word_tokenize
tokens_en = word_tokenize(all_words_en)
words_en = []
for word in tokens_en:
        words_en.append(word.lower())

nltk.download('stopwords')
sw = nltk.corpus.stopwords.words('english')
words_ns_en = []
for word in words_en:
        if word not in sw:
            words_ns_en.append(word)

from nltk import FreqDist
fdist1 = FreqDist(words_ns_en)
most_common_en = fdist1.most_common(30)
print(most_common_en)
