class Finding:
    def __init__(self, rule, lineno, severity, message):
        self.rule_id = rule.id
        self.cwe = rule.weakness
        self.lineno = lineno
        self.severity = severity
        self.message = message

    def __str__(self):
        return (
            f"[{self.severity}] {self.rule_id} "
            f"(CWE: {self.cwe}) at line {self.lineno}: {self.message}"
        )
