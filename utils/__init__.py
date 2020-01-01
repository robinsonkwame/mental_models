import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator

stopwords = None

nlp_en = spacy.load('en_core_web_sm')
nlp_en.add_pipe(WordnetAnnotator(nlp_en.lang), after='tagger')
