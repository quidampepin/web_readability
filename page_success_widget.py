#import libraries
import pandas as pd
import csv
import matplotlib.pyplot as plt
import nltk
from wordcloud import WordCloud

#import CSV file as a Pandas dataframe
data = pd.read_csv('page_success_widget_all.csv', index_col = 0)

    #Separate English and French data
data_en = data[data['Page URL'].str.contains("EN", na=False)]

data_fr = data[data['Page URL'].str.contains("FR", na=False)]

    #look at what's wrong
what = data["What's wrong"]

what_en = data_en["What's wrong"]
what_fr = data_fr["What's wrong"]


#plot what's wrong

plt.rcParams['figure.figsize'] = (10, 6)
plt.gcf().subplots_adjust(left=0.25)
what.value_counts().sort_values().plot.barh(title = 'Feedback by reason', x='Reason', y='Number of occurrences')
plt.show()


#plot by task
tasks = data['Tasks']
tasks = data_en["Tasks"].str.split(", ", n = 3, expand = True)
tasks = tasks.apply(pd.Series.value_counts)
tasks = tasks.fillna(0)
tasks = tasks[0] + tasks[1] + tasks[2]
tasks = tasks.astype(int)
tasks = tasks.sort_values(ascending = False)
plt.rcParams['figure.figsize'] = (14, 8)
plt.gcf().subplots_adjust(left=0.30)
tasks.sort_values().plot.barh(title = 'Feedback by task', x='Reason', y='Number of occurrences')
plt.show()

#analyzing  words
word_list_en = data_en["Details"].tolist()
word_list_en = [str(i) for i in word_list_en]
all_words_en = ' '.join([str(elem) for elem in word_list_en])

word_list_fr = data_fr["Details"].tolist()
word_list_fr = [str(i) for i in word_list_fr]
all_words_fr = ' '.join([str(elem) for elem in word_list_fr])

#tokenize words
tokenizer = nltk.RegexpTokenizer(r"\w+")
tokens_en = tokenizer.tokenize(all_words_en)
words_en = []
for word in tokens_en:
        words_en.append(word.lower())

tokens_fr = tokenizer.tokenize(all_words_fr)
words_fr = []
for word in tokens_fr:
        words_fr.append(word.lower())

#remove nan
words_en = list(filter(('nan').__ne__, words_en))
words_fr = list(filter(('nan').__ne__, words_fr))

#remove English stop words to get most frequent words
nltk.download('stopwords')
sw = nltk.corpus.stopwords.words('english')
sw.append('covid')
sw.append('19')
words_ns_en = []
for word in words_en:
        if word not in sw:
            words_ns_en.append(word)

#Plot English most common words
from nltk import FreqDist
fdist1 = FreqDist(words_ns_en)
most_common_en = fdist1.most_common(50)
most_common_df = pd.DataFrame(most_common_en, columns = ['Word', 'Count'])
most_common_df.plot.barh(title = 'Most frequent words - English - All feedback', x='Word',y='Count')
plt.rcParams['figure.figsize'] = (14, 8)
plt.gcf().subplots_adjust(left=0.20)
plt.show()


#WordCloud English
word_cloud_en = ' '.join(words_ns_en)

wordcloud = WordCloud(max_font_size=40).generate(word_cloud_en)

import matplotlib.pyplot as plt

plt.imshow(wordcloud, interpolation='bilinear')

plt.axis("off")

plt.show()

#remove French stop words

swf = nltk.corpus.stopwords.words('french')
swf.append('covid')
swf.append('19')
swf.append('a')
swf.append('si')
swf.append('avoir')
swf.append('savoir')
swf.append('combien')
swf.append('être')
swf.append('où')
swf.append('comment')
swf.append('puis')
swf.append('peuvent')
swf.append('fait')
swf.append('aucun')
swf.append('bonjour')
swf.append('depuis')
swf.append('chez')
swf.append('faire')
swf.append('peut')
swf.append('plus')
swf.append('veux')
swf.append('dois')
swf.append('doit')
swf.append('dit')
swf.append('merci')
swf.append('cela')
swf.append('pouvons')
swf.append('pouvaient')
swf.append('vers')

words_ns_fr = []
for word in words_fr:
        if word not in swf:
            words_ns_fr.append(word)

#plot most frequent French words
fdist1 = FreqDist(words_ns_fr)
most_common_fr = fdist1.most_common(50)
most_common_df_fr = pd.DataFrame(most_common_fr, columns = ['Mot', 'Nombre'])
most_common_df_fr.plot.barh(title = 'Mots les plus fréquents - Toute la rétroaction - Français', x='Mot',y='Nombre')
plt.rcParams['figure.figsize'] = (14, 8)
plt.gcf().subplots_adjust(left=0.20)
plt.show()


#WordCloud French

word_cloud_fr = ' '.join(words_ns_fr)

