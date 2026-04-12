import ast
from .ast_walker import ASTWalker


class PatternAnalyzer:
    def __init__(self, rules):
        self.rules = rules

    def analyze(self, tree):
        matches = []

        for node in ASTWalker.walk(tree):
            if isinstance(node, ast.Call):
                func_names = self._get_func_names(node)

                for rule in self.rules:
                    for name in func_names:
                        if name and name in rule.patterns:
                            matches.append((rule, node))
                            break

        return matches

    def _get_func_names(self, node):
        """
        Return a list of possible function identifiers for a Call node.
        Examples:
          - hashlib.md5(...) -> ['hashlib.md5', 'md5']
          - h.update(...)     -> ['h.update', 'update']
          - open(...)         -> ['open']
        """
        names = []
        func = node.func
        if isinstance(func, ast.Attribute):
            full = self._get_attribute_fullname(func)
            if full:
                names.append(full)
            # also add the attribute name itself (method name)
            names.append(func.attr)
        elif isinstance(func, ast.Name):
            names.append(func.id)
        return names

    def _get_attribute_fullname(self, attr_node):
        parts = []
        node = attr_node
        # attr_node is an Attribute, walk back to build dotted name
        while isinstance(node, ast.Attribute):
            parts.append(node.attr)
            value = node.value
            if isinstance(value, ast.Name):
                parts.append(value.id)
                break
            elif isinstance(value, ast.Attribute):
                node = value
                continue
            else:
                # could be complex expression; give up building fullname
                return None
        parts.reverse()
        return ".".join(parts)