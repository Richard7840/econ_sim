class Event:
    def __init__(self, name, description, trigger_threshold, effects):
        self.name = name
        self.description = description
        self.trigger_threshold = trigger_threshold
        self.effects = effects
