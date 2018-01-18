import random
class DepTreeExtractor:

    def __init__(self, tokens):
        self.tokens = tokens
        self.triplets = []
        self.trip_number = 0
        self.corresponding_proper_nouns = []

        self.heads_proper_nouns = []
        # Find all tokens that serve as heads of proper nouns in the corpus
        self.find_head_proper_nouns()
        # print("heads proper nouns")
        # self.print_heads_proper_nouns()
        self.find_corresponding_proper_noun()
        self.dep_tree_extractor()
        self.print_random_of_30_triplets()

    def find_head_proper_nouns(self):
        for token in self.tokens:
            if token.pos_ == 'PROPN' and not token.dep_ == 'compound':
                self.heads_proper_nouns.append(token)

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

    def find_corresponding_proper_noun(self):
        for proper_noun in self.heads_proper_nouns:
            set_of_children_with_dep_compound = set()
            child = [child if child.dep_ == 'compound' else None for child in proper_noun.children]
            for c in child:
                if not c is None:
                    set_of_children_with_dep_compound.add(c)
            self.corresponding_proper_nouns.append((proper_noun, set_of_children_with_dep_compound))

    def print_heads_proper_nouns(self):
        heads_count = 0
        for head in self.heads_proper_nouns:
            print("head proper noun number: " + str(heads_count))
            print("head text: " + head.text)
            print("head pos: " + head.pos_)
            print("head dep: " + head.dep_)
            print("head children: ")
            print([child for child in head.children])
            heads_count += 1

    def print_corresponding_proper_nouns(self):
        print("head with his children: ")
        for tuple in self.corresponding_proper_nouns:
            print("head: ")
            print(tuple[0])
            print("children: ")
            print(tuple[1])

    def print_output(self, h1, h2):
            if self.condition_one(h1, h2):
                h = h1.head
                self.trip_number += 1
                print((h1, h, h2))
                self.triplets.append((h1, h, h2))
            elif self.condition_two(h1, h2):
                h = h1.head
                h_tag = h2.head
                self.trip_number += 1
                print((h1, h.text + ' ' + h_tag.text, h2))
                self.triplets.append((h1, h.text + ' ' + h_tag.text, h2))

    def dep_tree_extractor(self):
        for h1 in range(len(self.corresponding_proper_nouns)):
            for h2 in range(h1 + 1, len(self.corresponding_proper_nouns)):
                first_head_proper_noun = self.corresponding_proper_nouns[h1][0]
                second_head_proper_noun = self.corresponding_proper_nouns[h2][0]
                self.print_output(first_head_proper_noun, second_head_proper_noun)
                self.print_output(second_head_proper_noun, first_head_proper_noun)
        print("---------------- Total number of triplets " + str(self.trip_number) + " ----------------")

    def condition_one(self, h1, h2):
        """
        :param h1: token h1
        :param h2: token h2
        :return: boolean - True if both h1, h2 have the same head h, the edge (h,h1) is labeled nsubj and the edge
        (h,h2) is labeled dobj. Otherwise, False
        """
        if h1.head == h2.head:
            if h1.dep_ == 'nsubj' and h2.dep_ == 'dobj':
                return True
        return False

    def condition_two(self, h1, h2):
        """
        :param h1: token h1
        :param h2: token h2
        :return: boolean - True if h1 parent in the dep tree is the same as h2 grandparent,
        the edge (h,h1) is labeled nsubj, the edge (h,h') (denote h' - h2 parent) is labeled prep,
        the edge (h',h2) is labeled pobj.
        """
        h = h1.head
        h_tag = h2.head
        h2_grandparent = h_tag.head
        if h == h2_grandparent:
            if h1.dep_ == 'nsubj' and h_tag.dep_ == 'prep' and h2.dep_ == 'pobj':
                return True
        return False