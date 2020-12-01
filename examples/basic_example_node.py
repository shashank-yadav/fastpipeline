import sys
import os
sys.path.append('C://Users//admin//projects//fastpipeline')

# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)

from fastpipeline.base_node import BaseNode

class Node(BaseNode):
    def __init__(self):
        super().__init__()

    def new_func(self):
        return 10

if __name__ == "__main__":
    node = Node()
    print(node.hash())
    import pdb; pdb.set_trace()