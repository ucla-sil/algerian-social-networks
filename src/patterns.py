NAME = {'POS': {'IN': ['PROPN', 'NOUN',]}, 'OP': '+'}
DE = {'REGEX': "d[eu']"}


MATCHERS = {
    'FATHER_SON_1': [
        {'POS': 'PROPN', 'OP': '!',},
        {'LOWER': ',', 'OP' : '!'},
        {'LOWER': 'fils'},
        {},
        DE,
        {'POS': 'PROPN'},
        {'LOWER': '-', 'OP': '?'},
        NAME,
    ],
    'FATHER_SON_2': [
        NAME,
        {'LOWER': ','},
        {'LOWER': 'fils'},
        DE,
        NAME,
    ],
    'FATHER_SON_3': [
        {'POS': 'PROPN', 'OP': '!',},
        {'LOWER': ',', 'OP' : '!'},
        {'LOWER': 'fils'},
        DE,
        NAME,
        {'LOWER': ','},
        NAME,
    ],

    'FATHER_DAUGHTER_1': [
        # NOTE: this is just the match for the daughter's name. We find the father's name in the handler.
        {'LOWER': 'sa',},
        {'LOWER': 'fille',},
        {'LOWER': ',', 'OP': '?'},
        NAME,
    ],

    'FATHER_DAUGHTER_2': [
        NAME,
        {'LOWER': ','},
        {'LOWER': 'fille'},
        DE,
        NAME,
    ],

    'FATHER_DAUGHTER_4': [
        {'POS': 'PROPN', 'OP': '!',},
        {'LOWER': 'fille'},
        DE,
        NAME,
    ],

    'GENDRE_1': [ NAME, {'LOWER': ','}, {'LOWER': 'gendre',}, DE, NAME, ],
    'GENDRE_2': [ NAME, {'LOWER': ','}, {'LOWER': 'gendre',}, DE, {'POS' : 'N'}, ],

}