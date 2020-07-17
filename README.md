(Le fraçais suit l'anglais)
# Web readability score

This is an experimental way of calculating a readability score specifically for the web.
It was developed with pages on Canada.ca in mind.


## Basic Flesch-Kincaid score

Basic Flesch-Kincaid uses 2 variables to get a score:
- average sentence length
- average number of syllables per word

Basic readability score doesn't handle headings and bullet lists very well. If there isn't a period at the end of a heading or a bullet item, it considers it to be still the same sentence.

Concretely, it means that a page with a lot of bullet points gets a bad Flesch-Kincaid score, even if we know it's often a good thing to use bullet points.

We also know it's usually a good idea to keep paragraphs short and use headings to separate the text in chunks.

## Adjusted web readability score
This script:
- scrapes the HTML of a URL
- adds a period at the end of each heading and each bullet point (so each of these is considered as a “sentence” for the purpose of the readability score)
- only keeps what’s in the “main” tag of the HTML page
- attributes “points” (on a max of 100) based on the following metrics:
  - **Flesch-Kincaid score:** grade level at 6 or under gives the full 60 points, a grade level 18 and over gives 0 points, and anything in between is prorated
  - **Number of words between headings:** 40 words or less per heading gives 20 points, 200 words or more per heading gives 0 point, and anything in between is prorated
  - **Number of words per paragraph:** 30 words or less per paragraph gives 20 points, 80 words or more per paragraph gives 0 point, and anything in between is prorated

The script also gives a list of the 15 most frequent words (excluding stop words). This could be useful for SEO purposes.


## How to use the script
- Install Python 3, and all needed libraries:
  - Flask
  - bs4 (BeautifulSoup)
  - readability
  - requests
  - nltk
- Run read_score.py in a Python intepreter - it launched a local server
- Go to http://localhost:5000/read_score, and pass 2 parameters:
  - the language of the page
  - the URL of the page

For example, if you go http://localhost:5000/read_score?lang=en&url=https://www.canada.ca/en/services/benefits.html, you'll get the readability score and most frequent words for the Benefits theme page.


*******

# Score de lisibilité Web

Il s'agit d'une méthode expérimentale de calcul d'un score de lisibilité spécifique au Web.

Il a été développé pour les pages de Canada.ca.


## Note de base de Flesch-Kincaid

Le score Flesch-Kincaid de base utilise 2 variables pour obtenir un score :
- la longueur moyenne des phrases
- le nombre moyen de syllabes par mot

La note de lisibilité de base ne gère pas très bien les en-têtes et les listes à puces sur le Web. S'il n'y a pas de point à la fin d'une en-tête ou d'une puce, il considère qu'il s'agit toujours de la même phrase.

Concrètement, cela signifie qu'une page avec beaucoup de puces obtient un mauvais score Flesch-Kincaid, même si nous savons que c'est souvent une bonne chose d'utiliser des puces.

Nous savons aussi que c'est souvent une bonne idée de garder les paragraphes courts et d'utiliser des en-têtes pour séparer le texte en sections.

## Score de lisibilité web ajusté
Le script:
- va chercher le code HTML d'une URL
- ajoute un point à la fin de chaque titre et de chaque puce (chacun d'eux est donc considéré comme une "phrase" aux fins de la note de lisibilité)
- ne conserve que ce qui se trouve dans la balise "main" de la page HTML
- attribue des "points" (sur un maximum de 100) en fonction des paramètres suivants :
  - **Score Flesch-Kincaid :** un niveau de 6 ou moins donne 60 points, un niveau de 18 et plus donne 0 point, et un score entre les deux est calculé au prorata
  - **Nombre de mots entre les en-têtes :** 40 mots ou moins entre les en-têtes donne 20 points, 200 mots ou plus par titre donne 0 point, et un nombre entre les deux est calculé au prorata
  - **Nombre de mots par paragraphe :** 30 mots ou moins par paragraphe donne 20 points, 80 mots ou plus par paragraphe donne 0 point, et un nombre entre les deux est calculé au prorata

Le script donne également une liste des 15 mots les plus fréquents (en excluant des mots très fréquents). Cela pourrait être utile pour le les techniques d'optimisation de recherche (SEO).


## Comment utiliser le script
- Installez Python 3, et toutes les bibliothèques nécessaires :
  - Flask
  - bs4 (BeautifulSoup)
  - readability
  - requests
  - nltk
- Exécutez read_score.py dans un interpréteur Python - cela lance un serveur local
- Allez sur http://localhost:5000/read_score, et incluez 2 paramètres :
  - la langue de la page
  - l'URL de la page

Par exemple, si vous allez sur http://localhost:5000/read_score?lang=fr&url=https://www.canada.ca/fr/services/prestations.html, vous obtiendrez le score de lisibilité et les mots les plus fréquents pour la page thématique des avantages.
