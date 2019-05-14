NAME = {'POS': {'IN': ['PROPN', 'PUNCT',]}, 'OP': '*'}
# NAME = {'POS': 'PROPN', 'OP': '+'}
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
        {'POS': 'PROPN'},
        {'LOWER': '-', 'OP': '?'},
        NAME,
    ],
    'FATHER_SON_3': [
        {'POS': 'PROPN', 'OP': '!',},
        {'LOWER': ',', 'OP' : '!'},
        {'LOWER': 'fils'},
        DE,
        {'POS': 'PROPN'},
        NAME,
        {'LOWER': ','},
        {'LOWER': '-', 'OP': '?'},
        {'POS': 'PROPN'},
        NAME,
    ],

    'FATHER_DAUGHTER_2': [
        NAME,
        {'LOWER': ','},
        {'LOWER': 'fille'},
        DE,
        {'POS': 'PROPN'},
        NAME,
    ],

    'FATHER_DAUGHTER_4': [
        {'POS': 'PROPN', 'OP': '!',},
        {'LOWER': 'fille'},
        DE,
        {'POS': 'PROPN'},
        {'LOWER': '-', 'OP': '?'},
        NAME,
    ],

    'GENDRE_1': [ NAME, {'POS': 'PROPN'}, {'LOWER': ','}, {'LOWER': 'gendre',}, DE, {'POS': 'PROPN'}, NAME, ],
    'GENDRE_2': [ NAME, {'POS': 'PROPN'}, {'LOWER': ','}, {'LOWER': 'gendre',}, DE, {'POS' : 'N'}, ],

}