from mental_models import utils
from itertools import combinations
from collections import defaultdict


class AutoMap(object):
    def __init__(self, text=None, nlp=None, delete_list=None):
        nlp = nlp
        if not nlp:
            nlp = utils.nlp_en
        self.raw_text = text.strip()\
                            .replace('\n', '')\
                            .replace('.', '')\
                            .replace(',', '')\
                            .replace('(', '')\
                            .replace(')', '')
        self.text = nlp(self.raw_text)
        self.delete_list = delete_list
        if not delete_list:
            # self.delete_list = set(None) ?
            self.delete_list = set(nlp.Defaults.stop_words)

        self.text_concepts =\
            [token for token in self.text if not
                (token.text.lower() in self.delete_list or
                 token.is_punct                         or
                 token.is_space)]
        self.text_concepts_length = len(self.text_concepts)

    def get_statements(self):
        #  kinda wordy, lets take out self
        get_higher_or_text_concept = self.get_higher_or_text_concept

        def replace_with_concepts(concepts):
            for window_size in concepts:
                for index in range(len(concepts[window_size])):
                    # here we update the text to a concept 
                    concepts[window_size][index] =\
                        (get_higher_or_text_concept(
                            concepts[window_size][index][0]),
                         get_higher_or_text_concept(
                             concepts[window_size][index][1]))
            return concepts

        response = {}
        direct = defaultdict(list)
        rhetorical = defaultdict(list)
        offset_index = 1
        word_index = 0

        words_with_offsets =\
            [word_offset for word_offset in
                zip(
                    self.text_concepts,
                    range(self.text_concepts_length)
                )]

        all_combinations_with_offsets =\
            [(pair[0][word_index],
              pair[1][word_index],
              pair[1][offset_index] - pair[0][offset_index])
                for pair in combinations(words_with_offsets, 2)]

        for concept_a, concept_b, offset in all_combinations_with_offsets:
            direct[offset].append((concept_a, concept_b))

        #  now we construct the rhetorical version by throwing out any pair
        # that includes a stopword (.is_stop). Since we don't use the delete_list
        # in practice I just check .is_stop
        for window_size in direct.keys():
            for item in direct[window_size]:
                rhetorical[window_size] =\
                    [item for item in direct[window_size]
                        if not (item[0].is_stop or item[1].is_stop)]

        #  now we need to replace the text with its concept across both versions
        # note: I could optimize this by doing this directly in the step above
        response['direct'] = replace_with_concepts(direct)
        response['rhetorical'] = replace_with_concepts(rhetorical)

        return response

    def get_higher_or_text_concept(self, token):
        ret = token.text
        if not token.is_stop:
            #synset = token._.wordnet.synsets()[0]
            synset_lookup = token._.wordnet.synsets()
            if synset_lookup:
                synset = synset_lookup[0]
                hypernyms = synset.hypernyms()
                if not hypernyms:
                    hypernyms = synset.root_hypernyms()
                if hypernyms:
                    ret = hypernyms[0].name()
        return ret

    def get_concepts(self,
                     want_higher_concepts=False,
                     want_text_concepts=False,
                     include_text_concepts=False):
        def have_a_higher_concept_or_text_concept(is_stop, include_text_concepts):
            ret = False
            if not is_stop:
                ret = True
            if is_stop and include_text_concepts:
                ret = True
            return ret
        #  kinda wordy, lets take out self
        get_higher_or_text_concept = self.get_higher_or_text_concept

        response = {}
        higher_concepts = None

        if want_higher_concepts:
            #  here I include filter logic that surfaces any text concepts
            # that sare spaCy stop words; this way some words come to the surface
            # beacuse otherwise WordNet has a higher concept for everything
            print("in higher concepts")
            higher_concepts = [
                get_higher_or_text_concept(token)
                    for token in self.text_concepts if
                        have_a_higher_concept_or_text_concept(token.is_stop,
                                                              include_text_concepts)]

        #  package up data into the response object ...
        if want_text_concepts:
            response['text_concepts'] = self.text_concepts

        if want_higher_concepts:
            response['higher_concepts'] = higher_concepts

        return response
