import codecs

import spacy.matcher
import spacy.tokenizer

import quotemerger
from patterns import MATCHERS
from relationships import FatherSonRelationship, FatherDaughterRelationship, GendreRelationship, RelationshipHandler

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


# NAME = {'POS': 'PROPN', 'OP': '+'}


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



def main():
    in_file = codecs.open('Mercier_1600-1837.txt').read()
    relationship_set = RelationshipHandler()
    merger = quotemerger.HyphenatedNameMerger(nlp.vocab)
    nlp.add_pipe(merger.merger, first=True)
    matcher.add('FATHER_SON_1', relationship_set.handle_fs_1, MATCHERS['FATHER_SON_1'])
    matcher.add('FATHER_SON_2', relationship_set.handle_fs_2, MATCHERS['FATHER_SON_2'])
    matcher.add('FATHER_SON_3', relationship_set.handle_fs_3, MATCHERS['FATHER_SON_3'])

    matcher.add('FATHER_DAUGHTER_2', relationship_set.handle_fd_2, MATCHERS['FATHER_DAUGHTER_2'])
    matcher.add('FATHER_DAUGHTER_4', relationship_set.handle_fd_4, MATCHERS['FATHER_DAUGHTER_4'])

    matcher.add('GENDRE_1', relationship_set.handle_gendre_1, MATCHERS['GENDRE_1'])
    matcher.add('GENDRE_2', relationship_set.handle_gendre_2, MATCHERS['GENDRE_2'])
    parsed_doc = nlp(in_file)
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
