import uuid


class FatherSonRelationship:

    def __init__(self, father='unnamed father', son='unnamed son'):
        self.father = father
        self.son = son


class FatherDaughterRelationship:

    def __init__(self, father, daughter, matched_rule):
        self.father = father
        self.daughter = daughter
        self.matched_rule = matched_rule


class GendreRelationship:

    def __init__(self, father, husband, name):
        self.father = father
        self.husband = husband
        self.name = name


class RelationshipHandler:

    def __init__(self, names=None):
        self.relationships = []

    def handle_fs_1(self, matcher, doc, i, matches):
        match_id, start, end = matches[i]
        inner_doc = doc[start:end]
        self.relationships.append(FatherSonRelationship(father=inner_doc.ents[0]))

    def handle_fs_2(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        if len(inner_doc.ents) == 1:
            son = inner_doc[0]
            father = inner_doc.ents[0]
        else:
            son = inner_doc.ents[0]
            father = inner_doc.ents[1]

        self.relationships.append(FatherSonRelationship(
            son=son,
            father=father
        ))

    def handle_fs_3(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        self.relationships.append(FatherSonRelationship(
            father=inner_doc.ents[0]
        ))

    def handle_fd_1(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        daughter = inner_doc.ents[0].text
        pos = 0
        father = None
        while pos < 100:
            pos += 1
            if doc[start - pos].tag_ == 'PROPN':
                father = doc[start - pos].text
                break
        if father and daughter:
            self.relationships.append(FatherDaughterRelationship(father=father, daughter=daughter, matched_rule='fd1'))

    def handle_fd_2(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        if len(inner_doc.ents) < 2:
            for word in inner_doc:
                print(word, word.pos_, word.tag_)
            print('Found mismatch')
        self.relationships.append(FatherDaughterRelationship(
            daughter=inner_doc.ents[0],
            father=inner_doc.ents[1],
            matched_rule='fd2'
        ))

    def __find_prior_entity(self, start, limit, doc):
        index = start

        tag_start = None
        tag_end = None

        while index > 0 and index > (start - limit):
            if doc[index].tag_ == 'PROPN':
                if not tag_end:
                    tag_end = index + 1
                tag_start = index
            elif tag_end:
                tag_start = index + 1
                break
            index -= 1
        if not tag_start:
            tag_start = index
        if tag_start and tag_end:
            return doc[tag_start:tag_end]

    def handle_fd_3(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        daughter = 'unnamed daughter'
        father = self.__find_prior_entity(start, 100, doc) or 'father not found'

        self.relationships.append(FatherDaughterRelationship(
            daughter=daughter,
            father=father,
            matched_rule='fd3'
        ))

    def handle_fd_4(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        father = None
        if inner_doc.ents:
            father = inner_doc.ents[0].text
        # else:
        #     father = inner_doc.conjuncts[0]
        self.relationships.append(FatherDaughterRelationship(
            father=father,
            daughter='unnamed daughter',
            matched_rule='fd4'
        ))

    def handle_mariage_1_and_2(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        husband = inner_doc.ents[0]
        father = self.__find_prior_entity(start, 100, doc) or 'father not found'
        self.relationships.append(GendreRelationship(
            father=father,
            husband=husband,
            name='unnamed woman'
        ))

    def handle_mariage_3_and_4(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        father = inner_doc.ents[0]
        husband = self.__find_prior_entity(start, 100, doc) or 'husband not found'
        self.relationships.append(GendreRelationship(
            father=father,
            husband=husband,
            name = 'unnamed woman'
        ))

    def handle_mariage_5(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        name = inner_doc.ents[0]
        index = start - 1
        husband = self.__find_prior_entity(start, 100, doc) or 'husband not found'
        self.relationships.append(GendreRelationship(
            father='father not located by pattern',
            name=name,
            husband=husband
        ))

    def handle_mariage_6(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        name = inner_doc.ents[0]
        husband = inner_doc.ents[1]
        index = start - 1
        father = self.__find_prior_entity(start, 100, doc) or 'father not found'
        self.relationships.append(GendreRelationship(
            father=father,
            husband=husband,
            name=name
        ))

    def handle_gendre_1(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        self.relationships.append(GendreRelationship(
            father=inner_doc.ents[0],
            husband=inner_doc.ents[1],
            name='unnamed woman'
        ))

    def handle_gendre_2(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        self.relationships.append(
            GendreRelationship(
                husband=inner_doc.ents[0],
                father=inner_doc[-1],
                name='unnamed woman'
            )
        )

    def handle_gendre_3(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        husband = inner_doc.ents[0]
        index = start - 1
        father = self.__find_prior_entity(start, 100, doc) or 'father not found'
        self.relationships.append(GendreRelationship(
            father=father,
            husband=husband,
            name="unnamed woman"
        ))

    def handle_pere_1(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        father = inner_doc.ents[0]
        son = inner_doc.ents[1]
        self.relationships.append(FatherSonRelationship(
            father=father,
            son=son
        ))


class Mention:

    def __init__(self, span):
        self.span = span


class Person:

    def __init__(self, name):
        self.name = name
        self.gender = None
        self.spouse = None
        self.father = None
        self.mother = None
        self.children = {}

        self.mentions = []


class PeopleSet:

    def __init__(self, names):
        self.relationships = []
        self.people = names
        self.parse_errors = []

    def _name(self, name_ent):
        return str(name_ent).replace('- ', '-')

    def handle_fs_1(self, matcher, doc, i, matches):
        match_id, start, end = matches[i]
        inner_doc = doc[start:end]
        self.relationships.append(FatherSonRelationship(father=inner_doc.ents[0]))
        father_name = self._name(inner_doc.ents[0])
        son = Person('unnamed')

        son.father = self.people[father_name]
        son.gender = 'male'
        self.people[father_name].children[son.name] = son
        self.people[father_name].gender = 'male'

    def handle_fs_2(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]

        if len(inner_doc.ents) == 2:
            son_name = name_from_text(inner_doc.ents[0])
            father_name = name_from_text(inner_doc.ents[1])
        else:
            son_name = name_from_text(inner_doc[0])
            father_name = name_from_text(inner_doc[-1])

        if son_name not in self.people:
            self.people[son_name] = Person(son_name)
        if father_name not in self.people:
            self.people[father_name] = Person(father_name)

        self.people[son_name].father = self.people[father_name]
        self.people[father_name].children[son_name] = self.people[son_name]
        self.people[father_name].gender = 'male'
        self.people[son_name].gender = 'male'

    def handle_fs_3(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        # self.relationships.append(FatherSonRelationship(
        #     father=inner_doc.ents[0]
        # ))
        father_name = name_from_text(inner_doc.ents[0])
        son_id = uuid.uuid4()
        son = Person(son_id)
        son.gender = 'male'
        self.people[father_name].children[son_id] = son

    def handle_fd_1(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        daughter_name = name_from_text(inner_doc.ents[0])
        daughter = self.people[daughter_name]
        daughter.gender = 'female'
        pos = 0
        father = None
        while pos < 100:
            pos += 1
            if doc[start - pos].tag_ == 'PROPN':
                father_name = name_from_text(doc[start - pos])
                father = self.people[father_name]
                break
        if father and daughter:
            self.people[father_name].children[daughter_name] = daughter
            self.people[daughter_name].father = father
            self.relationships.append(FatherDaughterRelationship(father=father, daughter=daughter, matched_rule='fd1'))

    def handle_fd_2(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        if len(inner_doc.ents) < 2:
            for word in inner_doc:
                print(word, word.pos_, word.tag_)
            print('Found mismatch')
        daughter_name = name_from_text(inner_doc.ents[0])
        if daughter_name == 'Daika':
            print(inner_doc)
        father_name = name_from_text(inner_doc.ents[1])
        daughter = self.people[daughter_name]
        daughter.gender = 'female'
        father = self.people[father_name]
        father.gender = 'male'
        father.children[daughter_name] = daughter
        daughter.father = father
        self.relationships.append(FatherDaughterRelationship(
            daughter=inner_doc.ents[0],
            father=inner_doc.ents[1],
            matched_rule='fd2'
        ))

    def handle_fd_3(self, matcher, doc, i, matches):
        pass

    def handle_fd_4(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        daughter_name = uuid.uuid4()
        daughter = Person(daughter_name)
        daughter.gender = 'female'
        father_name = name_from_text(inner_doc.ents[0])
        try:
            father = self.people[father_name]
        except KeyError as ex:
            self.parse_errors.append(
                {
                    'phrase': inner_doc,
                    'daughter': daughter,
                    'problem': 'missing father',
                }
            )
            return
        father.children[daughter_name] = daughter
        daughter.father = father
        # self.relationships.append(FatherDaughterRelationship(
        #     father=father,
        #     daughter='unnamed daughter',
        #     matched_rule='fd4'
        # ))

    def handle_gendre_1(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        self.relationships.append(GendreRelationship(
            father=inner_doc.ents[0],
            husband=inner_doc.ents[1],
        ))
        father_name = name_from_text(inner_doc[0])
        husband_name = name_from_text(inner_doc.ents[1])
        father = self.people[father_name]
        husband = self.people[husband_name]
        unnamed_woman_id = uuid.uuid4()
        unnamed_woman = Person(unnamed_woman_id)
        unnamed_woman.gender = 'female'
        self.people[father_name].father = father
        self.people[husband_name].spouse = husband

    def handle_gendre_2(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        father_name = name_from_text(inner_doc[-1])
        husband_name = name_from_text(inner_doc.ents[0])
        father = self.people[father_name]
        husband = self.people[husband_name]
        unnamed_woman_id = uuid.uuid4()
        unnamed_woman = Person(unnamed_woman_id)
        unnamed_woman.gender = 'female'
        self.people[father_name].father = father
        self.people[husband_name].spouse = husband
        # self.relationships.append(
        #     GendreRelationship(
        #         husband=inner_doc.ents[0],
        #         father=inner_doc[-1]
        #     )
        # )


def name_from_text(ent):
    try:
        tokens = ' '.join([str(t) for t in ent if str(t).lower() != 'bey'])
    except TypeError:
        tokens = str(ent)
    cleaned_name = tokens.replace('bey-', ' ').replace('-bey', ' ')
    cleaned_name = cleaned_name.replace('Bey-', ' ').replace('-Bey', ' ')
    cleaned_name = cleaned_name.replace('- ', '-')
    if cleaned_name[0] == '-':
        cleaned_name = cleaned_name[1:]
    if cleaned_name[-1] == '-':
        cleaned_name = cleaned_name[:-1]
    return cleaned_name.strip()