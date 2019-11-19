import glob
# import xml.etree.ElementTree
import lxml.etree

# import spacy


def main():
    dir_to_search = glob.glob('Ancor-Centre-CC-BY-SA/corpus_OTG/annotation_integree/*.xml')
    dir_to_search = ['Ancor-Centre-CC-BY-SA/corpus_OTG/annotation_integree/1AG0141.xml']
    for corpus_annotation_file in dir_to_search:
        # corpus_annotation_xml = xml.etree.ElementTree.parse(corpus_annotation_file)
        # corpus_annotation_xml = lxml.etree.ElementTree.parse(corpus_annotation_file)
        corpus_annotation_xml = lxml.etree.parse(corpus_annotation_file)
        characterization_types = corpus_annotation_xml.findall('.//type')
        # extract whole corpus
        for characterization_type in characterization_types:
            if characterization_type.text == 'ANAPHORE':
                print(characterization_type.getparent().getparent())
                relation_node = characterization_type.getparent().getparent()
                terms = relation_node.findall('./positioning/term/[@id]')
                for term in terms:
                    print(term.get('id'))
            # find parent, and then find sibling "positioning"
            # then look up specific words with those IDs

        # then, iterate through each "Turn" section and make a sentence out of that
        for section in corpus_annotation_xml.findall('//Turn'):
            print(section)

        # convert that into an NLP/Doc object:
        #   for each child node, append that to a document
        #   if it's an <anchor> node and there's a reference to a previous node, mark that as a reference
        # then output it in CoNLL format


if __name__ == '__main__':
    main()
