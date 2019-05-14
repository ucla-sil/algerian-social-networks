#!/usr/bin/env python
# coding: utf8
"""A simple example of extracting relations between phrases and entities using spaCy's named entity recognizer and the dependency parse. Here, we extract money and currency values (entities labelled as MONEY) and then check the dependency tree to find the noun phrase they are referring to – for example: $9.4 million --> Net income.

Compatible with: spaCy v2.0.0+

Ashley's note: I'm working to modify this code to extract relational data from French historical sources.
"""
from __future__ import unicode_literals, print_function

import plac
import spacy

nlp = spacy.load('fr')

TEXTS = open('sample.txt', 'r').readlines() #open a document


@plac.annotations(
    model=("Model to load (needs parser and NER)", "positional", None, str))
def main(model='fr'):
    nlp = spacy.load(model) # uses French language model
    print("Loaded model '%s'" % model)
    print("Processing %d texts" % len(TEXTS))



# continue modifying code from here. Group parent-child relationships by type.
KEYWORDS = set(['mère', 'père', 'fils', 'fille', 'épous', 'femme', 'client', 'parent', 'mari', 'veuve'])
def extract_relations(previous_sentence, sentence): # merge entities and noun chunks into one token. Is this what I want to do?
	# merges two arrays - doc.ents and doc.noun_chunks. Identify what doc.ents does. noun_chunks method pulls noun phrases - phrases with a noun as the head. "noun + the words describing the noun," such as "autonomous cars," "lavish green grass," etc.
    # spans = list(previous_sentence.ents) + list(previous_sentence.noun_chunks)
    # for span in spans:
    #     span.merge()
    # spans = list(sentence.ents) + list(sentence.noun_chunks)
    # for span in spans:
    #     span.merge()

    found_it = False

    relationship = {'parent': None, 'child': None,}

    for index, word in TEXTS:
        if word.text in KEYWORDS:
            found_it = True
            for word_2 in sentence:
                if word_2.pos_ == 'PROPN':
                    if word.text == 'fils':
                        relationship['child'] = word_2
                    else:
                        relationship['parent'] = word_2
                    break
                index -= 1
            break

            # If père appears in the sentence as well, ignore.

    to_check = 'parent' if relationship['child'] else 'child'
    other = 'parent' if to_check == 'child' else 'child'
    for index, word in enumerate(sentence):
        if word.text == relationship[other].text:
            continue
        if word.pos_ == 'PROPN':
            relationship[to_check] = word
            return relationship


    if not found_it:
        return []

    relations = [] 
    aggregate = []

    for index, word in enumerate(sentence):
        if word.text in KEYWORDS:
            found_it = True
            for word_2 in sentence:
                if word_2.pos_ == 'PROPN':
                    if word.text == 'fille':
                        relationship['child'] = word_2
                    else:
                        relationship['parent'] = word_2
                    break
                index -= 1
            break


    found_it = False
    for word in doc:
        if aggregate:
            if word.text in KEYWORDS:
                found_it = True
            aggregate.append(word)
        if word.ent_type_ == 'PER':
            aggregate.append(word)
            if len(aggregate) > 1:
                break
    if found_it:        
        return aggregate
    else:
        return []
    
    for person in filter(lambda w: w.ent_type_ == 'PER', doc):
        print(person.dep_)


    if relations:
        print('{parent} is parent of {child}'.format(**relations))


if __name__ == '__main__':
    plac.call(main)

    # Expected output:
    # Net income      MONEY   $9.4 million
    # the prior year  MONEY   $2.7 million
    # Revenue         MONEY   twelve billion dollars
    # a loss          MONEY   1b










    