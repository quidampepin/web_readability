from flask import Flask
from flask import request
from flask import app, render_template

app = Flask(__name__)

@app.route('/read_score')

def suggest():

	#get url
    url = request.args.get('url')

    import pandas as pd

    #get the html from the URL
    import requests
    r = requests.get(url)
    html = r.text

    #get the html content as text - get content from the "main" tag
    from bs4 import BeautifulSoup
    original_soup = BeautifulSoup(html, features="lxml").find('main')
    original_text = original_soup.get_text()

    #get initial readability total_score
    from readability import Readability
    r_o = Readability(original_text)
    original_fk = r_o.flesch_kincaid()

    #add periods after bullet points and headings so that the Flesch Kicaid score considers them as sentences
    html1 = html.replace("</li>", ".</li>")
    html2 = html1.replace("</h1>", ".</h1>")
    html3 = html2.replace("</h2>", ".</h2>")
    html4 = html3.replace("</h3>", ".</h3>")
    html5 = html4.replace("</h4>", ".</h4>")
    html6 = html5.replace("</h5>", ".</h5>")
    html7 = html6.replace("</h6>", ".</h6>")

    #get adjusted readability total_score
    revised_soup = BeautifulSoup(html7, features="lxml").find('main')
    revised_text = revised_soup.get_text()

    from readability import Readability
    r_f = Readability(revised_text)
    final_fk = r_f.flesch_kincaid()


    #tokenize the text for processing
    import nltk
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer('\w+')
    tokens = tokenizer.tokenize(revised_text)
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
    most_common = fdist1.most_common(20)

    #get all headings and calculate how many words on average between headings
    headings = original_soup.findAll(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    hratio = len(words)/(len(headings))

    #get all paragraphs and all bulleted list, and calculate how many words per paragraph on average
    paragraphs = original_soup.findAll(['p', 'ul'])
    pratio = (len(words)/len(paragraphs))

    #calculate points for readability
    if final_fk.score <= 6:
        fkpoints = 60
    elif final_fk.score >= 18:
        fkpoints = 0
    else :
        fkpoints = (60-((final_fk.score-6)*5))

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
    total_score = format(total_score, '.2f')
    fkpoints = format(fkpoints, '.2f')
    final_fk_score = format(final_fk.score, '.2f')
    hpoints = format(hpoints, '.2f')
    hratio = format(hratio, '.2f')
    ppoints = format(ppoints, '.2f')
    pratio = format(pratio, '.2f')
    total_words = len(words)


    return render_template("read_score.html", total_score = total_score, fkpoints = fkpoints, final_fk_score = final_fk_score, hpoints = hpoints, hratio = hratio, ppoints = ppoints, pratio = pratio, total_words = total_words, most_common = most_common)

if __name__ == '__main__':
    app.run()
