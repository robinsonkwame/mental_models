import utils
import sematch
import memoization


class AutoMap(object):
    def __init__(self, text=None, nlp=None, delete_list=None):
        nlp = nlp
        if not nlp:
            nlp = utils.nlp_en
        self.raw_text = text
        self.text = nlp(self.raw_text)
        self.delete_list = delete_list
        if not delete_list:
            self.delete_list = set(nlp.Defaults.stop_words)

        self.text_concepts =\
            [token for token in self.text if not
                (token.text.lower() in self.delete_list or
                 token.is_punct                         or
                 token.is_space)]

    def get(self,
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

        def get_higher_or_text_concept(token):
            ret = token.text
            if not token.is_stop:
                synset = token._.wordnet.synsets()[0]
                hypernyms = synset.hypernyms()
                if not hypernyms:
                    hypernyms = synset.root_hypernyms()
                if len(hypernyms) > 0:
                    ret = hypernyms[0].name()
            return ret

        response = {}
        text_concepts = None
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
            response['text_concepts'] = text_concepts

        if want_higher_concepts:
            response['higher_concepts'] = higher_concepts

        return response
