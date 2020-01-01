import utils
import sematch
import memoization


class AutoMap(object):
    def __init__(self, text=None, delete_list=None):
        """
        Note:
        For text we assume the entire unit of text is given by text
        """
        self.text = text.strip().strip('\n').lower().split()
        self.delete_list = set(delete_list)
        if not self.delete_list:
            self.delete_list = set(utils.stopwords)

        #  note we will need to stem
        self.text_concepts =\
            [word for word in self.text
                if word not in self.delete_list]

    def get(self, higher_concepts=False, text_concepts=False):
        response = {}

        if text_concepts:
            response['text_concepts'] = self.text_concepts

        return response
