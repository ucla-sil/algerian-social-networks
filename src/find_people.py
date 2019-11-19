"""
Process:

    1. Iterate through document and find every NER
    2. Capture mentions
    3. Look for patterns mentioning each person
    4. Update with familial relationships
    5. Print out tree as nodes and edges (for each person, write out relationships to others)

"""
import codecs

import spacy

import quotemerger
from patterns import MATCHERS
from relationships import Person, PeopleSet, name_from_text, FatherDaughterRelationship, GendreRelationship, \
    FatherSonRelationship


def gender_to_parent(gender):
    if gender == 'male':
        return 'father'
    else:
        return 'mother'

def main():
    in_file = codecs.open('Mercier_1600-1837.txt').read()
    nlp = spacy.load('fr')
    print('Model loaded ...')
    merger = quotemerger.HyphenatedNameMerger(nlp.vocab)
    nlp.add_pipe(merger.merger, first=True)

    parsed_doc = nlp(in_file)
    print('Parsed doc ...')

    named_people = {}
    relationship_set = PeopleSet(named_people)
    for ent in parsed_doc.ents:
        if ent.label_ == 'PERSON':
            name = name_from_text(ent)
            named_people[name] = Person(name)

    print('Found all people ...')

    # for name in sorted(named_people.keys()):
    #     print(name)

    # Iterate through all matches and update relationships
    matcher = spacy.matcher.Matcher(nlp.vocab)
    matcher.add('FATHER_SON_1', relationship_set.handle_fs_1, MATCHERS['FATHER_SON_1'])
    matcher.add('FATHER_SON_2', relationship_set.handle_fs_2, MATCHERS['FATHER_SON_2'])
    matcher.add('FATHER_SON_3', relationship_set.handle_fs_3, MATCHERS['FATHER_SON_3'])

    matcher.add('FATHER_DAUGHTER_2', relationship_set.handle_fd_2, MATCHERS['FATHER_DAUGHTER_2'])
    matcher.add('FATHER_DAUGHTER_4', relationship_set.handle_fd_4, MATCHERS['FATHER_DAUGHTER_4'])

    matcher.add('GENDRE_1', relationship_set.handle_gendre_1, MATCHERS['GENDRE_1'])
    matcher.add('GENDRE_2', relationship_set.handle_gendre_2, MATCHERS['GENDRE_2'])
    parsed_doc = nlp(in_file)
    matcher(parsed_doc)

    for _, person in relationship_set.people.items():
        for child in person.children:
            print('{} is the {} of {}'.format(
                person.name, gender_to_parent(person.gender), child
            ))

if __name__ == '__main__':
    main()

