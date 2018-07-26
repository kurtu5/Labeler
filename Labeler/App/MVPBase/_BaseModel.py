class BaseModel(object):
    other_models = {}
    def __init__(self, name, other_models = None):
        """ Base model stores list of related models """
        self.observer = None
        self.name = name
        self.others = {}
        self.other_models[name] = self

        if other_models:
            for other in other_models:
                self.add_model(other)

        # Allow for showable windows
        self.window_enabled = False

    def sib(self, model_name):
        return self.other_models[model_name]
    
    def add_model(self, other):
        self.others[other.name]=other

    def start(self, observer):
        self.observer = observer
        self.window_enabled = self.observer.event_gen('window_enable', False)
