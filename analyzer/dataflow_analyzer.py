import ast
from .dataflow_tracker import DataFlowTracker


class DataFlowAnalyzer:
    def analyze(self, tree):
        self._attach_parents(tree)

        tracker = DataFlowTracker()
        tracker.walk(tree)

        return tracker.symbols

    def _attach_parents(self, tree):
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
