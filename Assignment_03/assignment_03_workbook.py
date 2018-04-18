# Import Statements
import pandas as pd #matplotlib support failed
import numpy as np
# %matplotlib inline  #breaks
from datetime import datetime

# Data I/O
data = pd.read_json("Assignment_03/reviews.json") # Data import
# data.shape
# data.axes[1].tolist()
# data.head(4)
data['date'] = data['date'].apply(lambda x: datetime.fromordinal(x)) # Date conversion

# Basic Analysis # from nltk import ngrams
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
# Extract the simple dependent and independent variables from the dataframe
body_list = data['body'].tolist()
rating_list = data['stars'].tolist()
# Split into training data and test data
x_train, x_test, y_train, y_test = train_test_split(body_list, rating_list, test_size=0.2, random_state=1)
# Fit vectorizer to training data
vectorizer = CountVectorizer(lowercase=True, strip_accents='ascii', stop_words='english', min_df=0.01, max_df=0.9, binary=True)
#analyzer='word', ngram_range=(1,1), max_df=1.0 or 1, min_df=1.0 or 1, max_features=?int, binary=False, #KEEP THIS IN
vectorizer = vectorizer.fit(x_train)
# Transform training and test dataset using the vectorizer
x_train = vectorizer.transform(x_train) #just do .toarray() here?
x_test = vectorizer.transform(x_test)
total_word_counts = [sum(word_count) for word_count in zip(*x_train.toarray())]
word_frequencies = dict(zip(vectorizer.get_feature_names(), total_word_counts))
most_frequent_term = max(word_frequencies, key = word_frequencies.get)
print("The most frequent term is '" + most_frequent_term + "' and it occurs " + str(word_frequencies[most_frequent_term]) + " times in the training corpus.")
# import plotly.plotly as py #TODO: remove
# from plotly.graph_objs import * #TODO: remove
# import plotly.graph_objs as go
top_indexes = [i for i, x in enumerate(y_train) if x>=4]
bot_indexes = [i for i, x in enumerate(y_train) if x<4]
top_reviews = x_train.toarray()[top_indexes]
bot_reviews = x_train.toarray()[bot_indexes]
top_word_counts = [sum(word_count) for word_count in zip(*top_reviews)]
bot_word_counts = [sum(word_count) for word_count in zip(*bot_reviews)]
# top_word_frequencies = dict(zip(vectorizer.get_feature_names(), top_word_counts))
# bot_word_frequencies = dict(zip(vectorizer.get_feature_names(), bot_word_counts))
top_bot_word_counts = pd.DataFrame({"word": vectorizer.get_feature_names(), "top": top_word_counts, "bot": bot_word_counts})
top_bot_word_counts.sort_values('top', ascending=False)[:5]
top_bot_word_counts.sort_values('bot', ascending=False)[:5]
# import cufflinks as cf #TODO: remove
# cf.set_config_file(offline=True, world_readable=True, theme='ggplot') #revise this #TODO: remove
a = top_bot_word_counts.sort_values('top', ascending=False)[:5].set_index('word')
b = top_bot_word_counts.sort_values('bot', ascending=False)[:5].set_index('word')
import matplotlib.pyplot as plt

a.append(b).drop_duplicates().plot.bar()
# top_bot_word_counts.sort_values('top', ascending=False)[:5].iplot(kind='bar', filename='cufflinks/grouped-bar-chart')
# top_bar = go.Bar(
#     x = top_bot_word_counts.sort_values('top', ascending=False)[:5]
# )

# x_train.data.tolist()
vector = vectorizer.fit([temp])
vector.tr
a = vectorizer.transform([temp])
vector = vectorizer.fit_transform([temp])
vector.toarray()
vectorizer.get_feature_names()
type(vector)

# list(ngrams(body_list, n=1))

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
