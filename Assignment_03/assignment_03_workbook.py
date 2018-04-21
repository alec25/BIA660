# Import Statements
import pandas as pd #matplotlib support failed
import numpy as np # %matplotlib inline  #breaks
from datetime import datetime

# Data I/O
data = pd.read_json("Assignment_03/reviews.json") # Data import
# data.shape # data.axes[1].tolist() # data.head(4)
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

top_indexes = [i for i, x in enumerate(y_train) if x>=4]
bot_indexes = [i for i, x in enumerate(y_train) if x<4]
top_reviews = x_train.toarray()[top_indexes]
bot_reviews = x_train.toarray()[bot_indexes]
top_word_counts = [sum(word_count) for word_count in zip(*top_reviews)]
bot_word_counts = [sum(word_count) for word_count in zip(*bot_reviews)]
top_bot_word_counts = pd.DataFrame({"word": vectorizer.get_feature_names(), "positive_review": top_word_counts, "negative_review": bot_word_counts})
top_bot_most = top_bot_word_counts.sort_values('positive_review')[-5:][::-1].append(top_bot_word_counts.sort_values('negative_review')[-5:][::-1]).set_index('word')
# import matplotlib.pyplot as plt # KEEP
# top_bot_most.drop_duplicates().plot.bar() # KEEP
# Maybe try knn also for this?

# Now the model
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
binary_train = [1 if x >=4 else 0 for x in y_train]
binary_test = [1 if x >=4 else 0 for x in y_test]
lr1 = LogisticRegression(penalty='l1')
lr2 = LogisticRegression(penalty='l2')
lr1.fit(x_train, binary_train); lr2.fit(x_train, binary_train)
words_used1 = len(lr1.coef_[0]) - lr1.coef_[0].tolist().count(0)
words_used2 = len(lr2.coef_[0]) - lr2.coef_[0].tolist().count(0)
print(str(words_used1)+' words used in the L1 regression w/ accuracy: '+
      str(round(100 * lr1.score(x_test, binary_test), 2))+'%, '+
      str(words_used2)+' words used in the L2 regression w/ accuracy: '+
      str(round(100 * lr2.score(x_test, binary_test), 2)))
# confusion_matrix(binary_test, lr1.predict(x_test))
# confusion_matrix(binary_test, lr2.predict(x_test))

### More advanced training
# onehot_style = pd.DataFrame(preprocessing.label_binarize(data['style'], classes = data['style'].unique())).loc[:,1:2] #Keep
data_backup = data
#
data = data_backup
from sklearn import preprocessing
# Styles to Int
le = preprocessing.LabelEncoder()
le.fit(data['style'])
data['style'] = le.transform(data['style'])
# Author
data['author'] = [1 if x=='Amazon Customer' else 0 for x in data['author']] #maybe 0 for 'amazon customer' else num names?
# Text = Title + " " + Body
data['text'] = pd.Series(data['title'] + " " + data['body'])
data = data.drop(columns=['title', 'body'])
# Normalize Dates
data['date'] = data['date'].apply(datetime.toordinal)
data['date'] = data['date'] - min(data['date'])
data['date'] = data['date'] / max(data['date'])
#
from autocorrect import spell
import re
raw_texts = data['text'].tolist()
# new_backup = data
def process_text(review_text):
    digits = sum(1 for let in review_text if let.isdigit())
    no_contractions = re.sub("[']+", "", review_text)
    clean_text = re.sub("[!\"#$%&()*+,\-./:;<=>?@[\]^_`\\{|}~]|(\n)|[0-9]+", ' ', no_contractions)
    new_text = list(map(spell, clean_text.split()))
    differences = sum([1 for a, b in zip(new_text, clean_text.split()) if a != b])
    return ' '.join(new_text), digits, differences
# list(map(process_text, raw_texts))
texts, numbers, typos = zip(*list(map(process_text, raw_texts)))
# data['text'] = pd.Series(texts)
data['numbers'] = pd.Series(numbers)
data['typos'] = pd.Series(typos)
stars = data['stars']
data = data.drop(columns=['text', 'stars'])
# Now for TfIdf #texts
from sklearn.feature_extraction.text import TfidfVectorizer
word_list = list(map(str.split, texts))
# word_list = [word_tokenize(x) for x in texts] #seems slightly slower
from nltk.stem.snowball import EnglishStemmer # Also turns the text lowercase
#nltk..wordnet.WordNetLemmatizer() #maybe?!?!?!
stemmer = EnglishStemmer(ignore_stopwords=True) #ignore_stopwords=False
stemmed_word_list = list(map(lambda x: [stemmer.stem(w) for w in x], word_list))
stemmed_list = list(map(lambda x: ' '.join(x), stemmed_word_list))
tfidf = TfidfVectorizer(lowercase=True, stop_words='english', norm=None, use_idf=False, max_df=0.99, min_df=2)

