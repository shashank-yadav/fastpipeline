from mlpipeline.base_node import BaseNode

class Node(BaseNode):
    def __init__(self, config={}):
        super().__init__(config)

    
if __name__ == "__main__":
    # execute only if run as a script
    n = Node()
    print(type(Node))