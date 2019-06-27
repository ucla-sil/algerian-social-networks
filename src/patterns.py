NAME = {'POS': {'IN': ['PROPN',]}, 'OP': '+'}
DE = {'TEXT': {'REGEX': "^d[eu']$" }}
BEY = {'TEXT': {'LOWER': 'bey', }, 'OP': '?'}


MATCHERS = {
    'FATHER_SON_1': [
        {'POS': 'PROPN', 'OP': '!',},
        {'LOWER': ',', 'OP' : '!'},
        {'LOWER': 'fils'},
        {},
        DE,
        BEY,
        {'POS': 'PROPN'},
        {'LOWER': '-', 'OP': '?'},
        NAME,
    ],
    'FATHER_SON_2': [
        NAME,
        {'LOWER': ','},
        {'LOWER': 'fils'},
        DE,
        BEY,
        NAME,
    ],
    'FATHER_SON_3': [
        {'POS': 'PROPN', 'OP': '!',},
        {'LOWER': ',', 'OP' : '!'},
        {'LOWER': 'fils'},
        DE,
        BEY,
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
        BEY,
        NAME,
    ],

    'FATHER_DAUGHTER_4': [
        {'POS': 'PROPN', 'OP': '!',},
        {'LOWER': 'fille'},
        DE,
        BEY,
        {'POS': {'IN': ['PROPN',]}, 'OP': '+'}
    ],

    'GENDRE_1': [ NAME, {'LOWER': ','}, {'LOWER': 'gendre',}, DE, NAME, ],
    'GENDRE_2': [ NAME, {'LOWER': ','}, {'LOWER': 'gendre',}, DE, {'POS' : 'N'}, ],

}