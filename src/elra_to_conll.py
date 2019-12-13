import codecs
import glob
import lxml.etree
import spacy

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

out_file = codecs.open('./elra-w0032.conll', 'w', encoding='utf-8')

for in_dir in ['STENDHAL/articles-hermes', 'XRCE/JOC', 'XRCE/LeMonde', ]:
    for in_file_name in glob.glob('../../../W0032/{}/*.xml'.format(in_dir)):
        print(in_file_name)
        in_file = open(in_file_name)
        #parser = lxml.etree.XMLParser(encoding='ISO-8859-1')
        parser = lxml.etree.XMLParser(encoding='ISO-8859-1', dtd_validation=True)
        #instance_file_xml = lxml.etree.parse(in_file_name)
        instance_file_xml = lxml.etree.parse(in_file_name, parser)
        for paragraph in instance_file_xml.findall('.//p'):
            #findall returns bytes, so we need to convert to a string for nlp(text) to work.
            #trim the first two characters as these are always b' because each item consisted of bytes
            text = str(lxml.etree.tostring(paragraph))[2:];
            #print(text);
            doc = nlp(text)
            # then add in anaphoras
            #for sentence in paragraph.findall('.//s'):
            #    for token in sentence:
            #        print(str(lxml.etree.tostring(token))[2:]);
