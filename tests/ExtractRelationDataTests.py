import unittest
import xml.dom.minidom

import lxml

import elra
import elra_to_conll


from tests.TestUtilsMixin import  TestUtilsMixin


class ExtractRelationDataTests(unittest.TestCase, TestUtilsMixin):

    def testFindCoRefElementSpansCorrectly(self):
        in_data = xml.dom.minidom.parseString(''.join(["""<s> Argumenter, pour <exp id="e3455">chacun</exp>, c'est ainsi, """,
            """à la fois, défendre <exp id="e3456">un point de vue</exp> et vouloir <exp id="e3457">""",
            """<ptr type="coref" src="e3456"/>le</exp> faire partager, autrement dit : choisir <exp id="e3458">""",
            """<ptr type="coref" src="e3455"/>ses</exp> mots et organiser <exp id="e3459">""",
            """<ptr type="coref" src="e3455"/>son</exp>  """,
            """discours dans l'intention de faire adhérer à des idées, à des convictions. </s> """,
        ]))

        expected = [
            {'start': 18, 'end': 24, 'type': 'src', 'id': 'e3455', 'text': 'chacun', },
            {'start': 59, 'end': 74, 'type': 'src', 'id': 'e3456', 'text': 'un point de vue', },
            # TODO: check if the following actually work in practice
            {'start': 86, 'end': 88, 'type': 'ref', 'id': 'e3457', 'ref': 'e3456', 'text': 'le', },
            {'start': 129, 'end': 132, 'type': 'ref', 'id': 'e3458', 'ref': 'e3455', 'text': 'ses', },
            {'start': 151, 'end': 154, 'type': 'ref', 'id': 'e3459', 'ref': 'e3455', 'text': 'son', },
        ]

        actual = elra.align_xml_to_string(in_data.getElementsByTagName('s')[0])
        self.assertEqual(expected, actual)
# " Argumenter, pour chacun, c'est ainsi, à la fois, défendre un point de vue et vouloir le faire partager, autrement dit : choisir ses mots et organiser son discours dans l'intention de faire adhérer à des idées, à des convictions. "

    def testExtractTextReturnsCorrectText(self):
        in_data = lxml.etree.fromstring(''.join([
            """<s> Argumenter, pour <exp id="e3455">chacun</exp>, c'est ainsi, """,
            """à la fois, défendre <exp id="e3456">un point de vue</exp> et vouloir <exp id="e3457">""",
            """<ptr type="coref" src="e3456"/>le</exp> faire partager, autrement dit : choisir <exp id="e3458">""",
            """<ptr type="coref" src="e3455"/>ses</exp> mots et organiser <exp id="e3459">""",
            """<ptr type="coref" src="e3455"/>son</exp> """,
            """discours dans l'intention de faire adhérer à des idées, à des convictions. </s> """,
        ]))
        self.assertEqual(
            " Argumenter, pour chacun, c'est ainsi, à la fois, défendre un point de vue et vouloir le faire partager, autrement dit : choisir ses mots et organiser son discours dans l'intention de faire adhérer à des idées, à des convictions. ",
            elra.extract_text_lxml(in_data)
        )

    def testExtractDistinctiveSegment(self):
        in_data = lxml.etree.fromstring(''.join([
            """<s> La controverse politique, la publicité commerciale, les discussions ordinaires entretiennent """,
            """<exp id="e3460">cette nécessité <seg type="distinctif">quotidienne</seg></exp> : <exp id="e3461"> """,
            """<ptr type="desc" src="e3460"/>celle d'affirmer, de s'affirmer</exp> et par voie de conséquence, de """,
            """créer des champs d'accord, au prix de désaccords ou d'exclusions partagées : " La plus haute """,
            """science du gouvernement est la rhétorique, c'est-à-dire la science du parler. </s> """
        ]))
        self.assertEqual(
            """ La controverse politique, la publicité commerciale, les discussions ordinaires entretiennent cette nécessité quotidienne :  celle d'affirmer, de s'affirmer et par voie de conséquence, de créer des champs d'accord, au prix de désaccords ou d'exclusions partagées : " La plus haute science du gouvernement est la rhétorique, c'est-à-dire la science du parler. """,
            elra.extract_text_lxml(in_data)
        )

