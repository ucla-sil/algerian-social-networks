class TestUtilsMixin:

    def notImplemented(self):
        raise NotImplementedError("Method not implemented")

    def debug_doc(self, doc):
        for token in doc:
            print(token.text, token.pos_, token.tag_)
