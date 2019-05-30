import unittest

import spacy

from quotemerger import HyphenatedNameMerger
from tests.TestUtilsMixin import TestUtilsMixin


class HyphenatedNameMergerTests(unittest.TestCase, TestUtilsMixin):

    # Setup is done up here because loading the language model takes a long time
    nlp = spacy.load('fr')
    merger = HyphenatedNameMerger(nlp.vocab)
    nlp.add_pipe(merger.merger, first=True)

    def setUp(self) -> None:
        # self.matcher = spacy.matcher.Matcher(self.nlp.vocab)
        # self.merger = HyphenatedNameMerger(self.nlp.vocab)
        # self.matcher = spacy.matcher.Matcher(self.nlp.vocab)
        # self.matcher.add(
        #     'PROPER_NAME_1',
        #     self.__find_proper_name,
        #     [{'POS': {'IN': ['PROPN',]}, 'OP': '+'}]
        # )
        # self.matches = []
        # self.nlp.add_pipe(self.merger.merger, first=True)
        pass

    def __find_proper_name(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        current_match = str(inner_doc)
        if self.matches:
            last_match = self.matches[-1]
            if current_match.startswith(last_match):
                self.matches[-1] = current_match
            elif last_match.endswith(current_match):
                pass
            else:
                self.matches.append(current_match)
        else:
            self.matches.append(current_match)

    def testSingleHyphenatedNames(self):
        test_case = "Je suis Ahmed-Bou."
        parsed_doc = self.nlp(test_case)
        self.assertEqual('Ahmed-Bou', parsed_doc[2].text)

    def testNameWithSimpleNameThenHyphenatedNameIsOneName(self):
        test_case = "Non. Je suis Ahmed Abd-Karim."
        parsed_doc = self.nlp(test_case)
        self.assertEqual('Abd-Karim', parsed_doc[5].text)

    def testNameWithThreeHyphenatedNamesIsOneName(self):
        test_case = " L’année suivante, le cheikh El-Islam-Mohammed mourait en revenant du pèlerinage."
        parsed_doc = self.nlp(test_case)
        self.assertEqual('El-Islam-Mohammed', parsed_doc[7].text)

    def testNameWithFourHyphenatedNamesIsOneName(self):
        test_case = "Et tu est Abd-El-Kerim-El-Feggoun, n'est-ce pas?"
        parsed_doc = self.nlp(test_case)
        self.assertEqual('Abd-El-Kerim-El-Feggoun', parsed_doc[3].text)

    def testHyphenatedWordsDoNotMatch(self):
        test_case = "Celui-ci n'est pas un pipe"
        parsed_doc = self.nlp(test_case)
        self.assertEqual('Celui-ci', parsed_doc[0:1].text)

    def testHyphenatedWordsFollowedByAnotherWordThenHyphenatedNameOnlyMatchesName(self):
        test_case = 'Celui-ci est le grand Abd-El-Kerim-El-Feggoun, mon pére.'
        parsed_doc = self.nlp(test_case)
        self.assertEqual('Abd-El-Kerim-El-Feggoun', parsed_doc[4].text)

    def testNameFollowedByHyphenatedWordOnlyMatchesName(self):
        test_case = 'Abd-El-Kerim-El-Feggoun, mon pére.'
        parsed_doc = self.nlp(test_case)
        self.assertEqual('Abd-El-Kerim-El-Feggoun', parsed_doc[0].text)

    def testNameFollowedBySimpleWordFollowedByHyphenatedNameOnlyMatchesName(self):
        test_case = 'Et tu, Abd-El-Kerim-El-Feggoun, celui-ci est mon pére.'
        parsed_doc = self.nlp(test_case)
        self.assertEqual('Abd-El-Kerim-El-Feggoun', parsed_doc[3].text)

    def testTwoHyphenatedNamesSeparatedBySpaceMatchTwoNames(self):
        test_case = 'Et moi, El-Islam-Mohammed, je suis Abd-El-Kerim et ton pére.'
        parsed_doc = self.nlp(test_case)
        self.assertEqual('El-Islam-Mohammed', parsed_doc[3].text)
        self.assertEqual('Abd-El-Kerim', parsed_doc[7].text)

    def testTwoHyphenatedNamesSeparatedByAnotherWordMatchTwoNames(self):
        test_case = 'El-Islam-Mohammed et Abd-El-Kerim vont pour le supermarchet.'
        parsed_doc = self.nlp(test_case)
        self.assertEqual('El-Islam-Mohammed', parsed_doc[0].text)
        self.assertEqual('Abd-El-Kerim', parsed_doc[2].text)

    def testTwoHyphenatedNamesSeparatedByTwoWordsMatchTwoNames(self):
        test_case = 'El-Islam-Mohammed et tu, Abd-El-Kerim, vont pour le supermarchet.'
        parsed_doc = self.nlp(test_case)
        self.assertEqual('El-Islam-Mohammed', parsed_doc[0].text)
        self.assertEqual('Abd-El-Kerim', parsed_doc[4].text)

    def testTwoHyphenatedNamesSeparatedByHyphenatedWordsMatchTwoNames(self):
        test_case = 'El-Islam-Mohammed et Celui-ci, tu, Abd-El-Kerim, vont pour le supermarchet.'
        parsed_doc = self.nlp(test_case)
        self.assertEqual('El-Islam-Mohammed', parsed_doc[0].text)
        self.assertEqual('Abd-El-Kerim', parsed_doc[6].text)


class NamesWithApostrophesMergerTests(unittest.TestCase, TestUtilsMixin):

    nlp = spacy.load('fr')
    merger = HyphenatedNameMerger(nlp.vocab)
    nlp.add_pipe(merger.merger, first=True)

    def testSingleNameWithApostrophes(self):
        test_case = 'El-R’ozlane'
        parsed_doc = self.nlp(test_case)
        self.assertEqual(test_case, parsed_doc[0].text)

    def testSingleNameWithHyphensAndApostrophes(self):
        test_case = 'Sour-El-R’ozlane'
        parsed_doc = self.nlp(test_case)
        self.assertEqual(test_case, parsed_doc[0].text)

    def testWordsWithApostrophesDoNotMatch(self):
        test_case = "C'est la vie."
        parsed_doc = self.nlp(test_case)
        self.assertEqual('C\'', parsed_doc[0].text)
        self.assertEqual('est', parsed_doc[1].text)

    def testNamesWithApostrophesMatchInASentence(self):
        test_case = """Bien accueilli par lui, il obtint une escorte qui le conduisit 
            jusqu’à Sour-El-R’ozlane (Aumale), avec l’appui du cheikh Bouzid, chef des 
            Oulad- Mokrane de la Medjana; de là, il gagna Alger. Mais, le dey de 
            Tunis réclama avec insistance l’extradition de son neveu et le pacha 
            Kourd-Abdi ne put moins faire que de l’incarcérer (1729).
        """
        parsed_doc = self.nlp(test_case)
        self.assertEqual('Sour-El-R’ozlane', parsed_doc[15].text)

    def testWordsWithApostrophesAndNamesMatchesOnlyNames(self):
        test_case = "C'est Sour-El-R’ozlane, l'advocat."
        parsed_doc = self.nlp(test_case)
        self.assertEqual('Sour-El-R’ozlane', parsed_doc[2].text)

    def testTwoNamesWithApostrophesMatchBothNames(self):
        test_case = """Bien accueilli par lui, il obtint une escorte qui le conduisit 
            jusqu’à Sour-El-R’ozlane (Aumale), avec l’appui du cheikh Bouzid, chef des 
            Oulad- Mokrane de la Medjana; de là, il gagna Alger. Mais, le dey de 
            Tunis réclama avec insistance l’extradition de son neveu et le pacha 
            Kourd-Abdi ne put moins faire que de l’incarcérer (1729).
        """
        parsed_doc = self.nlp(test_case)
        self.assertEqual('Sour-El-R’ozlane', parsed_doc[15].text)