wordcloud = WordCloud(max_font_size=40).generate(word_cloud_fr)

import matplotlib.pyplot as plt

plt.imshow(wordcloud, interpolation='bilinear')

plt.axis("off")

plt.show()


#English bigrams

from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
bcf = BigramCollocationFinder.from_words(words_en)
from nltk.corpus import stopwords
stopset = sw
filter_stops = lambda w: len(w) < 3 or w in stopset
bcf.apply_word_filter(filter_stops)
bcf_list = bcf.nbest(BigramAssocMeasures.likelihood_ratio, 20)
bcf_joint_list = []
for words in bcf_list:
        bcf_joint_list.append(' '.join(words))
print('')
print('')
print('Most probable bigrams:')
for item in bcf_joint_list:
        print(item)


#English trigrams
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
tcf = TrigramCollocationFinder.from_words(words_en)
tcf.apply_word_filter(filter_stops)
tcf_list = tcf.nbest(TrigramAssocMeasures.likelihood_ratio, 20)
tcf_joint_list = []
for words in tcf_list:
        tcf_joint_list.append(' '.join(words))
print('')
print('')
print('Most probable trigrams:')
for item in tcf_joint_list:
        print(item)


#French bigrams
bcffr = BigramCollocationFinder.from_words(words_fr)
from nltk.corpus import stopwords
stopsetfr = swf
filter_stopsfr = lambda w: len(w) < 3 or w in stopsetfr
bcffr.apply_word_filter(filter_stopsfr)
bcffr_list = bcffr.nbest(BigramAssocMeasures.likelihood_ratio, 20)
bcffr_joint_list = []
for words in bcffr_list:
        bcffr_joint_list.append(' '.join(words))
print('')
print('')
print('Bigrammes les plus probables :')
for item in bcffr_joint_list:
        print(item)


#French trigrams

from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
tcffr = TrigramCollocationFinder.from_words(words_fr)
tcffr.apply_word_filter(filter_stopsfr)
tcffr_list = tcffr.nbest(TrigramAssocMeasures.likelihood_ratio, 20)
tcffr_joint_list = []
for words in tcffr_list:
        tcffr_joint_list.append(' '.join(words))
print('')
print('')
print('Trigrammes les plus probables :')
for item in tcffr_joint_list:
        print(item)


#look at data by what's wrong value_counts
#most common words info is missing
data_missing_en = data_en[data_en["What's wrong"].str.contains("missing", na=False)]

word_list_missing_en = data_missing_en["Details"].tolist()
word_list_missing_en = [str(i) for i in word_list_missing_en]
all_words_missing_en = ' '.join([str(elem) for elem in word_list_missing_en])

tokenizer = nltk.RegexpTokenizer(r"\w+")
tokens_missing_en = tokenizer.tokenize(all_words_missing_en)
words_missing_en = []
for word in tokens_missing_en:
        words_missing_en.append(word.lower())

words_missing_en = list(filter(('nan').__ne__, words_missing_en))

words_missing_ns_en = []
for word in words_missing_en:
        if word not in sw:
            words_missing_ns_en.append(word)

from nltk import FreqDist
fdist1 = FreqDist(words_missing_ns_en)
most_common_missing_en = fdist1.most_common(50)
most_common_missing_df = pd.DataFrame(most_common_missing_en, columns = ['Word', 'Count'])
most_common_missing_df.plot.barh(title = 'Most frequent words - English - Information is missing', x='Word',y='Count')
plt.rcParams['figure.figsize'] = (14, 8)
plt.gcf().subplots_adjust(left=0.20)
plt.show()


# most common words clear
data_clear_en = data_en[data_en["What's wrong"].str.contains("clear", na=False)]

word_list_clear_en = data_clear_en["Details"].tolist()
word_list_clear_en = [str(i) for i in word_list_clear_en]
all_words_clear_en = ' '.join([str(elem) for elem in word_list_clear_en])

tokenizer = nltk.RegexpTokenizer(r"\w+")
tokens_clear_en = tokenizer.tokenize(all_words_clear_en)
words_clear_en = []
for word in tokens_clear_en:
        words_clear_en.append(word.lower())

words_clear_en = list(filter(('nan').__ne__, words_clear_en))

words_clear_ns_en = []
for word in words_clear_en:
        if word not in sw:
            words_clear_ns_en.append(word)

from nltk import FreqDist
fdist1 = FreqDist(words_clear_ns_en)
most_common_clear_en = fdist1.most_common(50)
most_common_clear_df = pd.DataFrame(most_common_clear_en, columns = ['Word', 'Count'])
most_common_clear_df.plot.barh(title = 'Most frequent words - English - Information is not clear', x='Word',y='Count')
plt.rcParams['figure.figsize'] = (14, 8)
plt.gcf().subplots_adjust(left=0.20)
plt.show()
