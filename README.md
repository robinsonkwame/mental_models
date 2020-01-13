# mental_models
Extracts human mental models from text and facilitates mental model comparison and contrasting. An alternative implementation of "AutoMap," see: J Diesner, K M Carley, "AutoMap1.2 - Extract, analyze, represent, and compare mental models from texts" (2003) for more background details.

# Install
```
pip install mental_model
```

# Build
This library assumes that several models and datasets are available. You can run the command below to build them.

```
#  ... need a small language model 
python3 -m spacy download en_core_web_sm
# ... adds in WordNet tokenization for spaCy
python3 -m nltk.downloader wordnet
python3 -m nltk.downloader omw
```
