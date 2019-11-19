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

    'FATHER_DAUGHTER_3': [
        {'LOWER': 'sa'},
        {'LOWER': 'fille'},
        {'POS': {'IN': ['PROPN', ]}, 'OP': '!'}
    ],

    'FATHER_DAUGHTER_4': [
        {'POS': {'IN': ['PROPN', ]}, 'OP': '!'},
        {'LOWER': ',', 'OP': '!'},
        {'LOWER': 'fille'},
        DE,
        BEY,
        NAME
    ],

    'MARIAGE_1': [
        {'LOWER': 'en'},
        {'LOWER': 'mariage'},
        {'LOWER': 'sa'},
        {'LOWER': 'fille'},
        {'POS': {'IN': ['PROPN', ]}, 'OP': '+'}
    ],

    'MARIAGE_2': [
        {'LOWER': 'sa'},
        {'LOWER': 'fille'},
        {'LOWER': 'en'},
        {'LOWER': 'mariage'},
        {'POS': {'IN': ['PROPN', ]}, 'OP': '+'}
    ],

    'MARIAGE_3': [
        {'POS': {'IN': ['PROPN', ]}, 'OP': '+'},
        {'LOWER': 'dont'},
        {'LOWER': 'il'},
        {'LOWER': 'avait', 'OP': '?'},
        {'REGEX': 'épous[\w]+'},
        {'REGEX': 'sa|la|une'},
        {'REGEX': 'fille'},
        {'POS': {'IN': ['PROPN', ]}, 'OP': '+'}
    ],

    'MARIAGE_4': [
        {'POS': {'IN': ['PROPN', ]}, 'OP': '+'},
        {'LOWER': 'en'},
        {'LOWER': 'épousant'},
        {'REGEX': 'sa|la|une'},
        {'LOWER': 'fille'},
        {'POS': {'IN': ['PROPN', ]}, 'OP': '+'}
    ],

    'MARIAGE_5': [
        {'POS': {'IN': ['PROPN', ]}, 'OP': '+'},
        {'LOWER': 'il'},
        {'LOWER': 'avait', 'OP': '?'},
        {'REGEX': 'épous[\w]+'},
        {'POS': {'IN': ['PROPN', ]}, 'OP': '+'}
    ],

    'MARIAGE_6': [
        {'LOWER': 'en'},
        {'LOWER': 'mariage'},
        {'LOWER': 'sa'},
        {'LOWER': 'fille'},
        {'POS': {'IN': ['PROPN', ]}, 'OP': '+'},
        {'LOWER': 'à'},
        {'POS': {'IN': ['PROPN', ]}, 'OP': '+'}
    ],

    'GENDRE_1': [ NAME, {'LOWER': ','}, {'LOWER': 'gendre',}, DE, NAME, ],
    'GENDRE_2': [ NAME, {'LOWER': ','}, {'LOWER': 'gendre',}, DE, {'POS' : 'N'}, ],
    'GENDRE_3': [
        {'LOWER': 'son'},
        {'LOWER': 'gendre'},
        {'POS': {'IN': ['PROPN', ]}, 'OP': '+'}
    ],

    'PERE': [
        {'POS': {'IN': ['PROPN', ]}, 'OP': '+'},
        {'LOWER': ','},
        {'LOWER': 'son'},
        {'LOWER': 'beau'},
        {'LOWER': 'père'},
        {'POS': {'IN': ['PROPN', ]}, 'OP': '+'}
    ]

}