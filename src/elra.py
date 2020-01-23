from typing import List, Tuple

import xml.dom.minidom

import lxml.etree


def extract_text_lxml(sentence: lxml.etree._Element) -> str:
    """
    Extract entire text from set of etree nodes

    :param sentence: lxml.etree._Element sentence node of etree
    :return: str text of element and child elements
    """
    return lxml.etree.tostring(sentence, method='text', encoding='unicode')


def align_xml_to_string(sentence: xml.dom.minidom.Element) -> list:
    """

    :param sentence: xml.dom.minidom.Element <s> element from document
    :return: list references
    """
    elements = []
    current_position = 0
    for child in sentence.childNodes:
        if isinstance(child, xml.dom.minidom.Text):
            current_position += len(child.data)
        else:
            if child.tagName == 'exp':
                element = {}
                if isinstance(child.childNodes[0], xml.dom.minidom.Text):
                    texts = []
                    for node in child.childNodes:
                        if isinstance(node, xml.dom.minidom.Text):
                            texts.append(node.data)
                        else:
                            if len(node.childNodes) > 0:
                                for child2 in node.childNodes:
                                    if isinstance(child2, xml.dom.minidom.Text):
                                        texts.append(child2.data)
                                    #     print(child2.getAttribute('id'))
                                    #     print(child2.tagName)
                                # texts.append(node.childNodes[0].data)
                    text = ''.join(texts)
                    element['type'] = 'src'
                else:
                    text = child.childNodes[1].data
                    ref = child.childNodes[0].getAttribute('src')
                    element['type'] = 'ref'
                    element['ref'] = ref

                element['start'] = current_position
                element['end'] = current_position + len(text)
                element['id'] = child.getAttribute('id')
                element['text'] = text
                elements.append(element)
                current_position += len(text)
            else:
                print('Unknown child found: {}'.format(child.tagName))

    return elements


def increase_tag_positions(offset: int, elements: List[dict]) -> List[dict]:
    """
    Augment all start and end positions in list of elements

    NOTE: this creates *copies* and does not modify the original list


    :param offset: offset to increment by
    :param elements:  list of dictionaries of elements
    :return: updated list, copied
    """
    to_return = []
    for element in elements:
        added = {
            'start': element['start'] + offset,
            'end': element['end'] + offset,
            'type': element['type'],
            'id': element['id'],
            'text': element['text'],
        }
        if 'ref' in element:
            added['ref'] = element['ref']
        to_return.append(added)
    return to_return


# def whole_file_to_references(in_text: str) -> Tuple[str, List[dict]]:
def whole_file_to_references(for_text: lxml.etree.XMLParser, for_ref:xml.dom.minidom.Document) -> Tuple[str, List[dict]]:
    """
    Run process on entire document

    :param in_text: XML of document as text
    :return: whole text, plus list of references
    """

    # dtd_validation = b'.dtd' in in_text
    # parser_for_text = lxml.etree.XMLParser(encoding='ISO-8859-1', dtd_validation=dtd_validation)
    # parser_for_text.feed(in_text)
    # root_elem = parser_for_text.close()
    # for_text = lxml.etree.fromstring(in_text)
    # for_text = root_elem
    # for_ref = xml.dom.minidom.parseString(in_text)
    curr_offset = 0

    references = []
    texts = []

    for text_sentence, ref_sentence in zip(for_text.findall('.//s'), for_ref.getElementsByTagName('s')):
        text = extract_text_lxml(text_sentence)
        refs = align_xml_to_string(ref_sentence)
        references.extend(increase_tag_positions(curr_offset, refs))
        texts.append(text)
        curr_offset += len(text)

    return ''.join(texts), references


def tag_nlp_doc(doc, refs:List[dict]) -> None:
    missed_refs = []
    for ref in refs:
        if ref['type'] == 'src':
            result = doc.char_span(ref['start'], ref['end'], label='src')
            if result is None:
                missed_refs.append((ref['start'], ref['end'], ref['id'], ref['text']))
                continue
            for token in result:
                token._.coref = ref['id']
        else:
            result = doc.char_span(ref['start'], ref['end'], label='coref')
            if result is None:
                missed_refs.append((ref['start'], ref['end'], ref['id'], ref['text']))
                continue
            for token in result:
                token._.coref = ref['ref']

    missed_ref_count = len(missed_refs)
    if missed_ref_count > 0:
        print('{}/{} missed refs'.format(missed_ref_count, len(refs)))
        # for ref in missed_refs:
        #     print(ref)
