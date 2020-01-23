import codecs
import glob

import lxml.etree
import xml.dom.minidom
import spacy.tokens

import elra

# Sample format
"""
1. Filename
2. ?
3. ?
4. tokens
5. POS tag
6. parse tree
7. lemma
8.
9.
10. speaker
11.
12.
13.
14. co-reference label

"""

nlp = spacy.load('fr_core_news_md')

print('Spacy model loaded ...')

out_file = codecs.open('./elra-w0032.conll', 'w', encoding='utf-8')

# Format, from http://conll.cemantix.org/2012/data.html:
#  1. Document ID
#  2. Part number (optional)
#  3. Word number
#  4. Word
#  5. POS
#  6. Parse bit
#  7. Predicate lemma
#  8. Predicate frameset ID
#  9. Word sense
#  10. Speaker/author (optional)
#  11. Named Entities
#  12. Predicate arguments
#

# conll = spacy_conll.Spacy2ConllParser(model='fr_core_news_md')


def _is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_morphology(tagmap, tag):
    feats = [f'{prop}={val}' for prop, val in tagmap[tag].items() if not _is_number(prop)] if tag in tagmap else []
    if feats:
        return '|'.join(feats)
    else:
        return '-'

def doc_to_tuples(nlp, doc, line_idx):
    """

    :param nlp:
    :param doc:
    :param line_idx:
    :return: Doc in format below:

    1.
    2.
    3.
    4. word
    5. POS tag
    6. parse tree
    7. verb lemma
    8.
    9.
    10. speaker
    11.
    12.
    13.
    14. coref
    """
    for sent in doc.sents:
        line_idx += 1
        parsed_sent = ''
        lines = []

        for idx, word in enumerate(sent, 1):
            if not word.text.strip():
                continue
            if word.dep_.lower().strip() == 'root':
                head_idx = 0
            else:
                head_idx = word.head.i + 1 - sent[0].i

            line_tuple = (
                idx, # 2
                '-', # 3
                word.text,
                word.pos_,
                get_morphology(nlp.Defaults.tag_map, word.tag_),
                # word.tag_,
                word.lemma_,
                head_idx,
                '-',
                '-',
                word.dep_,
                '-',
                '-',
                word._.coref,
            )
            parsed_sent += '\t'.join(map(lambda x: str(x), line_tuple)) + '\n'
            lines.append(line_tuple)

        yield line_idx, lines, parsed_sent


def doc_to_tuples_generator(nlp, doc, line_idx):
    for sent in doc.sents:
        line_idx += 1

        for idx, word in enumerate(sent, 1):
            if not word.text.strip():
                continue
            if word.dep_.lower().strip() == 'root':
                head_idx = 0
            else:
                head_idx = word.head.i + 1 - sent[0].i

            line_tuple = (
                idx, # 2
                '-', # 3
                word.text,
                word.pos_,
                get_morphology(nlp.Defaults.tag_map, word.tag_),
                # word.tag_,
                word.lemma_,
                head_idx,
                '-',
                '-',
                word.dep_,
                '-',
                '-',
                word._.coref,
            )
            yield line_idx, line_tuple, None



def test():
    doc = nlp("Antoine voudrait aller à Paris.")


    for item in doc_to_tuples(nlp, doc, 0):
        print(item[1])




if __name__ == '__main__':
    spacy.tokens.Token.set_extension('coref', default='-')
    for in_dir in ['STENDHAL/articles-hermes', 'XRCE/JOC', 'XRCE/LeMonde', ]:
        for in_file_name in glob.glob('../../../W0032_2/{}/*.xml'.format(in_dir)):
            print('Tagging {}'.format(in_file_name))
            #parser = lxml.etree.XMLParser(encoding='ISO-8859-1')
            with open(in_file_name, 'rb') as in_file:
                all_xml = in_file.read()

                parser = lxml.etree.XMLParser(encoding='ISO-8859-1', dtd_validation=True)
                for_text = lxml.etree.parse(in_file_name, parser=parser)
                for_dom = xml.dom.minidom.parse(in_file_name)

                # all_text, references = elra.whole_file_to_references(all_xml)

                all_text, references = elra.whole_file_to_references(for_text, for_dom)
                all_text_doc = nlp(all_text)

                elra.tag_nlp_doc(all_text_doc, references)

                # for token in all_text_doc:
                #     print(token, token._.coref)

                for idx, lines, _ in doc_to_tuples_generator(nlp, all_text_doc, 0):
                    # print(in_file_name, line[1])
                    print(in_file_name, '\t'.join([str(line) for line in lines]))

            break
        break

        if 0:
            parser = lxml.etree.XMLParser(encoding='ISO-8859-1', dtd_validation=True)
            #instance_file_xml = lxml.etree.parse(in_file_name)
            instance_file_xml = lxml.etree.parse(in_file_name, parser)
            for paragraph in instance_file_xml.findall('.//p'):
                text = paragraph.text
                if not text:
                    break
                # doc = nlp(text)

                # then add in anaphoras
                # print(lxml.etree.tostring(paragraph))
                for sentence in paragraph.findall('.//s'):
                    continue
                    print(lxml.etree.tostring(sentence, encoding='unicode'))
                    for child in sentence.getchildren():
                        print(lxml.etree.tostring(child, method='text', encoding='unicode'))
                    # print(lxml.etree.tostring(sentence, method='text', encoding='unicode'))
                    # goal: count through the strings. Catch every time an anaphora reference happens.
                    # Mark the beginning and ending character of every span of text that is inside an <exp /> element
                    # Then go back and, using Doc.char_span, mark those as references or anaphoras
                    for child in sentence:
                        pass
                        # print(child.tag, child.text)
                        # print(str(lxml.etree.tostring(token))[2:]);
                # make map of phrases that are sources (<exp> elements)
                # make map of sections that co-ref something (exp > ptr["coref"] elements)


            dom_doc = xml.dom.minidom.parse(in_file_name)
            for para in dom_doc.getElementsByTagName('p'):
                for sentence in para.getElementsByTagName('s'):
                    for child in sentence.childNodes:
                        if isinstance(child, xml.dom.minidom.Text):
                            print('{}:{}'.format(len(child.data), child.data))
                            # print(len(child.data), ":", child.data)
                        else:
                            if isinstance(child.childNodes[0], xml.dom.minidom.Text):
                                print('{}:{}'.format(child.tagName, child.childNodes[0].data))
                                # print(child.tagName, ": ", child.childNodes[0].data)
                            else:
                                ref = child.childNodes[0].getAttribute('src')
                                print('{}:{} -> {}'.format(child.tagName, child.childNodes[1].data, ref))
                                # print(child.tagName, ": ", child.childNodes[1].data, " -> ", ref)

