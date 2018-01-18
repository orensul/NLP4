
"""
This class implements the POS extractor
"""
import random
class PosExtractor:

    def __init__(self, tokens):
        """

        """
        self.tokens = tokens
        self.triplets = []
        self.tokens_merge_propn = []
        self.pair_of_proper_nouns = []

        self.merge_propn()
        self.find_pair_of_proper_nouns()
        self.print_output()
        self.print_random_of_30_triplets()

    def print_random_of_30_triplets(self):
        print("--------------------- Random 30 Triplets ---------------------")
        triples = list(self.triplets)
        random.shuffle(triples)
        count_triples = 0
        for t in triples:
            print((t[0], t[1], t[2]))
            if count_triples == 30:
                break
            count_triples += 1

    def merge_propn(self):
        """
        Find all proper nouns in the corpus by locating consecutive sequences of tokens with the POS PROPN.
        """
        concat_proper_nouns = ''
        for token in self.tokens:
            # if this token also with POS PROPN, concat the text of the token to previous
            if token.pos_ == 'PROPN':
                concat_proper_nouns += token.text + ' '
            else:
                # if we have concat, append to self.tokens_merge_propn a token with concat text of prev tokens
                # and reset concat_proper_nouns to empty str
                if not concat_proper_nouns == '':
                    self.tokens_merge_propn.append((concat_proper_nouns[:-1], 'PROPN'))
                    concat_proper_nouns = ''
                # append the token
                self.tokens_merge_propn.append((token.text, token.pos_))

    def check_pair_of_tokens(self, token1_index, token2_index):
        """
        :param token1_index: index of the first token in tokens_merge_propn list
        :param token2_index: index of the second token in tokens_merge_propn list
        :return: boolean - True if all tokens between are not PUNCT and at least one of them of POS VERB,
        otherwise, False.
        """
        has_verb = False
        for i in range(token1_index, token2_index):
            if self.tokens_merge_propn[i][1] == 'PUNCT':
                return False
            if self.tokens_merge_propn[i][1] == 'VERB':
                has_verb = True
        if has_verb:
            return True
        return False

    def find_pair_of_proper_nouns(self):
        propn_indexes = []
        pair_of_propn_indexes = []

        # populate propn_indexes list with all of the indexes of PROPN tokens
        for i in range(len(self.tokens_merge_propn)):
            if self.tokens_merge_propn[i][1] == 'PROPN':
                propn_indexes.append(i)

        # find all of the pairs of indexes
        for i in range(len(propn_indexes)):
            for j in range(i+1, len(propn_indexes)):
                pair_of_propn_indexes.append((propn_indexes[i], propn_indexes[j]))

        i = 0
        while i < len(pair_of_propn_indexes):
            first_propn_index = pair_of_propn_indexes[i][0]
            second_propn_index = pair_of_propn_indexes[i][1]
            # if proper nouns pass the check, append them to pair_of_proper_nouns list
            if self.check_pair_of_tokens(first_propn_index, second_propn_index):
                self.pair_of_proper_nouns.append((self.tokens_merge_propn[first_propn_index],
                                                               self.tokens_merge_propn[second_propn_index],
                                                               first_propn_index,
                                                               second_propn_index))
            i += 1


    def print_output(self):
        """
        Prints triplets of pair of PROPN (subject, object) with the relation between them
        """
        trip_number = 0
        for pair_of_noun in self.pair_of_proper_nouns:
            trip_number += 1
            first_token = pair_of_noun[0]
            second_token = pair_of_noun[1]
            first_in_pair_token_number = pair_of_noun[2]
            second_in_pair_token_number = pair_of_noun[3]
            relation = ''
            relation_list = self.get_relation_tokens(first_in_pair_token_number,
                                                                     second_in_pair_token_number)
            for rel in relation_list:
                relation += rel + ' '

            print((first_token[0], relation[:-1], second_token[0]))
            self.triplets.append((first_token[0], relation[:-1], second_token[0]))

        print("--------------------- Total number of triplets: " + str(trip_number) + ' ---------------------')

    def get_relation_tokens(self, subject_index, object_index):
        """
        :param subject_index: index of the first PROPN - the subject
        :param object_index: index of the second PROPN - the object
        :return: list of relation_tokens
        """
        tokens_of_this_relation = []
        for i in range(subject_index, object_index):
            # take into the relation only tokens with (VERB or ADP) POS.
            if self.tokens_merge_propn[i][1] in ['VERB', 'ADP']:
                tokens_of_this_relation.append(self.tokens_merge_propn[i][0])
        return tokens_of_this_relation