import nltk

stopwords = None

try:
    stopwords = nltk.corpus.stopwords.words('english')
except LookupError:
    stopwords = nltk.download('stopwords')
