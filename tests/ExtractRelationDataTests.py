import unittest
import xml.dom.minidom

import lxml
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

        actual = elra_to_conll.align_xml_to_string(in_data.getElementsByTagName('s')[0])
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
        print(in_data)
        self.assertEqual(
            " Argumenter, pour chacun, c'est ainsi, à la fois, défendre un point de vue et vouloir le faire partager, autrement dit : choisir ses mots et organiser son discours dans l'intention de faire adhérer à des idées, à des convictions. ",
            elra_to_conll.extract_text(in_data)
        )


