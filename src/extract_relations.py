import codecs

import spacy.matcher
import spacy.tokenizer


KEYWORDS = set([
    'mère', 'père', 'fils', 'fille', 'épous',
    'femme', 'client', 'parent', 'mari', 'veuve'
])

"""
Forms:

    1. "fils" + [word] + (de/du/d') + (PROPN) => son of (PROPN = father)
    2. (PROPN1) comma "fils" (de/du/d') (PROPN2) => PROPN1 (son) of PROPN2 (father) 
    3. "fils" (de/du/d') (PROPN1) comma (PROPN2) => PROPN2 (son) of PROPN1
    
Rules:
    on "fils":
        if previous word is "comma", move to form 2 parser
        if next word is PROPN and word after all PROPNs is comma, then 
"""

NAME = {'POS': {'IN': ['PROPN',]}, 'OP': '+'}
# NAME = {'POS': 'PROPN', 'OP': '+'}
DE = {'REGEX': "d[eu']"}

MATCHERS = {
    'FATHER_SON_1': [
        {'POS': 'PROPN', 'OP': '!',},
        {'LOWER': ',', 'OP' : '!'},
        {'LOWER': 'fils'},
        {},
        DE,
        {'POS': 'PROPN'},
        {'LOWER': '-', 'OP': '?'},
        NAME,
    ],
    'FATHER_SON_2': [
        NAME,
        {'LOWER': ','},
        {'LOWER': 'fils'},
        DE,
        NAME,
    ],
    'FATHER_SON_3': [
        {'POS': 'PROPN', 'OP': '!',},
        {'LOWER': ',', 'OP' : '!'},
        {'LOWER': 'fils'},
        DE,
        NAME,
        {'LOWER': ','},
        NAME,
    ],

    'FATHER_DAUGHTER_2': [
        NAME,
        {'LOWER': ','},
        {'LOWER': 'fille'},
        DE,
        NAME,
    ],

    'FATHER_DAUGHTER_4': [
        {'POS': 'PROPN', 'OP': '!',},
        {'LOWER': 'fille'},
        DE,
        NAME,
    ],

    'GENDRE_1': [ NAME, {'LOWER': ','}, {'LOWER': 'gendre',}, DE, NAME, ],
    'GENDRE_2': [ NAME, {'LOWER': ','}, {'LOWER': 'gendre',}, DE, {'POS' : 'N'}, ],

}

class FatherSonRelationship:

    def __init__(self, father='unnamed father', son='unnamed son'):
        self.father = father
        self.son = son


class FatherDaughterRelationship:

    def __init__(self, father, daughter):
        self.father = father
        self.daughter = daughter


class GendreRelationship:

    def __init__(self, father, husband):
        self.father = father
        self.husband = husband


