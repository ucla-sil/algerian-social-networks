import unittest

from relationships import name_from_text
from tests.TestUtilsMixin import TestUtilsMixin


class NameFromTests (unittest.TestCase, TestUtilsMixin):

    def __runTest(self, expected, input):
        self.assertEqual(expected, name_from_text(input))

    def testNameFromTextDoesNotChangeNameWitoutBey(self):
        self.__runTest('Mourad El-Islam', ['Mourad', 'El-Islam'])

    def testNameFromTextRemovesBeyLowercase(self):
        self.__runTest('Mourad', ['Mourad-bey'])

    def testNameFromTextRemovesBeyAsTokens(self):
        self.__runTest('Mourad', ['Mourad', '-bey'])

    def testNameFromTextRemovesBeyAsTokensWithHyphenOnEnd(self):
        self.__runTest('Mourad', ['Mourad-', 'bey'])

    def testNameWithBeyAtBeginningRemovesBey(self):
        self.__runTest('Mourad', ['Bey', 'Mourad',])

    def testNameWithBeyAndHyphenAtBeginningRemovesBey(self):
        self.__runTest('Mourad', ['Bey-', 'Mourad', ])

    def testNameWithBeyAndHyphenAtBeginningAsOneTokenRemovesBey(self):
        self.__runTest('Mourad', ['Bey-Mourad', ])
