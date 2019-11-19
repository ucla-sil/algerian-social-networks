import unittest

import spacy

import quotemerger
from tests.TestUtilsMixin import TestUtilsMixin


class MarriageRelationships1Tests(unittest.TestCase, TestUtilsMixin):

    nlp = spacy.load('fr')
    merger = quotemerger.HyphenatedNameMerger(nlp.vocab)
    nlp.add_pipe(merger.merger, first=True)

    def testM1FindsFatherNameAndHusbandName(self):
        self.notImplemented()


class MarriageRelationship2Tests(unittest.TestCase, TestUtilsMixin):

    nlp = spacy.load('fr')
    merger = quotemerger.HyphenatedNameMerger(nlp.vocab)
    nlp.add_pipe(merger.merger, first=True)

    def testM2FindsFatherNameAndHusbandName(self):
        self.notImplemented()


class MarriageRelationship3Tests(unittest.TestCase, TestUtilsMixin):

    nlp = spacy.load('fr')
    merger = quotemerger.HyphenatedNameMerger(nlp.vocab)
    nlp.add_pipe(merger.merger, first=True)

    def testM3FindsFatherNameAndHusbandName(self):
        self.notImplemented()


class MarriageRelationship4Tests(unittest.TestCase, TestUtilsMixin):

    nlp = spacy.load('fr')
    merger = quotemerger.HyphenatedNameMerger(nlp.vocab)
    nlp.add_pipe(merger.merger, first=True)

    def testM4FindsFatherNameAndHusbandName(self):
        test_case = """Avec la fraction la plus turbulente des Douaouda commandée par 
            Oum-Hanni veuve de Ahmed Ben Selthri, il contracta une alliance en épousant 
            sa fille.
        """
        parsed_doc = self.nlp(test_case)
        self.assertEqual('')
        self.notImplemented()


class MarriageRelationship5Tests(unittest.TestCase, TestUtilsMixin):

    nlp = spacy.load('fr')
    merger = quotemerger.HyphenatedNameMerger(nlp.vocab)
    nlp.add_pipe(merger.merger, first=True)

    def testM5FindsFatherNameAndHusbandName(self):
        test_case = """
            Ce personnage avait jusqu’alors résidé à Alger où il avait épousé la belle Azîza-Bey, 
            veuve de son frère.  
        """
        self.notImplemented()


class MarriageRelationship6Tests(unittest.TestCase, TestUtilsMixin):

    nlp = spacy.load('fr')
    merger = quotemerger.HyphenatedNameMerger(nlp.vocab)
    nlp.add_pipe(merger.merger, first=True)

    def testM4FindsFatherNameAndHusbandName(self):
        self.notImplemented()
