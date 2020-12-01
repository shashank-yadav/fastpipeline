from fastpipeline.base_node import BaseNode
import pytest

class TestNodeWithRun(BaseNode):
    def __init__(self, config):
        super().__init__(config)

    def run(self, input):
        return input


class TestNodeWithoutRun(BaseNode):
    def __init__(self, config):
        super().__init__(config)

def test_base_node_without_run():
    with pytest.raises(NotImplementedError):
        n = TestNodeWithoutRun(config={})
