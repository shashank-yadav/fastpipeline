from typing import Dict, Any

class BaseNode:
    def __init__(self, config: Dict):
        pass

    def run(self, input: Dict[str, Any]):
        # raise NotImplementedError
        pass

    def log(self):
        pass

if __name__ == "__main__":
    # execute only if run as a script
    # n = Node()
    print(type(BaseNode))