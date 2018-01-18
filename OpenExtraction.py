import wikipedia, spacy
import PosExtractor
import DepTreeExtractor


pages = ['Donald Trump', 'Brad Pitt', 'Angelina Jolie']

class OpenExtraction(object):

    def __init__(self):
        for page in pages:
            self.tokens = []
            self.nlp = spacy.load('en')
            self.page = wikipedia.page(page).content
            self.analyzed_page = self.nlp(self.page)

            self.init_tokens()
            print()
            print("----------------- POS EXTRACTOR, page = " + page + ' -----------------')
            self.pos_extractor = []
            self.pos_extractor = PosExtractor.PosExtractor(self.tokens)
            print()
            print("----------------- DEP Tree EXTRACTOR, page = " + page + ' -----------------')
            self.dep_tree_extractor = DepTreeExtractor.DepTreeExtractor(self.tokens)

    def init_tokens(self):
        """
        reads all of the tokens into self.tokens list
        """
        for token in self.analyzed_page:
            self.tokens.append(token)


def main():
    oe = OpenExtraction()
main()