class RelationshipHandler:

    def __init__(self):
        self.relationships = []

    def handle_fs_1(self, matcher, doc, i, matches):
        match_id, start, end = matches[i]
        inner_doc = doc[start:end]
        print('FS 1: ')
        print(inner_doc)
        self.relationships.append(FatherSonRelationship(father=inner_doc.ents[0]))

    def handle_fs_2(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        print('FS 2: ')
        print(inner_doc)
        if len(inner_doc.ents) == 1:
            son = inner_doc[0]
            father = inner_doc.ents[0]
        else:
            son = inner_doc.ents[0]
            father = inner_doc.ents[1]

        self.relationships.append(FatherSonRelationship(
            son=son,
            father=father
        ))

    def handle_fs_3(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        print(inner_doc)
        self.relationships.append(FatherSonRelationship(
            father=inner_doc.ents[0]
        ))

    def handle_fd_2(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        print(inner_doc)
        self.relationships.append(FatherDaughterRelationship(
            daughter=inner_doc.ents[0],
            father=inner_doc.ents[1]
        ))

    def handle_fd_4(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        print(inner_doc)
        father = None
        if inner_doc.ents:
            father = inner_doc.ents[0]
        else:
            father = inner_doc.conjuncts[0]
        self.relationships.append(FatherDaughterRelationship(
            father=father,
            daughter='unnamed daughter'
        ))

    def handle_gendre_1(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        self.relationships.append(GendreRelationship(
            father=inner_doc.ents[0],
            husband=inner_doc.ents[1],
        ))


print('Loading model ...')
nlp = spacy.load('fr')
print('Model loaded')

matcher = spacy.matcher.Matcher(nlp.vocab)
match_merger = spacy.matcher.Matcher(nlp.vocab)

print('Matchers initialized')

def quote_merger(doc):
    matched_spans = []
    matches = match_merger(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        matched_spans.append(span)
        # print(span)
    for span in matched_spans:
        span.merge()
    return doc


def matcher_for_vocab(vocab):
    match_merger = spacy.matcher.Matcher(nlp.vocab)

    match_merger.add('HYPHENATED_NAMES', None, [
        # {'TEXT': {'REGEX': r'[A-Z]\w+-[\w-]+'}}
        # {'TEXT': {'REGEX': r'\w+-\w+'}}
        {'TEXT': {'REGEX': r"[A-Z][\w'’]+"}},
        {'TEXT': {'REGEX': r'-'}},
        {'TEXT': {'REGEX': r"[A-Z][\w'’]+"}},
        {'TEXT': {'REGEX': r"^([A-Z])|([A-Z][\w’'-]+)|(-)|(’)$"}, 'OP': '*'},
        # {'TEXT': {'REGEX': r'\w+'}},
    ])

def main():
    in_file = codecs.open('Mercier_1600-1837.txt').read()
    relationship_set = RelationshipHandler()
    match_merger.add('HYPHENATED_NAMES', None, [
        # {'TEXT': {'REGEX': r'[A-Z]\w+-[\w-]+'}}
        # {'TEXT': {'REGEX': r'\w+-\w+'}}
        {'TEXT': {'REGEX': r"[A-Z][\w'’]+"}},
        {'TEXT': {'REGEX': r'-'}},
        {'TEXT': {'REGEX': r"[A-Z][\w'’]+"}},
        {'TEXT': {'REGEX': r"^([A-Z])|([A-Z][\w’'-]+)|(-)|(’)$"}, 'OP': '*'},
        # {'TEXT': {'REGEX': r'\w+'}},
    ])
    matcher.add('FATHER_SON_1', relationship_set.handle_fs_1, MATCHERS['FATHER_SON_1'])
    matcher.add('FATHER_SON_2', relationship_set.handle_fs_2, MATCHERS['FATHER_SON_2'])
    matcher.add('FATHER_SON_3', relationship_set.handle_fs_3, MATCHERS['FATHER_SON_3'])

    matcher.add('FATHER_DAUGHTER_4', relationship_set.handle_fd_4, MATCHERS['FATHER_DAUGHTER_4'])

    matcher.add('GENDRE_1', relationship_set.handle_gendre_1, MATCHERS['GENDRE_1'])
    # matcher.add('GENDRE_2', relationship_set.handle_gendre_2, MATCHERS['GENDRE_2'])
    # nlp.add_pipe(quote_merger, first=True)
    parsed_doc = nlp(in_file)
    # result = match_merger(parsed_doc)
    # print('Exiting')
    # return
    matches = matcher(parsed_doc)

    for rel in relationship_set.relationships:
        if isinstance(rel, FatherSonRelationship):
            print('{} is the father of {}'.format(rel.father, rel.son))
        elif isinstance(rel, FatherDaughterRelationship):
            print('{} is the father of {}'.format(rel.father, rel.daughter))
        elif isinstance(rel, GendreRelationship):
            print('An unnamed woman is the daughter of {} and husband of {}'.format(
                rel.father, rel.husband
            ))

    print('Matchers done')


if __name__ == '__main__':
    main()
