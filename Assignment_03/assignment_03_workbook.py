# Import Statements
import pandas as pd
from datetime import datetime

# Data I/O
data = pd.read_json("Assignment_03/reviews.json") # Data import
# data.shape
# data.axes[1].tolist()
# data.head(4)
data['date'] = data['date'].apply(lambda x: datetime.fromordinal(x)) # Date conversion

# Basic Analysis
import string
# from nltk import ngrams
from sklearn.feature_extraction.text import CountVectorizer
body_list = data['body'].tolist()
vectorizer = CountVectorizer(loweracase=True, strip_accents='ascii', stop_words='english')
#analyzer='word', ngram_range=(1,1), max_df=1.0 or 1, min_df=1.0 or 1, max_features=?int, binary=False,
list(ngrams(body_list, n=1))

# New Features
import string
import re
def remove_punct(x):
def count_punct(x):
    return
temp
#
# import string
# punctuation_translator = str.maketrans('0123456789', 'XXXXXXXXXX', string.punctuation+"\n") #?
# temp.translate(punctuation_translator)

"[!\"#$%&'()*+,\-./:;<=>?@[\]^_`\\{|}~]"
re.sub("[!\"#$%&()*+,\-./:;<=>?@[\]^_`\\{|}~]|(\n)+", ' ', temp) #removed " ' " #.sub('[0-9]+', "#", temp)

data['num_chars'] = data['title'].apply(len) + data['body'].apply(len)
a.head(3)
# Data Manipulation/Tokenization
body_list = data['body']







# import string #is this even still necessary?
temp = data['body'][0] #TODO: remove, this is just for testing
from nltk import sent_tokenize, word_tokenize, wordpunct_tokenize # Tokenizers# import nltk
sent_temp = sent_tokenize(temp)
word_temp = word_tokenize(sent_temp[0])
[word_tokenize(x) for x in sent_temp] #...in [sent_temp[0]] ]
# nltk.wordpunct_tokenize(sent_temp[0]) #not sure about the difference, "It 's" -> "It ' s"; "I 'll" -> "I ' ll"?

#To compare them:
# " ".join(word_tokenize(temp))
# " ".join(wordpunct_tokenize(temp))

tokens = word_tokenize(temp)
# tokens = wordpunct_tokenize(temp)


# from nltk.stem import SnowballStemmer
# stemmer = SnowballStemmer("english", ignore_stopwords=False)
from nltk.stem.snowball import EnglishStemmer # Also turns the text lowercase
stemmer = EnglishStemmer(ignore_stopwords=False)
stemmer2 = EnglishStemmer(ignore_stopwords=True)
stemmed = [stemmer.stem(word) for word in tokens]
stemmed2 = [stemmer2.stem(word) for word in tokens]
" ".join(tokens)
" ".join(stemmed) #to compare them:
" ".join(stemmed2)

# string.punctuation #
punctuation = '"#%&\'()*+,-./:;<=>[\\]^_`{|}~' #include: $,?,!,@
punct_table = dict((ord(char), None) for char in punctuation)



[sent.translate(punct_table) for sent in texts] #i'll -> ill, stem first? #import string #?


from sklearn.feature_extraction.text import CountVectorizer




#from nltk import ngrams #or #from sklearn.feature_extraction.text import CountVectorizer
