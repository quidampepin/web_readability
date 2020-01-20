#get the url
url = input("Enter a URL: ")

#get the html from the URL
import requests
r = requests.get(url)
html = r.text

#get the html content as text - get content from the "main" tag
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, features="lxml").find('main')
text1 = soup.get_text()

#get initial readability total_score
from readability import Readability
r = Readability(text1)
fk1 = r.flesch_kincaid()

#add periods after bullet points and headings so that the Flesch Kicaid score considers them as sentences
html = html.replace("</li>", ".</li>")
html = html.replace("<h1>", ".</h1>")
html = html.replace("<h2>", ".</h2>")
html = html.replace("<h3>", ".</h3>")
html = html.replace("<h4>", ".</h4>")
html = html.replace("<h5>", ".</h5>")
html = html.replace("<h6>", ".</h6>")

#get adjusted readability total_score
soup = BeautifulSoup(html, features="lxml").find('main')
text = soup.get_text()

from readability import Readability
r = Readability(text)
fk = r.flesch_kincaid()


#tokenize the text for processing
import nltk
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer('\w+')
tokens = tokenizer.tokenize(text)
words = []
for word in tokens:
    words.append(word.lower())

#remove stop words from the tokens to get only the meaningful words
nltk.download('stopwords')
sw = nltk.corpus.stopwords.words('english')
words_ns = []
for word in words:
    if word not in sw:
        words_ns.append(word)

#get the 15 most used words in the text
from nltk import FreqDist
fdist1 = FreqDist(words_ns)
most_common = fdist1.most_common(15)

#get readability score from the text
from readability import Readability
r = Readability(text)
fk = r.flesch_kincaid()

#get all headings and calculate how many words on average between headings
headings = BeautifulSoup(html, features="lxml").findAll(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
hratio = (len(words)/len(headings))

#get all paragraphs and all bulleted list, and calculate how many words per paragraph on average
paragraphs = BeautifulSoup(html, features="lxml").findAll(['p', 'ul'])
pratio = (len(words)/len(paragraphs))

#calculate points for readability
if fk.score <= 6:
    fkpoints = 60
elif fk.score >= 18:
    fkpoints = 0
else :
    fkpoints = (60-((fk.score-6)*5))

#calculate points for number of words between headings
if hratio <= 40:
    hpoints = 20
elif hratio >= 200:
    hpoints = 0
else :
    hpoints = (20-((hratio-40)*0.125    ))

#calculate points for number of words per paragraph
if pratio <= 30:
    ppoints = 20
elif pratio >= 80:
    ppoints = 0
else :
    ppoints = (20-((pratio-30)*0.4))

#add all points
total_score = fkpoints+hpoints+ppoints

#print results
print ('Initial readability score:', format(fk1.score, '.2f'))
print ('Total points:', format(total_score, '.2f'), '/100')
print ('Basic readabilty points:', format(fkpoints, '.2f'), '/60', '(Flesch-Kincaid readability score of:', format(fk.score, '.2f'), ')')
print ('Heading points: ', format(hpoints, '.2f'), '/20', '(words per heading:', format(hratio, '.2f'), ')')
print ('Paragraph points: ', format(ppoints, '.2f'), '/20', '(words per paragraph:', format(pratio, '.2f'), ')')
print('Number of words: ', len(words))
print('Most used words')
print(*most_common,sep='\n')
