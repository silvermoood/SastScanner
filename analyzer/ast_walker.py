import ast


class ASTWalker:
    @staticmethod
    def walk(tree):

        if tree is None:
            return []
        return ast.walk(tree)