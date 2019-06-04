class TestUtilsMixin:

    def notImplemented(self):
        raise NotImplementedError("Method not implemented")

    def debug_doc(self, doc):
        for token in doc:
            print(token.text, token.pos_, token.tag_)

    def _assert_is_propn(self, item):
        self.assertEqual('PROPN', item.pos_)

    def _assert_ents_found(self, to_find: list, find_in):
        self.assertEqual(len(to_find), len(find_in), '/'.join(str(_) for _ in find_in))

        found_ents_strings = set([str(ent) for ent in find_in])
        for ent in to_find:
            self.assertIn(ent, found_ents_strings)

