import spacy


def quote_merger(doc):
    matched_spans = []
    matches = match_merger(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        matched_spans.append(span)
        # print(span)
    for span in matched_spans:
        span.merge()
    return doc


def matcher_for_vocab(vocab):
    match_merger = spacy.matcher.Matcher(nlp.vocab)

    match_merger.add('HYPHENATED_NAMES', None, [
        # {'TEXT': {'REGEX': r'[A-Z]\w+-[\w-]+'}}
        # {'TEXT': {'REGEX': r'\w+-\w+'}}
        {'TEXT': {'REGEX': r"[A-Z][\w'’]+"}},
        {'TEXT': {'REGEX': r'-'}},
        {'TEXT': {'REGEX': r"[A-Z][\w'’]+"}},
        {'TEXT': {'REGEX': r"^([A-Z])|([A-Z][\w’'-]+)|(-)|(’)$"}, 'OP': '*'},
        # {'TEXT': {'REGEX': r'\w+'}},
    ])


class QuoteMerger:
    
    def __init__(self, vocab):
        self.matcher = spacy.matcher.Matcher(vocab)
        self.matcher.add('HYPHENATED_NAMES', None, [
            # {'TEXT': {'REGEX': r'[A-Z]\w+-[\w-]+'}}
            # {'TEXT': {'REGEX': r'\w+-\w+'}}
            {'TEXT': {'REGEX': r"[A-Z][\w'’]+"}},
            {'TEXT': {'REGEX': r'-'}},
            {'TEXT': {'REGEX': r"[A-Z][\w'’]+"}},
            {'TEXT': {'REGEX': r"^([A-Z])|([A-Z][\w’'-]+)|(-)|(’)$"}, 'OP': '*'},
            # {'TEXT': {'REGEX': r'\w+'}},
        ])

    def quote_merger(self, doc):
        matched_spans = []
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            matched_spans.append(span)
            # print(span)
        for span in matched_spans:
            span.merge()
        return doc
