import unittest

import spacy
import spacy.tokens
import xml.dom.minidom
import lxml

import elra


class AlignRelationsTest(unittest.TestCase):

    nlp = spacy.load('fr_core_news_md')
    spacy.tokens.Token.set_extension('coref', default='')

    def testAlignWithPatches(self):
        in_text = ''.join([
           """<s> Argumenter, pour <exp id="e3455">chacun</exp>, c'est ainsi, """,
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

        references = elra.align_xml_to_string(in_data.getElementsByTagName('s')[0])
        doc = self.nlp(elra.extract_text_lxml(lxml.etree.fromstring(in_text)))
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

    def testNestedDistinctiveReferences(self):
        in_text = ''.join([
                """<s> La controverse politique, la publicité commerciale, les discussions ordinaires entretiennent """,
                """<exp id="e3460">cette nécessité <seg type="distinctif">quotidienne</seg></exp> : <exp id="e3461">""",
                """<ptr type="desc" src="e3460"/>celle d'affirmer, de s'affirmer</exp> et par voie de conséquence, de """,
                """créer des champs d'accord, au prix de désaccords ou d'exclusions partagées : " La plus haute """,
                """science du gouvernement est la rhétorique, c'est-à-dire la science du parler. </s> """
            ])

        in_data = xml.dom.minidom.parseString('<p>{}</p>'.format(in_text))
        references = elra.align_xml_to_string(in_data.getElementsByTagName('s')[0])

        doc = self.nlp(elra.extract_text_lxml(lxml.etree.fromstring(in_text)))
        self.assertNotEqual(len(references), 0)
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

    def testNestedDistinctiveSentences(self):
        in_texts = ''.join([
            """<s> La controverse politique, la publicité commerciale, les discussions ordinaires entretiennent """,
            """<exp id="e3460">cette nécessité <seg type="distinctif">quotidienne</seg></exp> : <exp id="e3461">""",
            """<ptr type="desc" src="e3460"/>celle d'affirmer, de s'affirmer</exp> et par voie de conséquence, de """,
            """créer des champs d'accord, au prix de désaccords ou d'exclusions partagées : " La plus haute """,
            """science du gouvernement est la rhétorique, c'est-à-dire la science du parler. </s> """
        ])

        offset = 0
        expected = [
            {'start': 94 + offset, 'end': 94 + 27 + offset, 'type': 'src', 'id': 'e3460', 'text': 'cette nécessité quotidienne'},
            {'start': 94 + 27 + 3 + offset, 'end': 94 + 27 + 3 + 31 + offset, 'type': 'ref', 'id': 'e3461', 'ref': 'e3460', 'text': "celle d'affirmer, de s'affirmer", },
        ]

        in_text = '<p>{}</p>'.format(''.join(in_texts))

        text, refs = elra.whole_file_to_references(in_text)

        self.assertEqual(expected, refs)


    def testAcrossTwoSentences(self):
        in_texts = [
            ''.join([
                """<s> Tout le monde sait ce qu'est discuter, défendre ses opinions, tenter de convaincre un interlocuteur. </s> """
            ]),
            ''.join(["""<s> Argumenter, pour <exp id="e3455">chacun</exp>, c'est ainsi, """,
                   """à la fois, défendre <exp id="e3456">un point de vue</exp> et vouloir <exp id="e3457">""",
                   """<ptr type="coref" src="e3456"/>le</exp> faire partager, autrement dit : choisir <exp id="e3458">""",
                   """<ptr type="coref" src="e3455"/>ses</exp> mots et organiser <exp id="e3459">""",
                   """<ptr type="coref" src="e3455"/>son</exp>  """,
                   """discours dans l'intention de faire adhérer à des idées, à des convictions. </s> """,
                ])
            ]

        offset = 103
        expected = [
            {'start': 18 + offset, 'end': 24 + offset, 'type': 'src', 'id': 'e3455', 'text': 'chacun', },
            {'start': 59 + offset, 'end': 74 + offset, 'type': 'src', 'id': 'e3456', 'text': 'un point de vue', },
            {'start': 86 + offset, 'end': 88 + offset, 'type': 'ref', 'id': 'e3457', 'ref': 'e3456', 'text': 'le', },
            {'start': 129 + offset, 'end': 132 + offset, 'type': 'ref', 'id': 'e3458', 'ref': 'e3455', 'text': 'ses', },
            {'start': 151 + offset, 'end': 154 + offset, 'type': 'ref', 'id': 'e3459', 'ref': 'e3455', 'text': 'son', },
        ]

        in_text = '<p>{}</p>'.format(''.join(in_texts))

        text, refs = elra.whole_file_to_references(in_text)

        self.assertEqual(expected, refs)


    def testAcrossThreeSentences(self):
        in_texts = [
            ''.join([
                """<s> Tout le monde sait ce qu'est discuter, défendre ses opinions, tenter de convaincre un interlocuteur. </s> """
            ]),
            ''.join([
                """<s> Argumenter, pour <exp id="e3455">chacun</exp>, c'est ainsi, """,
                 """à la fois, défendre <exp id="e3456">un point de vue</exp> et vouloir <exp id="e3457">""",
                 """<ptr type="coref" src="e3456"/>le</exp> faire partager, autrement dit : choisir <exp id="e3458">""",
                 """<ptr type="coref" src="e3455"/>ses</exp> mots et organiser <exp id="e3459">""",
                 """<ptr type="coref" src="e3455"/>son</exp>  """,
                 """discours dans l'intention de faire adhérer à des idées, à des convictions. </s> """,
             ]),
            ''.join([
                """<s> La controverse politique, la publicité commerciale, les discussions ordinaires entretiennent """,
                """<exp id="e3460">cette nécessité <seg type="distinctif">quotidienne</seg></exp> : <exp id="e3461">""",
                """<ptr type="desc" src="e3460"/>celle d'affirmer, de s'affirmer</exp> et par voie de conséquence, de """,
                """créer des champs d'accord, au prix de désaccords ou d'exclusions partagées : " La plus haute """,
                """science du gouvernement est la rhétorique, c'est-à-dire la science du parler. </s> """
            ]),
        ]

        offset = 103
        offset_2 = 232
        expected = [
            {'start': 18 + offset, 'end': 24 + offset, 'type': 'src', 'id': 'e3455', 'text': 'chacun', },
            {'start': 59 + offset, 'end': 74 + offset, 'type': 'src', 'id': 'e3456', 'text': 'un point de vue', },
            {'start': 86 + offset, 'end': 88 + offset, 'type': 'ref', 'id': 'e3457', 'ref': 'e3456', 'text': 'le', },
            {'start': 129 + offset, 'end': 132 + offset, 'type': 'ref', 'id': 'e3458', 'ref': 'e3455', 'text': 'ses', },
            {'start': 151 + offset, 'end': 154 + offset, 'type': 'ref', 'id': 'e3459', 'ref': 'e3455', 'text': 'son', },

            {'start': 94 + offset + offset_2, 'end': 94 + 27 + offset + offset_2, 'type': 'src', 'id': 'e3460', 'text': 'cette nécessité quotidienne'},
            {'start': 94 + 27 + 3 + offset + offset_2, 'end': 94 + 27 + 3 + 31 + offset + offset_2, 'type': 'ref', 'id': 'e3461', 'ref': 'e3460', 'text': "celle d'affirmer, de s'affirmer", },
        ]

        in_text = '<p>{}</p>'.format(''.join(in_texts))

        text, refs = elra.whole_file_to_references(in_text)

        self.assertEqual(expected, refs)



