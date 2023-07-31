import json

class ChoreConfig():
    def __init__(self, attrs={}):
        self._attrs = attrs
        

    def __repr__(self):
        return json.dumps(self._attrs)
    
    @staticmethod
    def load(s):
        config = ChoreConfig(json.loads(s))
        return config