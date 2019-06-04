import spacy
import spacy.matcher
import spacy.symbols


class HyphenatedNameMerger:
    
    def __init__(self, vocab):
        self.__matcher = spacy.matcher.Matcher(vocab)
        self.__matcher.add('HYPHENATED_NAMES', None, [
            {'TEXT': {'REGEX': r"[A-Z][\w-]+"}},
            # {'TEXT': {'REGEX': r'-'}, "OP": '?'},
            {'TEXT': {'REGEX': r"([A-Z][\w'-]+)|(-)"}},
            {'TEXT': {'REGEX': r"^([A-Z][\w-]+)|([MR][’'])|(-)|(’)$"}, 'OP': '*'},
        ])

        self.__matcher.add('NAMES_WITH_APOSTROPHES', None, [
            {'TEXT': {'REGEX': r"[A-Z][\w-]+"}},
            {'TEXT': {'REGEX': r'-'}},
            {'TEXT': {'REGEX': r"^([A-Z])|([MR][\w’'-]+)|(-)|(’)$"}, 'OP': '*'},
            {'TEXT': {'REGEX': r"[MR]['’]"}},
            {'TEXT': {'REGEX': r"[\w]+"}},
            {'TEXT': {'REGEX': r"^([A-Z])|([A-Z][\w’'-]+)|(-)|(’)$"}, 'OP': '*'},
            {'TEXT': {'REGEX': r"[MR]['’]"}, 'OP': '*'},
            {'TEXT': {'REGEX': r"[\w]+"}, 'OP': '*'},
        ])

    def merger(self, doc):
        matched_spans = []
        matches = self.__matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            matched_spans.append(span)
        with doc.retokenize() as retokenizer:
            for span in self.__filter_spans(matched_spans):
                retokenizer.merge(span, attrs={
                    'POS': spacy.symbols.PROPN,
                    'TAG': spacy.symbols.PROPN,
                    spacy.symbols.ENT_TYPE: spacy.symbols.PERSON,
                    # spacy.symbols.ENT_IOB: 'B',
                    # 'LABEL': 'ENT',
                })
                doc.ents = list(doc.ents) + [spacy.tokens.Span(
                    doc, span.start, span.end, label=spacy.symbols.PERSON
                )]
        return doc

    def __filter_spans(self, spans):
        # Filter a sequence of spans so they don't contain overlaps
        get_sort_key = lambda span: (span.end - span.start, span.start)
        sorted_spans = sorted(spans, key=get_sort_key, reverse=True)
        result = []
        seen_tokens = set()
        for span in sorted_spans:
            if span.start not in seen_tokens and span.end - 1 not in seen_tokens:
                result.append(span)
                seen_tokens.update(range(span.start, span.end))
        return result
