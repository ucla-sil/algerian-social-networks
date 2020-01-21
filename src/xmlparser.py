import typing


class Parser:

    def __init__(self, parent:'instanceof(self)'=None):
        self.parent = parent

    def handle(self, char: str) -> 'instanceof(self)':
        pass


def string_to_xml(in_string: str, starting_parser:Parser = None):
    parser = starting_parser or Parser()

    for index, char in enumerate(in_string):
        parser = parser.handle(char, index)


class ElementParser(Parser):

    def __init__(self, parent):
        self.parent = parent
        self.opening_tag = None
        self.children = []
        self.closing_tag = None

    def handle(self, char: str):
        """

        < -- open new tag
        '\s' -- increment character count but do nothing else
        '\w\d' -- add to body or create text element

        :param char:
        :return:
        """
        pass


class TagParser(Parser):

    def __init__(self, parent):
        super().__init__(parent)
        self.name = None
        self.attributes = []

    def handle(self, char: str):
        """
        /    -- this is a closing tag so tell parent it's closed when we reach the end
        >    -- terminate tag and return control to parent
        \w\d -- tag name or attribute value

        :param char:
        :return:
        """
        if char == '<':
            pass
        elif char == '>':
            pass


class TagNameParser(Parser):

    def __init__(self, parent: Parser):
        super().__init__(parent)
        self.tag_name = ''

    def handle(self, char: str) -> Parser:
        if char == ' ':
            return self.parent
        else:
            self.tag_name += char
            return self


class TextElementParser(Parser):

    def __init__(self, parent: Parser):
        super().__init__(parent)
        self.content = ''

    def handle(self, char: str) -> Parser:
        if char == '<':
            return self.parent.handle(char)
        else:
            self.content += char


class AttributeNameParser(Parser):

    def __init__(self, parent: Parser):
        super().__init__(parent)


class TextElementParser(Parser):
    pass


class AttributeValueParser(Parser):
    pass




