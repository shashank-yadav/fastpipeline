from os import path
from mlpiptline.base_node import BaseNode
from typing import List, Dict, Any, Tuple

class PipeLine:
    def __init__(self, experiment_name: str, workers: List[Tuple(str, BaseNode, Dict)], experiments_dir: str = './experiments'):
        self.experiment_name = experiment_name
        self.experiments_dir = experiments_dir
        self.savedir = path.join(self.experiments_dir, experiment_name)
        self.workers = workers

    def run(self, input: Dict[str, Any]):
        if not os.path.exists(self.experiments_dir):
            os.makedirs(self.experiments_dir)

        for node in nodes:
            out = node.run(input)
            input = out
                
        return out


if __name__ == "__main__":
    