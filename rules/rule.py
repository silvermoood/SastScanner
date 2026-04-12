class Rule:
    def __init__(self, data):
        self.id = data["id"]
        self.weakness = data["weakness"]
        self.patterns = data["patterns"]
        self.context_constraints = data.get("context_constraints", {})
        self.severity_policy = data["severity_policy"]
        self.explanation_template = data["explanation_template"]
