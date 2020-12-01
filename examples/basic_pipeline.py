import sys
import os
sys.path.append('C://Users//admin//projects//fastpipeline')

from fastpipeline.base_node import BaseNode
from fastpipeline.pipeline import PipeLine

class Node1(BaseNode):
    def __init__(self):
        super().__init__()

    def run(self, input):
        return {
            'x': 10
        }

class Node2(BaseNode):
    def __init__(self):
        super().__init__()

    def run(self, input):
        return {
            'x': input['x']*2
        }



if __name__ == "__main__":
    node1 = Node1()
    node2 = Node2()
    
    pipeline = PipeLine('test', [node1, node2])
    out = pipeline.run({'x': 10})
    print(out)