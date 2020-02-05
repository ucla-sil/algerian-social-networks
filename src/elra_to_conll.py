import os
import random
import codecs
import glob
import re
import shutil

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

# out_file = codecs.open('./elra-w0032.conll', 'w', encoding='utf-8')
out_files = [
    # codecs.open('./elra-w0032-training.conll', 'w', encoding='utf-8'),
    # codecs.open('./elra-w0032-testing.conll', 'w', encoding='utf-8'),
]

out_dirs = [ 'data/train', 'data/test', ]

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
                '0',
                '-',
                word._.coref,
            )
            parsed_sent += '\t'.join(map(lambda x: str(x), line_tuple)) + '\n'
            lines.append(line_tuple)

        yield line_idx, lines, parsed_sent


def doc_to_tuples_generator(nlp, doc, line_idx):
    matcher = re.compile(r'(\d+)')
    idx = 0
    last_coref = None
    last_coref_type = None
    for sent in doc.sents:
        # line_idx += 1

        for word, next_word in zip(sent, sent[1:]):
            if not word.text.strip():
                continue
            if word.dep_.lower().strip() == 'root':
                head_idx = 0
            else:
                head_idx = word.head.i + 1 - sent[0].i

            matches = matcher.search(word._.coref)
            coref = '-'
            coref_type = word._.coref_type
            if matches:
                coref = ''
                if coref_type != last_coref_type or matches[0] != last_coref:
                    coref = '('
                coref += matches[0]
                next_match = matcher.search(next_word._.coref)
                if next_word._.coref_type != coref_type or not next_match or (
                        next_match and matches[0] != next_match[0]
                    ):
                    coref += ')'

            line_tuple = (
                # idx, # 2
                idx, # 3
                word.text.strip(),
                word.pos_ or word.tag_,
                get_morphology(nlp.Defaults.tag_map, word.tag_),
                # word.tag_,
                word.lemma_.replace(' ', '-'),
                head_idx,
                '-',
                '-',
                word.dep_,
                '0',
                '-',
                coref,
                # '({})'.format(matches[0]) if matches else '-',
            )
            last_coref = matches[0] if matches and coref[-1] != ')' else '-'
            last_coref_type = word._.coref_type

            idx += 1
            yield line_idx, line_tuple, None





if __name__ == '__main__':
    for out_dir in out_dirs:
        out_dir_path = os.path.join('..', out_dir)
        if os.path.exists(out_dir_path):
            print('Wiping out {}'.format(out_dir))
            print('Found {}'.format(out_dir_path))
            shutil.rmtree(out_dir_path)
        try:
            os.mkdir(out_dir_path)
        except FileExistsError as ex:
            pass

    spacy.tokens.Token.set_extension('coref', default='-')
    spacy.tokens.Token.set_extension('coref_type', default='-')
    for in_dir in ['STENDHAL/articles-hermes', 'XRCE/JOC', 'XRCE_LeMonde', ]:
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

                simpler_file_name = in_file_name.split('/')[-1].split('.')[0] + '.v4_gold_conll'
                out_file = codecs.open(os.path.join('..', random.choice(out_dirs), simpler_file_name), 'w',
                                       encoding='utf-8')
                part_no = 1
                out_file.write("#begin document (nw/{}); part {}\n\n".format(simpler_file_name.split('.')[0], part_no))
                for idx, lines, _ in doc_to_tuples_generator(nlp, all_text_doc, part_no):
                    # print(in_file_name, line[1])
                    # print(in_file_name, '\t'.join([str(line) for line in lines]))
                    # simpler_file_name = '-'.join(in_file_name.split('/')[-2:])
                    out_file.write('nw/{}\t{}\t{}\n'.format(simpler_file_name.split('.')[0], idx, '\t'.join([str(line) for line in lines])))
                    # out_file.write('{}\t{}\n'.format(simpler_file_name, '\t'.join([str(line) for line in lines])))

                out_file.write('\n')
                out_file.write('#end document')
                out_file.close()

for out_file in out_files:
    out_file.close()
