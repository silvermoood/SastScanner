import ast


class SeverityEngine:
    def calculate(self, rule, node, symbols):
        severity = rule.severity_policy.get("base", "MEDIUM")

        if getattr(node, "args", None):
            arg = node.args[0]
            names = self._collect_names(arg)
            for name in names:
                if symbols.is_tainted(name):
                    severity = rule.severity_policy.get("tainted_input", "CRITICAL")
                    break

        return severity

    def _collect_names(self, node):
        names = set()
        for n in ast.walk(node):
            if isinstance(n, ast.Name):
                names.add(n.id)
        return names
