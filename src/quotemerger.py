import spacy


class HyphenatedNameMerger:
    
    def __init__(self, vocab):
        self.__matcher = spacy.matcher.Matcher(vocab)
        self.__matcher.add('HYPHENATED_NAMES', None, [
            {'TEXT': {'REGEX': r"[A-Z][\w'’]+"}},
            {'TEXT': {'REGEX': r'-'}},
            {'TEXT': {'REGEX': r"[A-Z][\w'’]+"}},
            {'TEXT': {'REGEX': r"^([A-Z])|([MR][\w’'-]+)|(-)|(’)$"}, 'OP': '*'},
        ])

        self.__matcher.add('NAMES_WITH_APOSTROPHES', None, [
            {'TEXT': {'REGEX': r"[A-Z][\w'’]+"}},
            {'TEXT': {'REGEX': r'-'}},
            {'TEXT': {'REGEX': r"^([A-Z])|([A-Z][\w’'-]+)|(-)|(’)$"}, 'OP': '*'},
            {'TEXT': {'REGEX': r"[MR]['’]+"}},
            {'TEXT': {'REGEX': r"[\w]+"}},
        ])

    def merger(self, doc):
        matched_spans = []
        matches = self.__matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            matched_spans.append(span)
        for span in matched_spans:
            span.merge()
        return doc
