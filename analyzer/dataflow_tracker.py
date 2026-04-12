import ast
from .symbol_table import SymbolTable
from .function_table import FunctionTable


class DataFlowTracker(ast.NodeVisitor):

    def __init__(self):
        super().__init__()
        self.symbols = SymbolTable()
        self.functions = FunctionTable()
        # objects: {varname: {"type":"hash", "algo":"md5", "tainted": bool}}
        self.objects = {}

    def walk(self, tree):
        # use NodeVisitor to process nodes in source order
        self.visit(tree)
        return self.symbols

    def visit_Assign(self, node):
        # handle single-target simple assignments only
        if len(node.targets) != 1:
            self.generic_visit(node)
            return
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            self.generic_visit(node)
            return
        tname = target.id

        # assignment from a call, e.g. param = request.form.get(...)
        if isinstance(node.value, ast.Call):
            fname = self._get_full_name(node.value.func)

            # request.* sources -> tainted
            if fname and fname.startswith("request."):
                self.symbols.mark_tainted(tname)

            # hashlib.md5() or hashlib.sha1() -> create hash object
            elif fname in ("hashlib.md5", "hashlib.sha1"):
                self.objects[tname] = {"type": "hash", "algo": fname.split(".")[1], "tainted": False}

            # assigned from digest() -> if source hash object was tainted, mark target tainted
            elif isinstance(node.value.func, ast.Attribute) and node.value.func.attr == "digest":
                obj = self._get_obj_name(node.value.func)
                if obj and obj in self.objects and self.objects[obj].get("tainted"):
                    self.symbols.mark_tainted(tname)

            else:
                # if call returns value from a tainted arg (e.g. foo(tainted)) -> mark tname tainted
                for arg in node.value.args:
                    if isinstance(arg, ast.Name) and self.symbols.is_tainted(arg.id):
                        self.symbols.mark_tainted(tname)
                        break
                # also if the method is called on a tainted object (e.g. bar.encode()) mark target tainted
                if isinstance(node.value.func, ast.Attribute):
                    base = self._get_obj_name(node.value.func)
                    if base and self.symbols.is_tainted(base):
                        self.symbols.mark_tainted(tname)

        # assignment from name: a = b (propagate taint and object-state)
        elif isinstance(node.value, ast.Name):
            if self.symbols.is_tainted(node.value.id):
                self.symbols.mark_tainted(tname)
            if node.value.id in self.objects:
                self.objects[tname] = dict(self.objects[node.value.id])

        else:
            # best-effort: if expression uses tainted names -> mark tname tainted
            for name in self._find_names(node.value):
                if self.symbols.is_tainted(name):
                    self.symbols.mark_tainted(tname)
                    break

        self.generic_visit(node)

    def visit_Expr(self, node):
        # handle expression calls, e.g. h.update(bar) or f.write(some)
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
            call = node.value
            method = call.func.attr
            obj = self._get_obj_name(call.func)

            # hash update: if arg tainted, mark object tainted
            if method == "update" and obj and obj in self.objects:
                for arg in call.args:
                    if isinstance(arg, ast.Name) and self.symbols.is_tainted(arg.id):
                        self.objects[obj]["tainted"] = True
                        break

            # other side-effects (write, etc.) we don't mark here — severity engine will check tainted args
        self.generic_visit(node)

    def _get_full_name(self, func):
        # return dotted full name for Name/Attribute where possible
        if isinstance(func, ast.Name):
            return func.id
        elif isinstance(func, ast.Attribute):
            parts = []
            node = func
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
                    return None
            parts.reverse()
            return ".".join(parts)
        return None

    def _get_obj_name(self, attr_node):
        # return the base object name for an attribute like h.update -> 'h'
        if isinstance(attr_node, ast.Attribute):
            value = attr_node.value
            if isinstance(value, ast.Name):
                return value.id
        return None

    def _find_names(self, node):
        names = set()
        for n in ast.walk(node):
            if isinstance(n, ast.Name):
                names.add(n.id)
        return names