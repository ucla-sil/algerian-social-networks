import glob
import codecs


def coref_opens(coref_str: str) -> bool:
    return coref_str[0] == '('


def coref_closes(coref_str: str) -> bool:
    return coref_str[-1] == ')'


def coref_continues(coref_str: str) -> bool:
    return not coref_opens_and_closes(coref_str)


def coref_opens_and_closes(coref_str: str) -> bool:
    return coref_str[0] == '(' and coref_str[-1] == ')'


def empty_coref(coref_str: str) -> bool:
    return coref_str == '-'


def coref_from_string(coref_str: str) -> str:
    if coref_opens_and_closes(coref_str):
        return coref_str[1:-1]
    elif coref_opens(coref_str):
        return coref_str[1:]
    elif coref_closes(coref_str):
        return coref_str[:-1]
    else:
        if '(' in coref_str or ')' in coref_str:
            raise Exception(f'Paren found in coref_str {coref_str}')
        return coref_str


mistakes = {}
for in_filename in glob.glob('../data/train/*_conll'):
    with codecs.open(in_filename, encoding='utf-8') as in_file:
        mistakes_this_file = []
        coref_open = False
        current_coref = None
        for line_no, line in enumerate(in_file):
            line_text = line.strip()
            if line[0] == '#' or not line_text:
                continue

            possible_coref = line.strip().split('\t')[-1]
            if coref_open:
                if coref_closes(possible_coref):
                    coref_open = False
                elif coref_opens(possible_coref):
                    current_coref = coref_from_string(possible_coref)
                    mistakes_this_file.append(current_coref)
                elif empty_coref(possible_coref):
                    mistakes_this_file.append(current_coref)
                    current_coref = None
                    coref_open = False
                else:
                    # Coref continues
                    pass
            else:
                if coref_opens_and_closes(possible_coref):
                    continue
                elif coref_opens(possible_coref):
                    current_coref = coref_from_string(possible_coref)
                    coref_open = True
                elif coref_closes(possible_coref):
                    mistakes_this_file.append(current_coref)
                    mistakes_this_file.append(possible_coref)
        if mistakes_this_file:
            mistakes[in_filename] = mistakes_this_file

if not mistakes:
    print('No errors found')
else:
    for filename, mistake_list in mistakes.items():
        print(filename)
        for mistake in mistake_list:
            print(f'\t{mistake}')

