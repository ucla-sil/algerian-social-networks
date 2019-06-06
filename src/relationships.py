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

    def __init__(self, father, husband):
        self.father = father
        self.husband = husband


class RelationshipHandler:

    def __init__(self):
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

    def handle_fd_3(self, matcher, doc, i, matches):
        pass

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

    def handle_gendre_1(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        self.relationships.append(GendreRelationship(
            father=inner_doc.ents[0],
            husband=inner_doc.ents[1],
        ))

    def handle_gendre_2(self, matcher, doc, i, matches):
        _, start, end = matches[i]
        inner_doc = doc[start:end]
        self.relationships.append(
            GendreRelationship(
                husband=inner_doc.ents[0],
                father=inner_doc[-1]
            )
        )