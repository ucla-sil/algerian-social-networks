import codecs

import spacy.matcher
import spacy.tokenizer

import quotemerger
from patterns import MATCHERS
from relationships import FatherSonRelationship, FatherDaughterRelationship, GendreRelationship, RelationshipHandler


def main():
    in_file = codecs.open('Mercier_1600-1837.txt').read()
    relationship_set = RelationshipHandler()
    merger = quotemerger.HyphenatedNameMerger(nlp.vocab)
    nlp.add_pipe(merger.merger, first=True)
    matcher.add('FATHER_SON_1', relationship_set.handle_fs_1, MATCHERS['FATHER_SON_1'])
    matcher.add('FATHER_SON_2', relationship_set.handle_fs_2, MATCHERS['FATHER_SON_2'])
    matcher.add('FATHER_SON_3', relationship_set.handle_fs_3, MATCHERS['FATHER_SON_3'])

    matcher.add('FATHER_DAUGHTER_1', relationship_set.handle_fd_1, MATCHERS['FATHER_DAUGHTER_1'])
    matcher.add('FATHER_DAUGHTER_2', relationship_set.handle_fd_2, MATCHERS['FATHER_DAUGHTER_2'])
    matcher.add('FATHER_DAUGHTER_3', relationship_set.handle_fd_3, MATCHERS['FATHER_DAUGHTER_3'])
    matcher.add('FATHER_DAUGHTER_4', relationship_set.handle_fd_4, MATCHERS['FATHER_DAUGHTER_4'])

    matcher.add('MARIAGE_1',relationship_set.handle_mariage_1_and_2, MATCHERS['MARIAGE_1'])
    matcher.add('MARIAGE_2',relationship_set.handle_mariage_1_and_2, MATCHERS['MARIAGE_2'])
    matcher.add('MARIAGE_3',relationship_set.handle_mariage_3_and_4, MATCHERS['MARIAGE_3'])
    matcher.add('MARIAGE_4',relationship_set.handle_mariage_3_and_4, MATCHERS['MARIAGE_4'])
    matcher.add('MARIAGE_5',relationship_set.handle_mariage_5, MATCHERS['MARIAGE_5'])
    matcher.add('MARIAGE_6',relationship_set.handle_mariage_6, MATCHERS['MARIAGE_6'])

    matcher.add('GENDRE_1', relationship_set.handle_gendre_1, MATCHERS['GENDRE_1'])
    matcher.add('GENDRE_2', relationship_set.handle_gendre_2, MATCHERS['GENDRE_2'])
    matcher.add('GENDRE_3', relationship_set.handle_gendre_3, MATCHERS['GENDRE_3'])

    matcher.add('PERE', relationship_set.handle_pere_1, MATCHERS['PERE'])

    parsed_doc = nlp(in_file)
    matches = matcher(parsed_doc)

    out_file = codecs.open('relations.csv', 'w', encoding='utf8')
    out_file.write('parent,child,relation type\n')
    for rel in relationship_set.relationships:
        if isinstance(rel, FatherSonRelationship):
            out_file.write('{},{},son\n'.format(rel.father, rel.son))
            print('{} is the father of {}'.format(rel.father, rel.son))
        elif isinstance(rel, FatherDaughterRelationship):
            out_file.write('{},{},daughter\n'.format(rel.father, rel.daughter))
            print('{} is the father of {}'.format(rel.father, rel.daughter))
        elif isinstance(rel, GendreRelationship):
            out_file.write('{},{},daughter'.format(rel.father, rel.name))
            out_file.write('{},{},spouse'.format(rel.husband, rel.name))
            print('An unnamed woman is the daughter of {} and husband of {}'.format(
                rel.father, rel.husband
            ))
    out_file.close()

    print('Matchers done')


if __name__ == '__main__':
    print('Loading model ...')
    nlp = spacy.load('fr')
    print('Model loaded')

    matcher = spacy.matcher.Matcher(nlp.vocab)
    match_merger = spacy.matcher.Matcher(nlp.vocab)

    print('Matchers initialized')

    main()

