#import libraries
import pandas as pd
import csv
import matplotlib.pyplot as plt
import nltk
from wordcloud import WordCloud

#import CSV file as a Pandas dataframe
data = pd.read_csv('success_widget_1.csv', index_col = 0)

    #Separate English and French data
data_en = data[data['Page URL'].str.contains("EN", na=False)]

data_fr = data[data['Page URL'].str.contains("FR", na=False)]

    #look at what's wrong
what = data["What's wrong"]

what_en = data_en["What's wrong"]
what_fr = data_fr["What's wrong"]


#plot what's wrong

what.value_counts().sort_index().plot.barh(title = 'Feedback by reason', x='Reason', y='Number of occurrences')
plt.show()

tasks = data['Tasks']
tasks.value_counts().plot.barh(title = 'Feedback by task', x='Reason', y='Number of occurrences')
plt.show()

#analyzing words
word_list_en = data_en["Details"].tolist()
word_list_en = [str(i) for i in word_list_en]
all_words_en = ' '.join([str(elem) for elem in word_list_en])

#tokenize words
tokenizer = nltk.RegexpTokenizer(r"\w+")
tokens_en = tokenizer.tokenize(all_words_en)
words_en = []
for word in tokens_en:
        words_en.append(word.lower())

#remove nation
words_en = list(filter(('nan').__ne__, words_en))

#remove stop words to get most frequent words
nltk.download('stopwords')
sw = nltk.corpus.stopwords.words('english')
sw.append('covid')
sw.append('19')
words_ns_en = []
for word in words_en:
        if word not in sw:
            words_ns_en.append(word)

from nltk import FreqDist
fdist1 = FreqDist(words_ns_en)
most_common_en = fdist1.most_common(50)
print('Most common words:')
print(most_common_en)

#WordCloud
word_cloud_en = ' '.join(words_ns_en)

wordcloud = WordCloud(max_font_size=40).generate(word_cloud_en)

import matplotlib.pyplot as plt

plt.imshow(wordcloud, interpolation='bilinear')

plt.axis("off")

plt.show()


#look at bigrams


from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
bcf = BigramCollocationFinder.from_words(words_en)
from nltk.corpus import stopwords
stopset = set(stopwords.words('english'))
filter_stops = lambda w: len(w) < 3 or w in stopset
bcf.apply_word_filter(filter_stops)
print('Most common bigrams:')
print(bcf.nbest(BigramAssocMeasures.likelihood_ratio, 20))

#look at trigrams
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
tcf = TrigramCollocationFinder.from_words(words_en)
from nltk.corpus import stopwords
stopset = set(stopwords.words('english'))
filter_stops = lambda w: len(w) < 3 or w in stopset
tcf.apply_word_filter(filter_stops)
print('Most common trigrams:')
print(tcf.nbest(TrigramAssocMeasures.likelihood_ratio, 20))