#now the thing
texts1, texts2, data1, data2, stars1, stars2 = train_test_split(stemmed_list, data, stars, test_size=0.15, random_state=1)
# texts1, data1, stars1, texts2, data2, stars2 = train_test_split(texts, data, stars, test_size=0.15, random_state=1)
tfidf.fit(texts1)
tf1 = tfidf.transform(texts1)
tf2 = tfidf.transform(texts2)
# x_train, x_test, y_train, y_test = train_test_split(body_list, rating_list, test_size=0.2, random_state=1)
# ok cool now we have all our training data
tf1 = pd.DataFrame(tf1.toarray(), index=data1.axes[0])
tf2 = pd.DataFrame(tf2.toarray(), index=data2.axes[0])
data_in1 = pd.concat([data1, tf1], axis=1)
data_in2 = pd.concat([data2, tf2], axis=1)
#now lets try simple regression
from sklearn.linear_model import Lasso
lasso = Lasso(alpha=0.1)
lasso.fit(data_in1, stars1)
# features_used1 = len(lasso.coef_) - lasso.coef_.tolist().count(0) #6
signifigant_features = data_in1.dtypes.index[[i for i, j in enumerate(lasso.coef_) if j != 0]]
sig_words = [tfidf.get_feature_names()[i] for i in signifigant_features[2:]]
print(', '.join(signifigant_features[:2])+' | '+', '.join(sig_words))
# Since Lasso only gives us 6 indicator variables (with an Lambda or "alpha" of 0.1, with the default value of 1
#we get 0 indicator variables. We can see that the model selected 4 of the word vectors and also the number of
#people that found the review helpful, and the number of numbers in the reviews text or title. The accuracy of the
#Lasso regression was embarrasingly low and so was not included here.
from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier()
mlp.fit(data1, stars1)
def per(x): return(str(round(100*x,2))+'%')
print(per(mlp.score(data1, stars1))+' training accuracy, '+per(mlp.score(data2, stars2))+' testing accuracy')
#now we redo stuff and try SMOTE over-sampling
from imblearn.over_sampling import SMOTE
# mlp.score(data1, stars1)
# mlp.score(data2, stars2)

# mlp.predict(data1)



# lr1.fit(data_in1, stars1); lr2.fit(x_train, binary_train)
words_used1 = len(lr1.coef_[0]) - lr1.coef_[0].tolist().count(0)
words_used2 = len(lr2.coef_[0]) - lr2.coef_[0].tolist().count(0)

print(str(words_used1)+' words used in the L1 regression w/ accuracy: '+
      str(round(100 * lr1.score(x_test, binary_test), 2))+'%, '+
      str(words_used2)+' words used in the L2 regression w/ accuracy: '+
      str(round(100 * lr2.score(x_test, binary_test), 2)))
lr1.score(x_train, binary_train)
lr2.score(x_train, binary_train)
# stemmed = [stemmer.stem(word) for word in tokens]


data.head(3)









# ('One Star Already no longer working after minimal use', 0, 0),
# ('Five Stars Great little flashlights', 0, 0)]

review_text = data['text'].tolist()[0]
digits = sum(1 for let in review_text if let.isdigit())
no_contractions = re.sub("[']+", "", review_text)
clean_text = re.sub("[!\"#$%&()*+,\-./:;<=>?@[\]^_`\\{|}~]|(\n)|[0-9]+", ' ', no_contractions)
new_text = list(map(spell, clean_text.split()))
differences = sum([1 for a, b in zip(new_text, clean_text.split()) if a != b])
#
data.head(3)
# round(100*sum([1 if 'stars' in x.lower() else 0 for x in data['title']])/len(data['title']),2)
for a, b in zip(new_text, clean_text.split()): print(a+ " - " + b)
sum(1 for let in review_text if let.isdigit())








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
       "[!\"#$%&'()*+,\-./:;<=>?@[\]^_`\\{|}~]"
re.sub("[!\"#$%&'()*+,\-./:;<=>?@[\]^_`\\{|}~]|(\n)+", ' ', temp) #removed " ' " #.sub('[0-9]+', "#", temp)
#               '
data['num_chars'] = data['title'].apply(len) + data['body'].apply(len)
a.head(3)
# Data Manipulation/Tokenization
body_list = data['body']







# import string #is this even still necessary?
temp = texts[0:3] #TODO: remove, this is just for testing
from nltk import sent_tokenize, word_tokenize, wordpunct_tokenize # Tokenizers# import nltk
# sent_temp = sent_tokenize(temp)
word_temp = word_tokenize(sent_temp[0])
# list(map(str.split, temp)) == [word_tokenize(x) for x in temp]
[word_tokenize(x) for x in temp] #...in [sent_temp[0]] ]
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
