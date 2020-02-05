import glob
# import xml.etree.ElementTree
import lxml.etree

# import spacy


def main():
    for in_dir in ['STENDHAL/articles-hermes', 'XRCE/JOC', 'XRCE/LeMonde']:
        for in_file_name in glob.glob('../../../W0032/{}/*.xml'.format(in_dir)):
            print(in_file_name)
            in_file = open(in_file_name)
            #parser = lxml.etree.XMLParser(encoding='ISO-8859-1')
            parser = lxml.etree.XMLParser(encoding='ISO-8859-1', dtd_validation=True)
            #instance_file_xml = lxml.etree.parse(in_file_name)
            instance_file_xml = lxml.etree.parse(in_file_name, parser)
    
            characterization_types = instance_file_xml.findall('.//type')
            # extract whole corpus
            for characterization_type in characterization_types:
                print("HI");
                if characterization_type.text == 'ANAPHORE':
                    print(characterization_type.getparent().getparent())
                    relation_node = characterization_type.getparent().getparent()
                    terms = relation_node.findall('./positioning/term/[@id]')
                    for term in terms:
                        print(term.get('id'))
                # find parent, and then find sibling "positioning"
                # then look up specific words with those IDs

            # then, iterate through each "Turn" section and make a sentence out of that
            for section in instance_file_xml.findall('//Turn'):
                print(section)

            # convert that into an NLP/Doc object:
            #   for each child node, append that to a document
            #   if it's an <anchor> node and there's a reference to a previous node, mark that as a reference
            # then output it in CoNLL format


if __name__ == '__main__':
    main()
