from .pattern_analyzer import PatternAnalyzer
from .context_analyzer import ContextAnalyzer
from .dataflow_analyzer import DataFlowAnalyzer
from .severity_engine import SeverityEngine
from .finding import Finding


class Analyzer:
    def __init__(self, rules):
        self.pattern = PatternAnalyzer(rules)
        self.context = ContextAnalyzer()
        self.dataflow = DataFlowAnalyzer()
        self.severity = SeverityEngine()

    def analyze(self, tree):
        matches = self.pattern.analyze(tree)
        refined = self.context.analyze(matches)
        symbols = self.dataflow.analyze(tree)

        findings = []

        for rule, node in refined:
            severity = self.severity.calculate(rule, node, symbols)
            msg = rule.explanation_template
            findings.append(
                Finding(rule, node.lineno, severity, msg)
            )

        return findings
