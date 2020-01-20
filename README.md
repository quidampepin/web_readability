# Web readability score

This is an attempt at tweaking the basic Flesch-Kincaid readability score to reflect how we write for the Web. It was developed with pages on Canada.ca in mind.


## Basic Flesch-Kincaid score

Basic Flesch-Kincaid uses 2 variables to get a score:
- average sentence length
- average number of syllables per word

One issue on the web is that it doesn't handle headings and bullet lists very well. If there isn't a period at the end of a heading or a bullet list, it considers it to be still the same sentence.

Concretely, it means that a page with a lot of bullet points gets a bad Flesch-Kincaid score, even if we know it's often a good thing to use bullet points.

One other issue is that it's ususally a good idea to keep paragraphs short and use headings to "chunk up" the text. I thought it would be nice to take these variables into account.

## Adjusted web readability score
With my limited Python knowledge, I built a script that:
- scrapes the HTML of a URL
- adds a period at the end of each heading and each bullet point (so each of these is considered as a “sentence” for the purpose of readability score)
- only keeps what’s in the “main” tag
- attributes “points” (on a max of 100) based on the following metrics:
  - **Flesch-Kincaid score:** grade level at 6 or under gives the full 60 points, a grade level 18 and over gives 0 points, and anything in between is prorated
  - **Number of words between headings:** 40 words or less per heading gives 20 points, 200 words or more per heading gives 0 point, and anything in between is prorated
  - **Number of words per paragraph:** 30 words or less per paragraph gives 20 points, 80 words or more per paragraph gives 0 point, and anything in between is prorated

It also give a list of the 15 most frequent words (excluding stop words) - it could be useful for SEO purposes.

This is quite arbitrary, obviously, and it may not work for every page, but results are interesting.

## Sample of script output
When launching a script (in Python 3), it asks for a URL, and spits out a report.

For example, https://www.canada.ca/en/services/benefits/education/student-aid/grants-loans/repay.html gives an initial readability score of grade 11.96.  
The adjusted Flesch-Kincaid score is 7.91 (because of all the bullet points and headings).  
Converted into points and factoring in the words between headings and number of words per paragraph, it gives a score of 82.85/100.

Here's the output:

Initial readability score: 11.96  
Total points: 82.85 /100  
Basic readabilty points: 50.45 /60 (Flesch-Kincaid readability score of: 7.91)  
Heading points:  12.41 /20 (words per heading: 100.75)  
Paragraph points:  20.00 /20 (words per paragraph: 23.71)  
Number of words:  806  
Most used words  
('rate', 20)  
('interest', 19)  
('repayment', 17)  
('time', 15)  
('payments', 14)  
('period', 11)  
('loan', 9)  
('make', 9)  
('6', 9)  
('month', 9)  
('student', 8)  
('one', 7)  
('payment', 7)  
('school', 7)  
('non', 7)  
