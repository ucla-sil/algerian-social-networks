import unittest

import spacy
import xml.dom.minidom
import lxml
import elra_to_conll


class MyTestCase(unittest.TestCase):

    nlp = spacy.load('fr_core_news_md')

    def testAlignWithPatches(self):
        in_text = ''.join(["""<s> Argumenter, pour <exp id="e3455">chacun</exp>, c'est ainsi, """,
                           """à la fois, défendre <exp id="e3456">un point de vue</exp> et vouloir <exp id="e3457">""",
                           """<ptr type="coref" src="e3456"/>le</exp> faire partager, autrement dit : choisir <exp id="e3458">""",
                           """<ptr type="coref" src="e3455"/>ses</exp> mots et organiser <exp id="e3459">""",
                           """<ptr type="coref" src="e3455"/>son</exp>  """,
                           """discours dans l'intention de faire adhérer à des idées, à des convictions. </s> """,
                           ])
        in_data = xml.dom.minidom.parseString(in_text)

        """
        expected = [
            {'start': 18, 'end': 24, 'type': 'src', 'id': 'e3455', 'text': 'chacun', },
            {'start': 59, 'end': 74, 'type': 'src', 'id': 'e3456', 'text': 'un point de vue', },
            {'start': 86, 'end': 88, 'type': 'ref', 'id': 'e3457', 'ref': 'e3456', 'text': 'le', },
            {'start': 129, 'end': 132, 'type': 'ref', 'id': 'e3458', 'ref': 'e3455', 'text': 'ses', },
            {'start': 151, 'end': 154, 'type': 'ref', 'id': 'e3459', 'ref': 'e3455', 'text': 'son', },
        ]
        """

        references = elra_to_conll.align_xml_to_string(in_data.getElementsByTagName('s')[0])
        spacy.tokens.Token.set_extension('coref', default='')
        doc = self.nlp(elra_to_conll.extract_text(lxml.etree.fromstring(in_text)))
        for ref in references:
            if ref['type'] == 'src':
                result = doc.char_span(ref['start'], ref['end'], label='src')
                for token in result:
                    token._.coref = ref['id']
            else:
                result = doc.char_span(ref['start'], ref['end'], label='coref')
                for token in result:
                    token._.coref = ref['ref']
            self.assertIsNotNone(result)

